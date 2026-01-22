TRIAGE_JOB_EXCEPTION: dict[str, dict[str, str]] = {
    "NEGATIVE_ATTEMPTS": {"code": "TJ-001", "message": "Triage job attempts should not be negative"},
    "INVALID_STATUS_CHANGE": {"code": "TI-002", "message": "Cannot change triage job status from {actual_status} to {new_status}"},
}
