# core/terminal/abort_conditions.py

class AbortReason:
    INTERRUPT = "global_interrupt"
    TIMEOUT = "timeout"
    SPEC_MISMATCH = "spec_mismatch"
    USER_ABORT = "user_abort"
