import unittest
from unittest.mock import patch

from src.nordvpn import commands

from . import mock_commands


class CommandsTests(unittest.TestCase):
    """Test cases for the nordvpn commands.

    These commands are the most basic components, just functions that call the shell
    commands of nordvpn and return the completed process with piped output.
    By replacing each of these functions with a mock, nothing is really being tested
    there, but it's just a way to test the mocks in a very basic way.
    """
    def test_nordvpn_account(self):
        """Test the nordvpn_account command mock."""
        with patch(
            "src.nordvpn.commands.nordvpn_account",
            mock_commands.mock_nordvpn_account(logged_in=True)
        ):
            completed_process = commands.nordvpn_account()
            expected_output = (
                b"\r-\r  \r\r-\r\\\r|\r/\r  \rAccount Information:\n"
                b"Email Address: danielcaballero88@gmail.com\n"
                b"VPN Service: Active (Expires on Jul 15th, 2025)\n"
            )
            assert completed_process.stdout == expected_output
            assert completed_process.returncode == 0

        with patch(
            "src.nordvpn.commands.nordvpn_account",
            mock_commands.mock_nordvpn_account(logged_in=False)
        ):
            completed_process = commands.nordvpn_account()
            expected_output = b'\r-\r  \r\r-\r  \rYou are not logged in.\n'
            assert completed_process.stdout == expected_output
            assert completed_process.returncode == 1

    def test_nordvpn_login(self):
        """Test the nordvpn_account command mock."""
        with patch(
            "src.nordvpn.commands.nordvpn_login",
            mock_commands.mock_nordvpn_login(logged_in=True)
        ):
            completed_process = commands.nordvpn_login()
            expected_output = (
                b'\r-\r  \r\r-\r  \r\r-\r\\\r|\r  \rContinue in the browser: '
                b'https://api.nordvpn.com/v1/users/oauth/login-redirect?attempt=mock-uuid\n'
                b'\r\r'
            )
            assert completed_process.stdout == expected_output
            assert completed_process.returncode == 0

        with patch(
            "src.nordvpn.commands.nordvpn_login",
            mock_commands.mock_nordvpn_login(logged_in=False)
        ):
            completed_process = commands.nordvpn_login()
            expected_output = (
                b'\r-\r  \r\r-\r  \r\r-\r\\\r|\r  \rContinue in the browser: '
                b'https://api.nordvpn.com/v1/users/oauth/login-redirect?attempt=mock-uuid\n'
                b'\r\r'
            )
            assert completed_process.stdout == expected_output
            assert completed_process.returncode == 0
