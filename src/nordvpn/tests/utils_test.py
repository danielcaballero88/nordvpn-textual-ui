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
@mock.patch.multiple(
    "src.nordvpn.commands",
    nordvpn_command=mock_nordvpn_command,
    nordvpn_account=mock_commands.get_mock_nordvpn_account(logged_in=True),
)
class UtilsTestsLoggedIn(unittest.TestCase):
    """Tests for the nordvpn.utils module when logged in."""

    def test_check_account(self):
        """Test the utils.check_account method."""
        result = utils.check_account()
        assert isinstance(result, dict)
        assert result.get("email") == "mock@mail.com"
        assert result.get("expiration") == "Expires on Jul 15th, 2025"

    def test_is_logged(self):
        """Test the utils.is_logged_in method."""
        is_logged_in = utils.is_logged_in()
        assert isinstance(is_logged_in, bool)
        assert is_logged_in

    @mock.patch(
        "src.nordvpn.commands.nordvpn_logout",
        mock_commands.get_mock_nordvpn_logout(logged_in=True),
    )
    def test_run_logout(self):
        """Test the utils.run_logout function."""
        output = utils.run_logout()
        assert "you are logged out" in output.lower()

    @mock.patch(
        "src.nordvpn.commands.nordvpn_login",
        mock_commands.get_mock_nordvpn_login(logged_in=True),
    )
    def test_run_login(self):
        """Test the utils.run_login function."""
        with self.assertRaises(utils.NotLoggedOutError):
            utils.run_login()

    def test_get_status(self):
        """Test the utils.get_status function."""
        with mock.patch(
            "src.nordvpn.commands.nordvpn_status",
            mock_commands.get_mock_nordvpn_status(logged_in=True, connected=False),
        ):
            status = utils.get_status()
            assert isinstance(status, dict)
            assert status == {
                "Status": "Disconnected",
                "Country": None,
                "City": None,
                "IP": None,
                "Uptime": None,
            }

        with mock.patch(
            "src.nordvpn.commands.nordvpn_status",
            mock_commands.get_mock_nordvpn_status(logged_in=True, connected=True),
        ):
            status = utils.get_status()
            assert isinstance(status, dict)
            assert status == {
                "Status": "Connected",
                "Country": "Mock_Country",
                "City": "Mock_City",
                "IP": "123.123.123.1",
                "Uptime": "18 seconds",
            }

    @mock.patch(
        "src.nordvpn.commands.nordvpn_countries",
        mock_commands.get_mock_nordvpn_countries(logged_in=True),
    )
    def test_get_countries(self):
        """Test the utils.get_countries function."""
        countries = utils.get_countries()
        assert isinstance(countries, list)
        assert countries == [
            "Albania",
            "Bulgaria",
            "Czech_Republic",
            "Greece",
            "Italy",
            "Moldova",
            "Romania",
            "Spain",
            "United_Kingdom",
            "Argentina",
            "Canada",
            "Denmark",
            "Hong_Kong",
            "Japan",
            "Netherlands",
            "Serbia",
            "Sweden",
            "United_States",
            "Australia",
            "Chile",
            "Estonia",
            "Hungary",
            "Latvia",
            "New_Zealand",
            "Singapore",
            "Switzerland",
            "Vietnam",
            "Austria",
            "Colombia",
            "Finland",
            "Iceland",
            "Lithuania",
            "North_Macedonia",
            "Slovakia",
            "Taiwan",
            "Belgium",
            "Costa_Rica",
            "France",
            "Indonesia",
            "Luxembourg",
            "Norway",
            "Slovenia",
            "Thailand",
            "Bosnia_And_Herzegovina",
            "Croatia",
            "Georgia",
            "Ireland",
            "Malaysia",
            "Poland",
            "South_Africa",
            "Turkey",
            "Brazil",
            "Cyprus",
            "Germany",
            "Israel",
            "Mexico",
            "Portugal",
            "South_Korea",
            "Ukraine",
        ]

    def test_get_cities(self):
        """Test the utils.get_cities function."""
        with mock.patch(
            "src.nordvpn.commands.nordvpn_cities",
        ) as mock_nordvpn_cities:
            mock_nordvpn_cities.return_value = mock_commands.get_mock_nordvpn_cities(
                logged_in=True
            )()
            cities = utils.get_cities("Some_Country")

            mock_nordvpn_cities.assert_called_with("Some_Country")
            assert isinstance(cities, list)
            assert cities == ["Mock_City_1", "Mock_City_2"]

    def test_connect_to_location(self):
        """Test the utils.connect_to_location function."""
        with mock.patch("src.nordvpn.commands.nordvpn_connect") as mock_nordvpn_connect:
            mock_nordvpn_connect.return_value = mock_commands.get_mock_nordvpn_connect(
                logged_in=True
            )()
            result = utils.connect_to_location("Some_Location")
            mock_nordvpn_connect.assert_called_with("Some_Location")
            assert isinstance(result, str)
            assert "you are connected to" in result.lower()

    @mock.patch(
        "src.nordvpn.commands.nordvpn_disconnect",
        mock_commands.get_mock_nordvpn_disconnect(logged_in=True),
    )
    def test_disconnect_from_nordvpn(self):
        """Test the utils.disconnect_from_nordvpn function."""
        result = utils.disconnect_from_nordvpn()
        assert isinstance(result, str)
        assert "you are disconnected" in result.lower()


# Mock the nordvpn_command method to ensure that no actual nordvpn shell
# command is called during tests in case of a mistake while development.
@mock.patch.multiple(
    "src.nordvpn.commands",
    nordvpn_command=mock_nordvpn_command,
    nordvpn_account=mock_commands.get_mock_nordvpn_account(logged_in=False),
)
class UtilsTestsLoggedOut(unittest.TestCase):
    """Tests for the nordvpn.utils module when logged in."""

    def test_check_account(self):
        """Test the utils.check_account method."""
        with self.assertRaises(utils.NotLoggedInError):
            utils.check_account()

    def test_is_logged_in(self):
        """Test the utils.is_logged_in method."""
        is_logged_in = utils.is_logged_in()
        assert isinstance(is_logged_in, bool)
        assert not is_logged_in

    @mock.patch(
        "src.nordvpn.commands.nordvpn_logout",
        mock_commands.get_mock_nordvpn_logout(logged_in=False),
    )
    def test_run_logout(self):
        """Test the utils.run_logout function."""
        with self.assertRaises(utils.NotLoggedInError):
            utils.run_logout()

    @mock.patch(
        "src.nordvpn.commands.nordvpn_login",
        mock_commands.get_mock_nordvpn_login(logged_in=False),
    )
    def test_run_login(self):
        """Test the utils.run_login function."""
        output = utils.run_login()
        assert "continue in the browser" in output.lower()

    def test_get_status(self):
        """Test the utils.get_status function."""
        with mock.patch(
            "src.nordvpn.commands.nordvpn_status",
            mock_commands.get_mock_nordvpn_status(logged_in=False, connected=False),
        ):
            with self.assertRaises(utils.NotLoggedInError):
                utils.get_status()

        with mock.patch(
            "src.nordvpn.commands.nordvpn_status",
            mock_commands.get_mock_nordvpn_status(logged_in=False, connected=True),
        ):
            with self.assertRaises(utils.NotLoggedInError):
                utils.get_status()

    @mock.patch(
        "src.nordvpn.commands.nordvpn_countries",
        mock_commands.get_mock_nordvpn_countries(logged_in=False),
    )
    def test_get_countries(self):
        """Test the utils.get_countries function."""
        with self.assertRaises(utils.NotLoggedInError):
            utils.get_countries()

    @mock.patch(
        "src.nordvpn.commands.nordvpn_cities",
        mock_commands.get_mock_nordvpn_cities(logged_in=False),
    )
    def test_get_cities(self):
        """Test the utils.get_cities function."""
        with self.assertRaises(utils.NotLoggedInError):
            utils.get_cities("Some_Country")

    @mock.patch(
        "src.nordvpn.commands.nordvpn_connect",
        mock_commands.get_mock_nordvpn_connect(logged_in=False),
    )
    def test_get_connect(self):
        """Test the utils.get_connect function."""
        with self.assertRaises(utils.NotLoggedInError):
            utils.connect_to_location("Some_Country")

    @mock.patch(
        "src.nordvpn.commands.nordvpn_disconnect",
        mock_commands.get_mock_nordvpn_disconnect(logged_in=False),
    )
    def test_get_disconnect(self):
        """Test the utils.get_disconnect function."""
        with self.assertRaises(utils.NotLoggedInError):
            utils.disconnect_from_nordvpn()
