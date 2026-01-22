TICKET_EXCEPTION: dict[str, dict[str, str]] = {
    "ALREADY_EXISTS": {"code": "TI-001", "message": "Ticket {external_id} already exists"},
    "INVALID_STATUS_CHANGE": {"code": "TI-002", "message": "Cannot change ticket triage status from {actual_status} to {new_status}"},
    "TICKET_ALREADY_EXISTS": {"code": "TI-003", "message": "Ticket {id} triage job {triage_job_id} already exists"},
}
