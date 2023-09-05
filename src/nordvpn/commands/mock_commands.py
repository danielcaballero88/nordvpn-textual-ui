"""Mocks for the commands module."""
from typing import Callable
from unittest import mock


class MockCompletedProcess:
    """Mock the subprocess.CompletedProcess class."""

    def __init__(self, stdout: bytes, returncode: int, *args, **kwargs):
        self.stdout = stdout
        self.returncode = returncode
        self.args = args
        self.kwargs = kwargs


class MockCommands:
    """Mock commands for NordVpn.

    Before using this, it needs to be instantiated and it starts with
    status logged out and disconnected. To change that, the attributes
    `logged_in` and `connected` can be set to True as desired.
    """

    def __init__(self):
        self.__logged_in = False
        self.__connected = False

    def set_connected(self, val: bool):
        """Set the status to connected True/False."""
        self.__connected = val

    def set_logged_in(self, val: bool):
        """Set the status to logged in True/False."""
        self.__logged_in = val

    def get_mock_nordvpn_generic(
        self,
        output_logged_in: bytes,
        returncode_logged_in: int,
        output_logged_out: bytes,
        returncode_logged_out: int,
    ) -> Callable[..., MockCompletedProcess]:
        """Generic mock for the nordvpn commands."""

        def _mock_nordvpn_generic_logged_in(*args, **kwargs) -> MockCompletedProcess:
            return MockCompletedProcess(
                output_logged_in, returncode_logged_in, *args, **kwargs
            )

        def _mock_nordvpn_generic_not_logged_in(
            *args, **kwargs
        ) -> MockCompletedProcess:
            return MockCompletedProcess(
                output_logged_out, returncode_logged_out, *args, **kwargs
            )

        if self.__logged_in:
            return _mock_nordvpn_generic_logged_in
        else:
            return _mock_nordvpn_generic_not_logged_in

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

            return MockCompletedProcess(
                stdout=(
                    b"\r-\r  \r\r-\r  \r"
                    b"Status: Connected\n"
                    b"Hostname: mc123.nordvpn.com\n"
                    b"IP: 123.123.123.1\n"
                    b"Country: Mock_Country\n"
                    b"City: Mock_City\n"
                    b"Current technology: NORDLYNX\n"
                    b"Current protocol: UDP\n"
                    b"Transfer: 39.91 KiB received, 48.27 KiB sent\n"
                    b"Uptime: 18 seconds\n"
                ),
                returncode=0,
            )
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
        return MockCompletedProcess(
            # fmt: off
            stdout=(
                b"\r-\r  \r\r-\r  \r"
                b"Mock_City_1\t\tMock_City_2\n"
            ),
            # fmt: on
            returncode=0,
        )

    def nordvpn_connect(self, location: str):
        assert isinstance(location, str)
        if self.__logged_in:
            return MockCompletedProcess(
                stdout=(
                    b"\r-\r  \r\r-\r\\\r  \r"
                    b"Connecting to Mock_Country #123 "
                    b"(mc123.nordvpn.com)\n"
                    b"\r-\r\\\r|\r/\r-\r\\\r  \rYou are connected to Mock_Country #123 "
                    b"(mc123.nordvpn.com)!\n"
                    b"\r-\r  \r"
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
                # fmt: on
                returncode=1,
            )

    def nordvpn_disconnect(self):
        if not self.__logged_in:
            raise ValueError("Cannot be connected if logged out.")

        if self.__connected:
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
