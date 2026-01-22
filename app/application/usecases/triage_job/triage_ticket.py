import json
import uuid
from typing import Callable

from sqlalchemy.orm import Session

from app.application.commands.triage_ticket_command import TriageTicketCommand
from app.domain.entities.prompt import Prompt
from app.domain.entities.ticket import Ticket
from app.domain.entities.triage_job import TriageJob
from app.domain.entities.triage_job_log import TriageJobLog
from app.domain.enums.ticket_triage_status import TicketTriageStatus
from app.domain.gateways.llm_client_gateway import LLMClientGateway
from app.domain.gateways.prompt.find_active_prompt_gateway import FindActivePromptGateway
from app.domain.gateways.ticket.find_ticket_by_id_gateway import FindTicketByIdGateway
from app.domain.gateways.ticket.update_ticket_triage_status_gateway import UpdateTicketTriageStatusGateway
from app.domain.gateways.triage_job.create_triage_job_log_gateway import CreateTriageJobLogGateway
from app.domain.gateways.triage_job.claim_triage_job_gateway import ClaimTriageJobGateway
from app.domain.gateways.triage_job.find_next_pending_triage_job_gateway import FindNextPendingTriageJobDatabaseGateway
from app.domain.gateways.triage_job.update_triage_job_gateway import UpdateTriageJobGateway
from app.infrastructure.logging import get_logger


_logger = get_logger(__name__)

DEFAULT_PROMPT_NAME = "ticket-triage"
DEFAULT_LANGUAGE = "pt-BR"
DEFAULT_CUSTOMER_TIER = "free"
DEFAULT_TEMPERATURE = 0.2
DEFAULT_MAX_TOKENS = 800


class TriageTicketUseCase:
    def __init__(
            self,
            uow,
            client: LLMClientGateway,
            find_next_pending_triage_job_gateway: Callable[[Session], FindNextPendingTriageJobDatabaseGateway],
            claim_triage_job_gateway: Callable[[Session], ClaimTriageJobGateway],
            update_triage_job_gateway: Callable[[Session], UpdateTriageJobGateway],
            find_ticket_by_id_gateway: Callable[[Session], FindTicketByIdGateway],
            update_ticket_triage_status_gateway: Callable[[Session], UpdateTicketTriageStatusGateway],
            find_active_prompt_gateway: Callable[[Session], FindActivePromptGateway],
            create_triage_job_log_gateway: Callable[[Session], CreateTriageJobLogGateway],
            prompt_name: str = DEFAULT_PROMPT_NAME,
    ):
        self.uow = uow
        self._client = client
        self._find_next_pending_triage_job_gateway = find_next_pending_triage_job_gateway
        self._claim_triage_job_gateway = claim_triage_job_gateway
        self._update_triage_job_gateway = update_triage_job_gateway
        self._find_ticket_by_id_gateway = find_ticket_by_id_gateway
        self._update_ticket_triage_status_gateway = update_ticket_triage_status_gateway
        self._find_active_prompt_gateway = find_active_prompt_gateway
        self._create_triage_job_log_gateway = create_triage_job_log_gateway
        self._prompt_name = prompt_name

    def execute(self, command: TriageTicketCommand) -> TriageJob | None:
        if command.triage_job_id is None:
            triage_job = self._start_next_job()
        else:
            triage_job = self._start_job_by_id(command.triage_job_id)
        if triage_job is None:
            return None

        prompt = None
        ticket = None
        user_prompt = ""
        output = ""
        success = False
        final_job = triage_job
        ticket_status = TicketTriageStatus.FAILED

        try:
            ticket = self._load_ticket(triage_job.ticket_id)
            if ticket is None:
                raise RuntimeError(f"Ticket {triage_job.ticket_id} not found")
            ticket = self._apply_ticket_status(ticket, TicketTriageStatus.ON_TRIAGE)
            self._persist_ticket(ticket)

            prompt = self._load_prompt(ticket.owner_id)
            if prompt is None:
                raise RuntimeError(f"Prompt '{self._prompt_name}' not found")

            user_prompt = self._render_user_prompt(prompt, ticket)
            output = self._client.execute(
                system=prompt.system_prompt,
                user=user_prompt,
                temperature=DEFAULT_TEMPERATURE,
                max_tokens=DEFAULT_MAX_TOKENS,
            )
            output = self._ensure_json_output(prompt, user_prompt, output)
            success = True
            final_job = triage_job.on_complete()
            ticket_status = TicketTriageStatus.COMPLETED
        except Exception as exc:
            output = str(exc)
            final_job = triage_job.on_fail()
            ticket_status = TicketTriageStatus.FAILED
            _logger.execute(
                "exception",
                "triage_job_failed",
                triage_job_id=triage_job.id,
                ticket_id=triage_job.ticket_id,
            )
        finally:
            if prompt is None:
                _logger.execute(
                    "error",
                    "triage_prompt_not_found",
                    prompt_name=self._prompt_name,
                    owner_id=str(ticket.owner_id) if ticket else None,
                )
                self._finalize_job(
                    triage_job=final_job,
                    ticket=ticket,
                    ticket_status=ticket_status,
                    prompt=None,
                    user_prompt=user_prompt,
                    output=output,
                    success=success,
                )
            else:
                self._finalize_job(
                    triage_job=final_job,
                    ticket=ticket,
                    ticket_status=ticket_status,
                    prompt=prompt,
                    user_prompt=user_prompt,
                    output=output,
                    success=success,
                )

        return final_job

    def _start_next_job(self) -> TriageJob | None:
        uow = self._resolve_uow()
        with uow as active_uow:
            db = active_uow.session
            triage_job = self._find_next_pending_triage_job_gateway(db).execute()
            if triage_job is None:
                return None
            triage_job = triage_job.on_running()
            triage_job = self._update_triage_job_gateway(db).execute(triage_job)
            return triage_job

    def _start_job_by_id(self, triage_job_id: uuid.UUID) -> TriageJob | None:
        uow = self._resolve_uow()
        with uow as active_uow:
            db = active_uow.session
            triage_job = self._claim_triage_job_gateway(db).execute(triage_job_id)
            if triage_job is None:
                return None
            return triage_job

    def _finalize_job(
            self,
            *,
            triage_job: TriageJob,
            ticket: Ticket | None,
            ticket_status: TicketTriageStatus,
            prompt: Prompt | None,
            user_prompt: str,
            output: str,
            success: bool,
    ) -> None:
        uow = self._resolve_uow()
        with uow as active_uow:
            db = active_uow.session
            self._update_triage_job_gateway(db).execute(triage_job)
            if ticket is not None:
                try:
                    updated_ticket = self._apply_ticket_status(ticket, ticket_status)
                    self._update_ticket_triage_status_gateway(db).execute(updated_ticket)
                except Exception:
                    _logger.execute(
                        "exception",
                        "ticket_status_update_failed",
                        ticket_id=str(ticket.id),
                        ticket_status=str(ticket_status),
                    )
            triage_job_log = TriageJobLog.create(
                input=user_prompt,
                output=self._normalize_output(output),
                prompt_id=prompt.id if prompt else None,
                success=success,
                triage_job_id=triage_job.id,
            )
            self._create_triage_job_log_gateway(db).execute(triage_job_log)

    def _load_ticket(self, ticket_id) -> Ticket | None:
        uow = self._resolve_uow()
        with uow as active_uow:
            db = active_uow.session
            return self._find_ticket_by_id_gateway(db).execute(ticket_id)

    def _load_prompt(self, owner_id) -> Prompt | None:
        uow = self._resolve_uow()
        with uow as active_uow:
            db = active_uow.session
            return self._find_active_prompt_gateway(db).execute(self._prompt_name, owner_id)

    def _persist_ticket(self, ticket: Ticket) -> Ticket | None:
        uow = self._resolve_uow()
        with uow as active_uow:
            db = active_uow.session
            return self._update_ticket_triage_status_gateway(db).execute(ticket)

    def _apply_ticket_status(self, ticket: Ticket, status: TicketTriageStatus) -> Ticket:
        if status == TicketTriageStatus.ON_TRIAGE:
            return ticket.on_triage()
        if status == TicketTriageStatus.COMPLETED:
            return ticket.on_complete()
        if status == TicketTriageStatus.FAILED:
            return ticket.on_fail()
        return ticket

    def _render_user_prompt(self, prompt: Prompt, ticket: Ticket) -> str:
        values = {
            "title": ticket.title,
            "description": ticket.description,
            "external_id": ticket.external_id,
            "owner_id": str(ticket.owner_id),
            "language": DEFAULT_LANGUAGE,
            "customer_tier": DEFAULT_CUSTOMER_TIER,
        }
        return prompt.user_template.format(**values)

    def _normalize_output(self, output: str) -> str:
        cleaned = output.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
            cleaned = cleaned.lstrip("\n")
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
        return cleaned.strip()

    def _parse_json_output(self, output: str) -> str:
        cleaned = self._normalize_output(output)
        parsed = json.loads(cleaned)
        return json.dumps(parsed, ensure_ascii=False)

    def _ensure_json_output(self, prompt: Prompt, user_prompt: str, output: str) -> str:
        try:
            return self._parse_json_output(output)
        except Exception:
            _logger.execute(
                "warning",
                "triage_output_parse_failed_retrying",
                prompt_name=self._prompt_name,
            )
        repair_prompt = (
            "The previous assistant response is not valid JSON. "
            "Return ONLY valid JSON that matches the expected output schema. "
            "Do not include markdown, code fences, or extra text.\n\n"
            f"Output schema:\n{json.dumps(prompt.output_schema, ensure_ascii=False)}\n\n"
            f"Original response:\n{output}"
        )
        repaired = self._client.execute(
            system=prompt.system_prompt,
            user=repair_prompt,
            temperature=DEFAULT_TEMPERATURE,
            max_tokens=DEFAULT_MAX_TOKENS,
        )
        return self._parse_json_output(repaired)

    def _resolve_uow(self):
        uow = getattr(self, "uow", None)
        if uow is None:
            raise RuntimeError("UseCase sem self.uow (necessario para TriageTicketUseCase)")
        if not hasattr(uow, "__enter__") and callable(uow):
            return uow()
        return uow
