import subprocess
from typing import List


class LinuxBackend:
    @staticmethod
    def run(cmd: List[str], timeout: int = 5) -> dict:
        try:
            completed = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
            return {
                "ok": completed.returncode == 0,
                "stdout": completed.stdout.strip(),
                "stderr": completed.stderr.strip(),
                "code": completed.returncode,
            }
        except Exception as e:
            return {
                "ok": False,
                "stdout": "",
                "stderr": str(e),
                "code": -1,
            }
