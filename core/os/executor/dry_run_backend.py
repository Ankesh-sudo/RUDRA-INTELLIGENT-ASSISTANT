class DryRunBackend:
    """
    Fake backend used during dry-run mode.
    Never touches the operating system.
    """

    def run(self):
        return {
            "status": "DRY_RUN",
            "message": "This action was not executed.",
        }
