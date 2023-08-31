"""Mocks for the commands module."""


class MockCompletedProcess:
    """Mock the subprocess.CompletedProcess class."""
    def __init__(self, stdout: bytes, returncode: int):
        self.stdout = stdout
        self.returncode = returncode


def mock_nordvpn_account(logged_in: bool):
    """Mock commands.nordvpn_account."""
    def _mock_nordvpn_account_logged_in():
        output = (
            b"\r-\r  \r\r-\r\\\r|\r/\r  \rAccount Information:\n"
            b"Email Address: danielcaballero88@gmail.com\n"
            b"VPN Service: Active (Expires on Jul 15th, 2025)\n"
        )
        return MockCompletedProcess(output, 0)

    def _mock_nordvpn_account_not_logged_in():
        output = b'\r-\r  \r\r-\r  \rYou are not logged in.\n'
        return MockCompletedProcess(output, 1)

    if logged_in:
        return _mock_nordvpn_account_logged_in
    else:
        return _mock_nordvpn_account_not_logged_in
