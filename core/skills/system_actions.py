import webbrowser
import os
import subprocess
import platform
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class SystemActions:
    def __init__(self, config=None):
        self.config = config
        self.system = platform.system()
        self.last_action = None
        self.last_args = None

    # ---------- BROWSER ----------

    def open_browser(self, url: str = None, target: str = None) -> Dict[str, Any]:
        try:
            if not url:
                url = "https://google.com"

            webbrowser.open(url)

            self._store_last("open_browser", {"url": url, "target": target})

            return {
                "success": True,
                "message": f"Opening {target or url}",
                "url": url
            }

        except Exception as e:
            logger.error(e)
            return {
                "success": False,
                "message": "Failed to open browser"
            }

    # ---------- TERMINAL ----------

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

            return {
                "success": True,
                "message": "Terminal opened",
                "command": command
            }

        except Exception as e:
            logger.error(e)
            return {
                "success": False,
                "message": "Failed to open terminal"
            }

    # ---------- FILE MANAGER ----------

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

            return {
                "success": True,
                "message": f"Opening {target or path}",
                "path": path
            }

        except Exception as e:
            logger.error(e)
            return {
                "success": False,
                "message": "Failed to open file manager"
            }

    # ---------- SEARCH ----------

    def search_web(self, query: str = None, target: str = None) -> Dict[str, Any]:
        try:
            if not query:
                return {
                    "success": False,
                    "message": "What should I search for?"
                }

            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(url)

            self._store_last("search_web", {"query": query})

            return {
                "success": True,
                "message": f"Searching for {query}",
                "url": url
            }

        except Exception as e:
            logger.error(e)
            return {
                "success": False,
                "message": "Search failed"
            }

    # ---------- FILE OPEN ----------

    def open_file(self, filename: str = None, full_path: str = None, target: str = None) -> Dict[str, Any]:
        try:
            path = full_path

            if not path and filename:
                for base in ["~/Downloads", "~/Desktop", "~/Documents"]:
                    test = os.path.expanduser(f"{base}/{filename}")
                    if os.path.exists(test):
                        path = test
                        break

            if not path:
                return {
                    "success": False,
                    "message": "File not found"
                }

            if self.system == "Linux":
                subprocess.Popen(["xdg-open", path])
            elif self.system == "Windows":
                os.startfile(path)
            elif self.system == "Darwin":
                subprocess.Popen(["open", path])

            self._store_last("open_file", {"path": path})

            return {
                "success": True,
                "message": f"Opening {os.path.basename(path)}",
                "path": path
            }

        except Exception as e:
            logger.error(e)
            return {
                "success": False,
                "message": "Failed to open file"
            }

    # ---------- LIST FILES ----------

    def list_files(self, path: str = None, target: str = None) -> Dict[str, Any]:
        try:
            if not path:
                path = os.getcwd()

            files = os.listdir(path)

            self._store_last("list_files", {"path": path})

            return {
                "success": True,
                "message": f"Files in {path}",
                "files": files
            }

        except Exception as e:
            logger.error(e)
            return {
                "success": False,
                "message": "Failed to list files"
            }

    # ---------- CONTEXT ----------

    def _store_last(self, action: str, args: Dict[str, Any]):
        self.last_action = action
        self.last_args = args

    def get_last_action(self):
        return self.last_action, self.last_args
