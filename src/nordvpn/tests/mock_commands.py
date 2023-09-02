"""Mocks for the commands module."""
from unittest.mock import MagicMock


class MockCompletedProcess:
    """Mock the subprocess.CompletedProcess class."""

    def __init__(self, stdout: bytes, returncode: int):
        self.stdout = stdout
        self.returncode = returncode


mock_nordvpn_command = MagicMock()
mock_nordvpn_command.return_value = MockCompletedProcess(b"", 0)


def get_mock_nordvpn_generic(
    output_logged_in: bytes,
    returncode_logged_in: int,
    output_logged_out: bytes,
    returncode_logged_out: int,
    logged_in: bool,
) -> MockCompletedProcess:
    """Generic mock for the nordvpn commands."""

    def _mock_nordvpn_generic_logged_in(*_args, **_kwargs):
        return MockCompletedProcess(output_logged_in, returncode_logged_in)

    def _mock_nordvpn_generic_not_logged_in(*_args, **_kwargs):
        return MockCompletedProcess(output_logged_out, returncode_logged_out)

    if logged_in:
        return _mock_nordvpn_generic_logged_in
    else:
        return _mock_nordvpn_generic_not_logged_in


def get_mock_nordvpn_account(logged_in: bool):
    """Mock commands.nordvpn_account."""
    return get_mock_nordvpn_generic(
        output_logged_in=(
            b"\r-\r  \r\r-\r\\\r|\r/\r  \r"
            b"Account Information:\n"
            b"Email Address: mock@mail.com\n"
            b"VPN Service: Active (Expires on Jul 15th, 2025)\n"
        ),
        returncode_logged_in=0,
        # fmt: off
        output_logged_out=(
            b"\r-\r  \r\r-\r  \r"
            b"You are not logged in.\n"
        ),
        # fmt: on
        returncode_logged_out=1,
        logged_in=logged_in,
    )


def get_mock_nordvpn_login(logged_in: bool):
    """Mock commands.nordvpn_login."""
    return get_mock_nordvpn_generic(
        # fmt: off
        output_logged_in=(
            b"\r-\r  \r\r-\r  \r"
            b"You are already logged in.\n"
        ),
        # fmt: on
        returncode_logged_in=1,
        output_logged_out=(
            b"\r-\r  \r\r-\r  \r\r-\r\\\r|\r  \r"
            b"Continue in the browser: "
            b"https://api.nordvpn.com/v1/users/oauth/login-redirect?attempt=mock-uuid\n"
            b"\r\r"
        ),
        returncode_logged_out=0,
        logged_in=logged_in,
    )


def get_mock_nordvpn_logout(logged_in: bool):
    """Mock commands.nordvpn_logout."""
    return get_mock_nordvpn_generic(
        # fmt: off
        output_logged_in=(
            b"\r-\r  \r\r-\r\\\r|\r/\r-\r\\\r|\r/\r  \r"
            b"You are logged out.\n"
        ),
        returncode_logged_in=0,
        output_logged_out=(
            b"\r-\r  \r\r-\r  \r"
            b"You are not logged in.\n"
        ),
        # fmt: on
        returncode_logged_out=1,
        logged_in=logged_in,
    )


def get_mock_nordvpn_status(logged_in: bool, connected: bool):
    """Mock commands.nordvpn_status."""
    if connected:
        if logged_in:
            raise ValueError("Cannot be connected while logged out.")
        return get_mock_nordvpn_generic(
            output_logged_in=(
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
            returncode_logged_in=0,
            output_logged_out=b"",  # This doesn't occur.
            returncode_logged_out=0,  # This doesn't occur.
            logged_in=logged_in,
        )
    else:  # disconnected
        return get_mock_nordvpn_generic(
            # fmt: off
            output_logged_in=(
                b"\r-\r  \r\r-\r  \r"
                b"Status: Disconnected\n"
            ),
            returncode_logged_in=0,
            output_logged_out=(
                b"\r-\r  \r\r-\r  \r"
                b"Status: Disconnected\n"
            ),
            # fmt: on
            returncode_logged_out=0,
            logged_in=logged_in,
        )


def get_mock_nordvpn_countries(logged_in: bool):
    """Mock commands.nordvpn_countries."""
    output = (
        b"\r-\r  \r\r-\r  \r"
        b"Albania\t\t\tBulgaria\t\tCzech_Republic\t\tGreece\t\t\t"
        b"Italy\t\t\tMoldova\t\t\tRomania\t\t\tSpain\t\t\tUnited_Kingdom\nArgentina"
        b"\t\tCanada\t\t\tDenmark\t\t\tHong_Kong\t\tJapan\t\t\tNetherlands\t\t"
        b"Serbia\t\t\tSweden\t\t\tUnited_States\nAustralia\t\tChile\t\t\tEstonia"
        b"\t\t\tHungary\t\t\tLatvia\t\t\tNew_Zealand\t\tSingapore\t\tSwitzerland"
        b"\t\tVietnam\nAustria\t\t\tColombia\t\tFinland\t\t\tIceland\t\t\tLithuania"
        b"\t\tNorth_Macedonia\t\tSlovakia\t\tTaiwan\nBelgium\t\t\tCosta_Rica\t\t"
        b"France\t\t\tIndonesia\t\tLuxembourg\t\tNorway\t\t\tSlovenia\t\tThailand\n"
        b"Bosnia_And_Herzegovina\tCroatia\t\t\tGeorgia\t\t\tIreland\t\t\tMalaysia\t"
        b"\tPoland\t\t\tSouth_Africa\t\tTurkey\nBrazil\t\t\tCyprus\t\t\tGermany\t\t"
        b"\tIsrael\t\t\tMexico\t\t\tPortugal\t\tSouth_Korea\t\tUkraine\n"
    )
    return get_mock_nordvpn_generic(
        output_logged_in=output,
        returncode_logged_in=0,
        output_logged_out=output,
        returncode_logged_out=0,
        logged_in=logged_in,
    )


def get_mock_nordvpn_cities(logged_in: bool):
    """Mock commands.nordvpn_cities for a made up country."""
    # fmt: off
    output = (
        b"\r-\r  \r\r-\r  \r"
        b"Mock_City_1\t\tMock_City_2\n"
    )
    # fmt: on
    return get_mock_nordvpn_generic(
        output_logged_in=output,
        returncode_logged_in=0,
        output_logged_out=output,
        returncode_logged_out=0,
        logged_in=logged_in,
    )


def get_mock_nordvpn_connect(logged_in: bool):
    """Mock commands.nordvpn_connect for a made up country."""
    return get_mock_nordvpn_generic(
        output_logged_in=(
            b"\r-\r  \r\r-\r\\\r  \r"
            b"Connecting to Mock_Country #123 "
            b"(mc123.nordvpn.com)\n"
            b"\r-\r\\\r|\r/\r-\r\\\r  \rYou are connected to Mock_Country #123 "
            b"(mc123.nordvpn.com)!\n"
            b"\r-\r  \r"
        ),
        returncode_logged_in=0,
        # fmt: off
        output_logged_out=(
            b"\r-\r  \r\r-\r  \r"
            b"You are not logged in.\n"
        ),
        # fmt: on
        returncode_logged_out=1,
        logged_in=logged_in,
    )


def get_mock_nordvpn_disconnect(logged_in: bool):
    """Mock commands.nordvpn_disconnect for a made up country."""
    return get_mock_nordvpn_generic(
        output_logged_in=(
            b"\r-\r  \r\r-\r\\\r|\r/\r  \r"
            b"You are disconnected from NordVPN.\n"
            b"How would you rate your connection quality on a scale from 1 (poor) to 5 "
            b"(excellent)? Type 'nordvpn rate [1-5]'.\n"
            b"\r\r"
        ),
        returncode_logged_in=0,
        # fmt: off
        output_logged_out=(
            b"\r-\r  \r\r-\r  \r"
            b"You are not connected to NordVPN.\n\r\r"
        ),
        # fmt: on
        returncode_logged_out=0,
        logged_in=logged_in,
    )
