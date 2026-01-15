from core.os.linux.linux_backend import LinuxBackend


class SystemInfo:
    @staticmethod
    def uname() -> dict:
        return LinuxBackend.run(["uname", "-a"])
