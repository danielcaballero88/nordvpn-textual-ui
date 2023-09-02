import unittest
from unittest import mock

from src.nordvpn import utils

from . import mock_commands

mock_nordvpn_command = mock.MagicMock()
mock_nordvpn_command.side_effect = ValueError(
    "This shouldn't be called, fix the tests."
)


# Mock the nordvpn_command method to ensure that no actual nordvpn shell
# command is called during tests in case of a mistake while development.
@mock.patch("src.nordvpn.commands.nordvpn_command", mock_nordvpn_command)
class UtilsTestsLoggedInAndConnected(unittest.TestCase):
    """Tests for the nordvpn.utils module."""

    @mock.patch(
        "src.nordvpn.commands.nordvpn_account",
        mock_commands.get_mock_nordvpn_account(logged_in=True),
    )
    def test_check_account_if_logged_in(self):
        """Test the check_account method when logged in."""
        result = utils.check_account()

        assert isinstance(result, dict)
        assert result.get("email") == "mock@mail.com"
        assert result.get("expiration") == "Expires on Jul 15th, 2025"

    @mock.patch(
        "src.nordvpn.commands.nordvpn_account",
        mock_commands.get_mock_nordvpn_account(logged_in=False),
    )
    def test_check_account_if_logged_out(self):
        """Test the check_account method when logged in."""
        with self.assertRaises(utils.NotLoggedInError):
            utils.check_account()
