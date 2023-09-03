import unittest
from unittest import mock

from src.nordvpn import utils

from ..commands.mock_commands import MockCommands

mock_commands = MockCommands()


@mock.patch("src.nordvpn.utils.commands", mock_commands)
class UtilsTests(unittest.TestCase):
    """Tests for the nordvpn.utils module when logged in."""

    def setUp(self):
        mock_commands.set_logged_in(True)
        mock_commands.set_connected(False)

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

    def test_run_logout(self):
        """Test the utils.run_logout function."""
        output = utils.run_logout()
        assert "you are logged out" in output.lower()

    def test_run_login(self):
        """Test the utils.run_login function."""
        with self.assertRaises(utils.NotLoggedOutError):
            utils.run_login()

    def test_get_status_if_connected(self):
        """Test the utils.get_status function when connected."""
        mock_commands.set_connected(True)
        status = utils.get_status()
        assert isinstance(status, dict)
        assert status == {
            "Status": "Connected",
            "Country": "Mock_Country",
            "City": "Mock_City",
            "IP": "123.123.123.1",
            "Uptime": "18 seconds",
        }

    def test_get_status_if_disconnected(self):
        """Test the utils.get_status function when disconnected."""
        mock_commands.set_connected(False)
        status = utils.get_status()
        assert isinstance(status, dict)
        assert status == {
            "Status": "Disconnected",
            "Country": None,
            "City": None,
            "IP": None,
            "Uptime": None,
        }

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
        cities = utils.get_cities("Some_Country")
        assert isinstance(cities, list)
        assert cities == ["Mock_City_1", "Mock_City_2"]

    def test_connect_to_location(self):
        """Test the utils.connect_to_location function."""
        result = utils.connect_to_location("Some_Location")
        assert isinstance(result, str)
        assert "you are connected to" in result.lower()

    def test_disconnect_from_nordvpn(self):
        """Test the utils.disconnect_from_nordvpn function."""
        mock_commands.set_connected(True)
        result = utils.disconnect_from_nordvpn()
        assert isinstance(result, str)
        assert "you are disconnected" in result.lower()

        mock_commands.set_connected(False)
        result = utils.disconnect_from_nordvpn()
        assert isinstance(result, str)
        assert "you are not connected" in result.lower()


@mock.patch("src.nordvpn.utils.commands", mock_commands)
class UtilsTestsLoggedOut(unittest.TestCase):
    """Tests for the nordvpn.utils module when logged out."""

    def setUp(self):
        mock_commands.set_logged_in(False)
        mock_commands.set_connected(False)

    def test_check_account(self):
        """Test the utils.check_account method."""
        with self.assertRaises(utils.NotLoggedInError):
            utils.check_account()

    def test_is_logged_in(self):
        """Test the utils.is_logged_in method."""
        is_logged_in = utils.is_logged_in()
        assert isinstance(is_logged_in, bool)
        assert not is_logged_in

    def test_run_logout(self):
        """Test the utils.run_logout function."""
        with self.assertRaises(utils.NotLoggedInError):
            utils.run_logout()

    def test_run_login(self):
        """Test the utils.run_login function."""
        output = utils.run_login()
        assert "continue in the browser" in output.lower()

    def test_get_status(self):
        """Test the utils.get_status function."""
        with self.assertRaises(utils.NotLoggedInError):
            utils.get_status()

        # logged in = False and connected = True is a non-case (cannot
        # be connected if logged out) but still it's good to add the
        # test case to ensure the code works.
        mock_commands.set_connected(True)
        with self.assertRaises(utils.NotLoggedInError):
            utils.get_status()

    def test_get_countries(self):
        """Test the utils.get_countries function."""
        with self.assertRaises(utils.NotLoggedInError):
            utils.get_countries()

    def test_get_cities(self):
        """Test the utils.get_cities function."""
        with self.assertRaises(utils.NotLoggedInError):
            utils.get_cities("Some_Country")

    def test_get_connect_to_location(self):
        """Test the utils.get_connect function."""
        with self.assertRaises(utils.NotLoggedInError):
            utils.connect_to_location("Some_Country")

    def test_get_disconnect(self):
        """Test the utils.get_disconnect function."""
        with self.assertRaises(utils.NotLoggedInError):
            utils.disconnect_from_nordvpn()
