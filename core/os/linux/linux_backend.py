import os
import shutil
import subprocess
from typing import List


class LinuxBackend:
    """
    Linux execution backend.

    Responsibilities:
    - Execute validated OS-level actions
    - NO intent logic
    - NO permission logic
    - NO NLP
    """

    @staticmethod
    def run(cmd: List[str], timeout: int = 5) -> dict:
        """
        Execute a Linux action safely.

        Supports:
        - Executables (e.g. code, nautilus)
        - URLs (https://...)
        - Directories (/home/user/Downloads)
        - Shell commands (explicit list only)
        """

        try:
            if not cmd or not isinstance(cmd, list):
                return LinuxBackend._error("Invalid command format")

            target = cmd[0]

            # -------------------------------------------------
            # 1️⃣ EXECUTABLE (installed binary)
            # -------------------------------------------------
            if shutil.which(target):
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                return LinuxBackend._ok(process)

            # -------------------------------------------------
            # 2️⃣ URL (http / https)
            # -------------------------------------------------
            if target.startswith(("http://", "https://")):
                process = subprocess.Popen(
                    ["xdg-open", target],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                return LinuxBackend._ok(process)

            # -------------------------------------------------
            # 3️⃣ DIRECTORY PATH
            # -------------------------------------------------
            expanded = os.path.expanduser(target)
            if os.path.isdir(expanded):
                process = subprocess.Popen(
                    ["xdg-open", expanded],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                return LinuxBackend._ok(process)

            # -------------------------------------------------
            # 4️⃣ FILE PATH
            # -------------------------------------------------
            if os.path.isfile(expanded):
                process = subprocess.Popen(
                    ["xdg-open", expanded],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                return LinuxBackend._ok(process)

            # -------------------------------------------------
            # ❌ UNKNOWN TARGET
            # -------------------------------------------------
            return LinuxBackend._error(f"Unknown executable or path: {target}")

        except Exception as e:
            return LinuxBackend._error(str(e))

    # -------------------------------------------------
    # INTERNAL HELPERS
    # -------------------------------------------------
    @staticmethod
    def _ok(process: subprocess.Popen) -> dict:
        return {
            "ok": True,
            "stdout": "",
            "stderr": "",
            "code": 0,
            "pid": process.pid,
        }

    @staticmethod
    def _error(message: str) -> dict:
        return {
            "ok": False,
            "stdout": "",
            "stderr": message,
            "code": -1,
        }
