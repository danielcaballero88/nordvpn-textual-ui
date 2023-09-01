import subprocess


def nordvpn_command(cmd: list[str]) -> subprocess.CompletedProcess:
    full_cmd = ["nordvpn"] + cmd
    completed = subprocess.run(full_cmd, capture_output=True, check=False)
    return completed


def nordvpn_account() -> subprocess.CompletedProcess:
    return nordvpn_command(["account"])


def nordvpn_login() -> subprocess.CompletedProcess:
    return nordvpn_command(["login"])


def nordvpn_logout() -> subprocess.CompletedProcess:
    return nordvpn_command(["logout"])


def nordvpn_status() -> subprocess.CompletedProcess:
    return nordvpn_command(["status"])


def nordvpn_countries() -> subprocess.CompletedProcess:
    return nordvpn_command(["countries"])


def nordvpn_cities(country: str) -> subprocess.CompletedProcess:
    return nordvpn_command(["cities", country])


def nordvpn_connect(place: str) -> subprocess.CompletedProcess:
    return nordvpn_command(["connect", place])


def nordvpn_disconnect() -> subprocess.CompletedProcess:
    return nordvpn_command(["disconnect"])
