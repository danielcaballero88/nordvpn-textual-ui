"""Mocks for the commands module."""


class MockCompletedProcess:
    """Mock the subprocess.CompletedProcess class."""
    def __init__(self, stdout: bytes, returncode: int):
        self.stdout = stdout
        self.returncode = returncode


def mock_nordvpn_generic(
        output_logged_in: bytes,
        returncode_logged_in: int,
        output_logged_out: bytes,
        returncode_logged_out: int,
        logged_in: bool
) -> MockCompletedProcess:
    """Generic mock for the nordvpn commands."""
    def _mock_nordvpn_generic_logged_in():
        return MockCompletedProcess(output_logged_in, returncode_logged_in)

    def _mock_nordvpn_generic_not_logged_in():
        return MockCompletedProcess(output_logged_out, returncode_logged_out)

    if logged_in:
        return _mock_nordvpn_generic_logged_in
    else:
        return _mock_nordvpn_generic_not_logged_in


def mock_nordvpn_account(logged_in: bool):
    """Mock commands.nordvpn_account."""
    return mock_nordvpn_generic(
        output_logged_in=(
            b"\r-\r  \r\r-\r\\\r|\r/\r  \rAccount Information:\n"
            b"Email Address: danielcaballero88@gmail.com\n"
            b"VPN Service: Active (Expires on Jul 15th, 2025)\n"
        ),
        returncode_logged_in=0,
        output_logged_out=b'\r-\r  \r\r-\r  \rYou are not logged in.\n',
        returncode_logged_out=1,
        logged_in=logged_in,
    )


def mock_nordvpn_login(logged_in: bool):
    """Mock commands.nordvpn_login."""
    # For this command both cases (logged in or not) provide the same result.
    output = (
        b'\r-\r  \r\r-\r  \r\r-\r\\\r|\r  \rContinue in the browser: '
        b'https://api.nordvpn.com/v1/users/oauth/login-redirect?attempt=mock-uuid\n'
        b'\r\r'
    )
    return mock_nordvpn_generic(
        output_logged_in=output,
        returncode_logged_in=0,
        output_logged_out=output,
        returncode_logged_out=0,
        logged_in=logged_in
    )
