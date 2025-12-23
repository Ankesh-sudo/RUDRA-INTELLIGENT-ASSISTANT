from loguru import logger
from core.system.executor import SystemExecutor


class AppRegistry:
    def __init__(self):
        self.executor = SystemExecutor()
        self._actions = {
            "browser": self.executor.open_browser,
            "terminal": self.executor.open_terminal,
            "file_manager": self.executor.open_file_manager,
            "calculator": lambda: self._run("gnome-calculator"),
            "vscode": lambda: self._run("code"),
        }

    def _run(self, cmd: str) -> bool:
        try:
            import subprocess
            subprocess.Popen([cmd])
            return True
        except Exception as e:
            logger.error("Failed to run {}: {}", cmd, e)
            return False

    def execute(self, app_name: str) -> bool:
        action = self._actions.get(app_name)
        if not action:
            return False
        return bool(action())
