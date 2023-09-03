import re

from .commands.commands import NordvpnCommands
from .commands.mock_commands import MockCommands
from .exceptions import NotLoggedInError, NotLoggedOutError


class NordvpnBase:
    """Class to interact with the nordvpn cli and keep track of status."""

    def __init__(self, test=False):
        self.test = test
        if test:
            self.cmds = MockCommands()
        else:
            self.cmds = NordvpnCommands()

    def check_account(self) -> dict[str, str]:
        """Run nordvpn account.

        This function is used to check if it is currently logged in by the wrapper function
        is_logged_in, so do not require being logged in within this one or there will be an
        infinite recursion.
        """
        # Initialize result
        result = {
            "email": None,
            "expiration": None,
        }
        completed = self.cmds.nordvpn_account()
        output = completed.stdout.decode("utf-8").replace("\r", "")
        if "not logged in" in output:
            raise NotLoggedInError()

        def _extract_email(_line: str) -> str | None:
            if not _line.startswith("Email"):
                return None
            re_match = re.search(r":\s*(\w+?@\w+?\.com)", _line)
            if not re_match:
                raise ValueError("Couldn't extract email with regex.")
            email = re_match.groups()[0]
            return email

        def _extract_expiration(_line: str) -> str | None:
            if not _line.startswith("VPN Service"):
                return None
            re_match = re.search(r"Active \((.+?)\)", _line)
            if not re_match:
                raise ValueError("Couldn't extract expire date with regex.")
            expiration = re_match.groups()[0]
            return expiration

        lines = output.split("\n")
        for line in lines:
            if _email := _extract_email(line):
                result["email"] = _email
            if _expiration := _extract_expiration(line):
                result["expiration"] = _expiration

        return result

    def is_logged_in(self) -> bool:
        try:
            self.check_account()
        except Exception as exc:
            print(exc)
            return False
        else:
            return True

    def login_required(self, func_name: str) -> None:
        """Check for logged in status."""
        if not self.is_logged_in():
            msg = f"function {func_name} requires to be logged in."
            raise NotLoggedInError(msg)

    def logout_required(self, func_name: str) -> None:
        """Check for logged in status."""
        if self.is_logged_in():
            msg = f"function {func_name} requires to be logged out."
            raise NotLoggedOutError(msg)

    def run_logout(self) -> str:
        self.login_required("run_logout")
        completed = self.cmds.nordvpn_logout()
        if completed.returncode != 0:
            raise ValueError(f"nordvpn_logout returned code {completed.returncode}")
        output = completed.stdout.decode("utf-8")
        return output

    def run_login(self) -> str:
        self.logout_required("run_login")
        completed = self.cmds.nordvpn_login()
        if completed.returncode != 0:
            raise ValueError(f"nordvpn_login returned ccode {completed.returncode}")
        output = completed.stdout.decode("utf-8")
        return output

    def get_status(self) -> dict[str, str | None]:
        self.login_required("get_status")
        result = {
            "Status": None,
            "Country": None,
            "City": None,
            "IP": None,
            "Uptime": None,
        }
        completed = self.cmds.nordvpn_status()
        output = completed.stdout.decode("utf-8")
        output = output.replace("\r", "")
        lines = output.split("\n")
        for line in lines:
            re_match = re.search(r"(\w+?):\s*([\w\s.]+)$", line)
            if re_match:
                key, val = re_match.groups()
                if key in result:
                    result[key] = val
        return result

    def get_countries(self) -> list[str]:
        self.login_required("get_countries")
        completed = self.cmds.nordvpn_countries()
        result = completed.stdout.decode("utf-8")
        result = result.replace("\r", "").replace("\n", "\t")
        result = re.sub("\t+", ";", result)
        result = result.split(";")
        countries = []
        for country_raw in result:
            re_match = re.search(r"(\w+)", country_raw)
            if re_match:
                countries.append(re_match.groups()[0])
        return countries

    def get_cities(self, country: str) -> list[str]:
        self.login_required("get_cities")
        completed = self.cmds.nordvpn_cities(country)
        result = completed.stdout.decode("utf-8")
        result = result.replace("\r", "").replace("\n", "\t")
        result = re.sub("\t+", ";", result)
        result = result.split(";")
        cities = []
        for country_raw in result:
            re_match = re.search(r"(\w+)", country_raw)
            if re_match:
                cities.append(re_match.groups()[0])
        return cities

    def connect_to_location(self, location: str) -> str:
        self.login_required("connect_to_location")
        completed = self.cmds.nordvpn_connect(location)
        output: str = completed.stdout.decode("utf-8")
        output = output.replace("\r", "")
        return output

    def disconnect_from_nordvpn(self) -> str:
        self.login_required("disconnect_from_nordvpn")
        completed = self.cmds.nordvpn_disconnect()
        output: str = completed.stdout.decode("utf-8")
        output = output.replace("\r", "")
        return output
