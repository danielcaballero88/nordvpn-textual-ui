import unittest
from unittest import mock

from src.nordvpn import utils

from . import mock_commands

mock_nordvpn_command = mock.MagicMock()
mock_nordvpn_command.side_effect = ValueError(
    "nordvpn_command was called, fix the mocks."
)


# Mock the nordvpn_command method to ensure that no actual nordvpn shell
# command is called during tests in case of a mistake while development.
@mock.patch("src.nordvpn.commands.nordvpn_command", mock_nordvpn_command)
class UtilsTestsLoggedIn(unittest.TestCase):
    """Tests for the nordvpn.utils module when logged in."""

    @mock.patch(
        "src.nordvpn.commands.nordvpn_account",
        mock_commands.get_mock_nordvpn_account(logged_in=True),
    )
    def test_check_account(self):
        """Test the utils.check_account method."""
        result = utils.check_account()
        assert isinstance(result, dict)
        assert result.get("email") == "mock@mail.com"
        assert result.get("expiration") == "Expires on Jul 15th, 2025"

    @mock.patch(
        "src.nordvpn.commands.nordvpn_account",
        mock_commands.get_mock_nordvpn_account(logged_in=True),
    )
    def test_is_logged(self):
        """Test the utils.is_logged_in method."""
        is_logged_in = utils.is_logged_in()
        assert isinstance(is_logged_in, bool)
        assert is_logged_in

    @mock.patch.multiple(
        "src.nordvpn.commands",
        nordvpn_account=mock_commands.get_mock_nordvpn_account(logged_in=True),
        nordvpn_logout=mock_commands.get_mock_nordvpn_logout(logged_in=True),
    )
    def test_run_logout(self):
        """Test the utils.run_logout function."""
        output = utils.run_logout()
        assert "you are logged out" in output.lower()

    @mock.patch.multiple(
        "src.nordvpn.commands",
        nordvpn_account=mock_commands.get_mock_nordvpn_account(logged_in=True),
        nordvpn_login=mock_commands.get_mock_nordvpn_login(logged_in=True),
    )
    def test_run_login(self):
        """Test the utils.run_login function."""
        with self.assertRaises(utils.NotLoggedOutError):
            utils.run_login()


# Mock the nordvpn_command method to ensure that no actual nordvpn shell
# command is called during tests in case of a mistake while development.
@mock.patch("src.nordvpn.commands.nordvpn_command", mock_nordvpn_command)
class UtilsTestsLoggedOut(unittest.TestCase):
    """Tests for the nordvpn.utils module when logged in."""

    @mock.patch(
        "src.nordvpn.commands.nordvpn_account",
        mock_commands.get_mock_nordvpn_account(logged_in=False),
    )
    def test_check_account(self):
        """Test the utils.check_account method."""
        with self.assertRaises(utils.NotLoggedInError):
            utils.check_account()

    @mock.patch(
        "src.nordvpn.commands.nordvpn_account",
        mock_commands.get_mock_nordvpn_account(logged_in=False),
    )
    def test_is_logged_in(self):
        """Test the utils.is_logged_in method."""
        is_logged_in = utils.is_logged_in()
        assert isinstance(is_logged_in, bool)
        assert not is_logged_in

    @mock.patch.multiple(
        "src.nordvpn.commands",
        nordvpn_account=mock_commands.get_mock_nordvpn_account(logged_in=False),
        nordvpn_logout=mock_commands.get_mock_nordvpn_logout(logged_in=False),
    )
    def test_run_logout(self):
        """Test the utils.run_logout function."""
        with self.assertRaises(utils.NotLoggedInError):
            utils.run_logout()

    @mock.patch.multiple(
        "src.nordvpn.commands",
        nordvpn_account=mock_commands.get_mock_nordvpn_account(logged_in=False),
        nordvpn_login=mock_commands.get_mock_nordvpn_login(logged_in=False),
    )
    def test_run_login(self):
        """Test the utils.run_login function."""
        output = utils.run_login()
        assert "continue in the browser" in output.lower()
