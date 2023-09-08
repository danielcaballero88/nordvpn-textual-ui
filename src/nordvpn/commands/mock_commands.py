"""Mocks for the commands module."""
from typing import Callable
from unittest import mock

MOCK_COUNTRIES = {
    "Mock_Country_1": ["Mock_City_1_1", "Mock_City_1_2"],
    "Mock_Country_2": ["Mock_City_2_1", "Mock_City_2_2"],
    "Mock_Country_3": ["Mock_City_3_1", "Mock_City_3_2"],
    "Mock_Country_4": ["Mock_City_4_1", "Mock_City_4_2"],
}

MOCK_CITIES = {}
for _country, _cities in MOCK_COUNTRIES.items():
    for _city in _cities:
        MOCK_CITIES[_city] = _country


class MockCompletedProcess:
    """Mock the subprocess.CompletedProcess class."""

    def __init__(self, stdout: bytes, returncode: int, *args, **kwargs):
        self.stdout = stdout
        self.returncode = returncode
        self.args = args
        self.kwargs = kwargs


class MockNordvpnCommands:
    """Mock commands for NordVpn.

    Before using this, it needs to be instantiated and it starts with
    status logged out and disconnected. To change that, the attributes
    `logged_in` and `connected` can be set to True as desired.
    """

    def __init__(self):
        self.__logged_in = False
        self.__connected = False
        self.__connected_country = None
        self.__connected_city = None

    def __set_connected(
        self, val: bool, country: str | None = None, city: str | None = None
    ):
        if val:
            assert country in MOCK_COUNTRIES
            assert city in MOCK_CITIES
        else:  # False
            assert country is None
            assert city is None

        self.__connected = val
        self.__connected_country = country
        self.__connected_city = city

    # Mock the base nordvpn_command with a MagicMock. I only need to
    # check that this method was ever called/not called for tests.
    nordvpn_command = mock.MagicMock()
    nordvpn_command.return_value = MockCompletedProcess(b"", 0)

    def nordvpn_account(self):
        if self.__logged_in:
            return MockCompletedProcess(
                stdout=(
                    b"\r-\r  \r\r-\r\\\r|\r/\r  \r"
                    b"Account Information:\n"
                    b"Email Address: mock@mail.com\n"
                    b"VPN Service: Active (Expires on Jul 15th, 2025)\n"
                ),
                returncode=0,
            )
        else:  # not logged in
            return MockCompletedProcess(
                # fmt: off
                stdout=(
                    b"\r-\r  \r\r-\r  \r"
                    b"You are not logged in.\n"
                ),
                # fmt: on,
                returncode=1,
            )

    def nordvpn_login(self):
        if self.__logged_in:
            return MockCompletedProcess(
                # fmt: off
                stdout=(
                    b"\r-\r  \r\r-\r  \r"
                    b"You are already logged in.\n"
                ),
                # fmt: on,
                returncode=1,
            )
        else:  # not logged in
            self.__logged_in = True
            return MockCompletedProcess(
                stdout=(
                    b"\r-\r  \r\r-\r  \r\r-\r\\\r|\r  \r"
                    b"Continue in the browser: "
                    b"https://api.nordvpn.com/v1/users/oauth/login-redirect?attempt=mock-uuid\n"
                    b"\r\r"
                ),
                returncode=0,
            )

    def nordvpn_logout(self):
        if self.__logged_in:
            self.__logged_in = False
            self.__set_connected(False)
            return MockCompletedProcess(
                # fmt: off
                stdout=(
                    b"\r-\r  \r\r-\r\\\r|\r/\r-\r\\\r|\r/\r  \r"
                    b"You are logged out.\n"
                ),
                # fmt: on
                returncode=0,
            )
        else:  # not logged in
            return MockCompletedProcess(
                # fmt: off
                stdout=(
                    b"\r-\r  \r\r-\r  \r"
                    b"You are not logged in.\n"
                ),
                # fmt: on
                returncode=1,
            )

    def nordvpn_status(self):
        if self.__connected:
            if not self.__logged_in:
                raise ValueError("Cannot be connected while logged out.")

            stdout = (
                b"\r-\r  \r\r-\r  \r"
                b"Status: Connected\n"
                b"Hostname: mc123.nordvpn.com\n"
                b"IP: 123.123.123.1\n"
            )
            stdout += f"Country: {self.__connected_country}\n".encode()
            stdout += f"City: {self.__connected_city}\n".encode()
            stdout += (
                b"Current technology: NORDLYNX\n"
                b"Current protocol: UDP\n"
                b"Transfer: 39.91 KiB received, 48.27 KiB sent\n"
                b"Uptime: 18 seconds\n"
            )
            return MockCompletedProcess(stdout=stdout, returncode=0)
        else:  # not connected
            # Logged in or not, the result is the same.
            return MockCompletedProcess(
                # fmt: off
                stdout=(
                    b"\r-\r  \r\r-\r  \r"
                    b"Status: Disconnected\n"
                ),
                # fmt: on
                returncode=0,
            )

    def nordvpn_countries(self):
        return MockCompletedProcess(
            # fmt: off
            stdout=(
                b"\r-\r  \r\r-\r  \r"
                b"Mock_Country_1\t\t"
                b"Mock_Country_2\t\t"
                b"Mock_Country_3\t\t\t"
                b"Mock_Country_4\n"
            ),
            # fmt: on
            returncode=0,
        )

    def nordvpn_cities(self, country: str):
        assert isinstance(country, str)
        cities = MOCK_COUNTRIES[country]
        cities_bytes = "\t\t".join(cities).encode()
        return MockCompletedProcess(
            # fmt: off
            stdout=(
                b"\r-\r  \r\r-\r  \r"
                + cities_bytes
                +b"\n"
            ),
            # fmt: on
            returncode=0,
        )

    def nordvpn_connect(self, location: str):
        assert isinstance(location, str)
        if location in MOCK_COUNTRIES:
            country = location
            city = MOCK_COUNTRIES[country][0]
        elif location in MOCK_CITIES:
            city = location
            country = MOCK_CITIES[city]
        else:
            raise ValueError(
                f"Bad value for location: {location}. Not country nor city"
            )

        if self.__logged_in:
            stdout = (
                b"\r-\r  \r\r-\r\\\r  \r"
                + f"Connecting to {country} #123 ".encode()
                + b"(mc123.nordvpn.com)\n"
                + f"\r-\r\\\r|\r/\r-\r\\\r  \rYou are connected to {country} #123 ".encode()
                + b"(mc123.nordvpn.com)!\n"
                b"\r-\r  \r"
            )
            self.__set_connected(True, country, city)
            return MockCompletedProcess(stdout=stdout, returncode=0)
        else:  # not logged in
            return MockCompletedProcess(
                # fmt: off
                stdout=(
                    b"\r-\r  \r\r-\r  \r"
                    b"You are not logged in.\n"
                ),
                # fmt: on
                returncode=1,
            )

    def nordvpn_disconnect(self):
        if not self.__logged_in:
            raise ValueError("Cannot be connected if logged out.")

        if self.__connected:
            self.__set_connected(False)
            return MockCompletedProcess(
                stdout=(
                    b"\r-\r  \r\r-\r\\\r|\r/\r  \r"
                    b"You are disconnected from NordVPN.\n"
                    b"How would you rate your connection quality on a scale from 1 (poor) to 5 "
                    b"(excellent)? Type 'nordvpn rate [1-5]'.\n"
                    b"\r\r"
                ),
                returncode=0,
            )
        else:  # not connected
            return MockCompletedProcess(
                stdout=(
                    b"\r-\r  \r\r-\r  \r" b"You are not connected to NordVPN.\n\r\r"
                ),
                # fmt: on
                returncode=0,
            )
