import os
import subprocess
import platform
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class SystemActions:
    """
    Day 50 — OS Adapter Layer
    - NO permissions
    - NO intent logic
    - NO policy decisions
    - Pure side-effect executors
    """

    def __init__(self, config=None):
        self.config = config
        self.system = platform.system()
        self.last_action = None
        self.last_args = None

    # =====================================================
    # 🟦 DAY 50 — OPEN APP (PRIMARY)
    # =====================================================
    def open_app(self, app_name: str, target: str = None) -> Dict[str, Any]:
        try:
            if not app_name:
                return {"success": False, "message": "No app name provided"}

            if self.system == "Linux":
                subprocess.Popen([app_name.lower()])

            elif self.system == "Windows":
                subprocess.Popen([app_name], shell=True)

            elif self.system == "Darwin":
                subprocess.Popen(["open", "-a", app_name])

            self._store_last("open_app", {"app_name": app_name})

            return {
                "success": True,
                "message": f"Opening {app_name}",
                "app": app_name,
            }

        except Exception as e:
            logger.error(e)
            return {
                "success": False,
                "message": f"Failed to open {app_name}",
            }

    # =====================================================
    # 🟦 DAY 50 — SYSTEM INFO (READ-ONLY)
    # =====================================================
    def system_info(self) -> Dict[str, Any]:
        try:
            info = {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
            }

            self._store_last("system_info", {})

            return {
                "success": True,
                "message": "System information retrieved",
                "info": info,
            }

        except Exception as e:
            logger.error(e)
            return {
                "success": False,
                "message": "Failed to retrieve system info",
            }

    # =====================================================
    # LEGACY HELPERS (SAFE / NON-CRITICAL)
    # =====================================================
    def open_terminal(self, command: str = None, target: str = None) -> Dict[str, Any]:
        try:
            if self.system == "Linux":
                if command:
                    subprocess.Popen(
                        ["gnome-terminal", "--", "bash", "-c", f"{command}; exec bash"]
                    )
                else:
                    subprocess.Popen(["gnome-terminal"])

            elif self.system == "Windows":
                subprocess.Popen(["cmd.exe"])

            elif self.system == "Darwin":
                subprocess.Popen(["open", "-a", "Terminal"])

            self._store_last("open_terminal", {"command": command})

            return {"success": True, "message": "Terminal opened"}

        except Exception as e:
            logger.error(e)
            return {"success": False, "message": "Failed to open terminal"}

    def open_file_manager(self, path: str = None, target: str = None) -> Dict[str, Any]:
        try:
            if not path:
                path = os.path.expanduser("~")

            if self.system == "Linux":
                subprocess.Popen(["nautilus", path])
            elif self.system == "Windows":
                os.startfile(path)
            elif self.system == "Darwin":
                subprocess.Popen(["open", path])

            self._store_last("open_file_manager", {"path": path})

            return {"success": True, "message": f"Opening {path}"}

        except Exception as e:
            logger.error(e)
            return {"success": False, "message": "Failed to open file manager"}

    def list_files(self, path: str = None, target: str = None) -> Dict[str, Any]:
        try:
            if not path:
                path = os.getcwd()

            files = os.listdir(path)

            self._store_last("list_files", {"path": path})

            return {
                "success": True,
                "message": f"Files in {path}",
                "files": files,
            }

        except Exception as e:
            logger.error(e)
            return {"success": False, "message": "Failed to list files"}

    # =====================================================
    # CONTEXT
    # =====================================================
    def _store_last(self, action: str, args: Dict[str, Any]):
        self.last_action = action
        self.last_args = args

    def get_last_action(self):
        return self.last_action, self.last_args


# =========================================================
# 🟦 DAY 50 — SKILL ENTRY POINTS (FUNCTION WRAPPERS)
# =========================================================

_system_actions = SystemActions()


def open_app(args: Dict[str, Any]):
    """
    Canonical system skill entry point for OPEN_APP.

    Expected args:
    {
        "app_name": "chrome"
    }
    """
    app_name = args.get("app_name")

    if not app_name:
        return {"success": False, "message": "Missing app_name"}

    return _system_actions.open_app(app_name=app_name)
