from core.os.linux.linux_backend import LinuxBackend


class Screenshot:
    @staticmethod
    def take(path: str) -> dict:
        # Requires scrot installed
        return LinuxBackend.run(["scrot", path])
