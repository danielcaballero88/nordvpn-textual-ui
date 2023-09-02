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

    def test_check_account(self):
        """Test the utils.check_account method."""
        with mock.patch(
            "src.nordvpn.commands.nordvpn_account",
            mock_commands.get_mock_nordvpn_account(logged_in=True),
        ):
            result = utils.check_account()
            assert isinstance(result, dict)
            assert result.get("email") == "mock@mail.com"
            assert result.get("expiration") == "Expires on Jul 15th, 2025"

        with mock.patch(
            "src.nordvpn.commands.nordvpn_account",
            mock_commands.get_mock_nordvpn_account(logged_in=False),
        ):
            with self.assertRaises(utils.NotLoggedInError):
                utils.check_account()

    def test_is_logged_in_if_logged_in(self):
        """Test the utils.is_logged_in method."""
        with mock.patch(
            "src.nordvpn.commands.nordvpn_account",
            mock_commands.get_mock_nordvpn_account(logged_in=True),
        ):
            is_logged_in = utils.is_logged_in()
            assert isinstance(is_logged_in, bool)
            assert is_logged_in

        with mock.patch(
            "src.nordvpn.commands.nordvpn_account",
            mock_commands.get_mock_nordvpn_account(logged_in=False),
        ):
            is_logged_in = utils.is_logged_in()
            assert isinstance(is_logged_in, bool)
            assert not is_logged_in
