import subprocess


class NordvpnCommands:
    """Commands to interact with the nordvpn cli.

    It's contained within a class so it's easier to mock for tests, this
    way all commands can be mocked at once easily.
    """

    def nordvpn_command(self, cmd: list[str]) -> subprocess.CompletedProcess:
        """Generic nordvpn command."""
        full_cmd = ["nordvpn"] + cmd
        completed = subprocess.run(full_cmd, capture_output=True, check=False)
        return completed

    def nordvpn_account(self) -> subprocess.CompletedProcess:
        return self.nordvpn_command(["account"])

    def nordvpn_login(self) -> subprocess.CompletedProcess:
        return self.nordvpn_command(["login"])

    def nordvpn_logout(self) -> subprocess.CompletedProcess:
        return self.nordvpn_command(["logout"])

    def nordvpn_status(self) -> subprocess.CompletedProcess:
        return self.nordvpn_command(["status"])

    def nordvpn_countries(self) -> subprocess.CompletedProcess:
        return self.nordvpn_command(["countries"])

    def nordvpn_cities(self, country: str) -> subprocess.CompletedProcess:
        return self.nordvpn_command(["cities", country])

    def nordvpn_connect(self, place: str) -> subprocess.CompletedProcess:
        return self.nordvpn_command(["connect", place])

    def nordvpn_disconnect(self) -> subprocess.CompletedProcess:
        return self.nordvpn_command(["disconnect"])


commands = NordvpnCommands()
