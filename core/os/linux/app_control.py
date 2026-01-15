from core.os.linux.linux_backend import LinuxBackend


class AppControl:
    @staticmethod
    def open_app(app_name: str) -> dict:
        return LinuxBackend.run([app_name])
