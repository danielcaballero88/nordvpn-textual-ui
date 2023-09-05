import unittest

from src.nordvpn.exceptions import NotLoggedInError, NotLoggedOutError
from src.nordvpn.nordvpn import NordvpnBase


class TestNordvpnBase(unittest.TestCase):
    """Tests for the NordvpnBase class when logged in."""

    def setUp(self):
        self.nordvpn = NordvpnBase(test=True)
        self.nordvpn.cmds.set_logged_in(True)
        self.nordvpn.cmds.set_connected(False)

    def test_check_account(self):
        """Test the utils.check_account method."""
        # Logged in case:
        result = self.nordvpn.check_account()
        assert isinstance(result, dict)
        assert result.get("email") == "mock@mail.com"
        assert result.get("expiration") == "Expires on Jul 15th, 2025"

        # Logged out case:
        self.nordvpn.cmds.set_logged_in(False)
        with self.assertRaises(NotLoggedInError):
            self.nordvpn.check_account()

    def test_is_logged_in(self):
        """Test the utils.is_logged_in method."""
        # Logged in case:
        is_logged_in = self.nordvpn.is_logged_in()
        assert isinstance(is_logged_in, bool)
        assert is_logged_in

        # Logged out case:
        self.nordvpn.cmds.set_logged_in(False)
        is_logged_in = self.nordvpn.is_logged_in()
        assert isinstance(is_logged_in, bool)
        assert not is_logged_in

    def test_run_logout(self):
        """Test the utils.run_logout function."""
        # Logged in case:
        output = self.nordvpn.run_logout()
        assert "you are logged out" in output.lower()

        # Logged out case:
        self.nordvpn.cmds.set_logged_in(False)
        with self.assertRaises(NotLoggedInError):
            self.nordvpn.run_logout()

    def test_run_login(self):
        """Test the utils.run_login function."""
        # Logged in case:
        with self.assertRaises(NotLoggedOutError):
            self.nordvpn.run_login()

        # Logged out case:
        self.nordvpn.cmds.set_logged_in(False)
        output = self.nordvpn.run_login()
        assert "continue in the browser" in output.lower()

    def test_get_status_if_connected(self):
        """Test the utils.get_status function when connected."""
        self.nordvpn.cmds.set_connected(True)
        # Logged in case:
        status = self.nordvpn.get_status()
        assert isinstance(status, dict)
        assert status == {
            "Status": "Connected",
            "Country": "Mock_Country",
            "City": "Mock_City",
            "IP": "123.123.123.1",
            "Uptime": "18 seconds",
        }

        # Logged out case:
        # logged in = False and connected = True is a non-case (cannot
        # be connected if logged out) but still it's good to add the
        # test case to ensure the code works.
        self.nordvpn.cmds.set_logged_in(False)
        with self.assertRaises(NotLoggedInError):
            self.nordvpn.get_status()

    def test_get_status_if_disconnected(self):
        """Test the utils.get_status function when disconnected."""
        self.nordvpn.cmds.set_connected(False)
        # Logged in case:
        status = self.nordvpn.get_status()
        assert isinstance(status, dict)
        assert status == {
            "Status": "Disconnected",
            "Country": None,
            "City": None,
            "IP": None,
            "Uptime": None,
        }

        # Logged out case:
        self.nordvpn.cmds.set_logged_in(False)
        with self.assertRaises(NotLoggedInError):
            self.nordvpn.get_status()

    def test_get_countries(self):
        """Test the utils.get_countries function."""
        # Logged in case:
        countries = self.nordvpn.get_countries()
        assert isinstance(countries, list)
        assert countries == [
            "Mock_Country_1",
            "Mock_Country_2",
            "Mock_Country_3",
            "Mock_Country_4",
        ]

        # Logged out case:
        self.nordvpn.cmds.set_logged_in(False)
        with self.assertRaises(NotLoggedInError):
            self.nordvpn.get_countries()

    def test_get_cities(self):
        """Test the utils.get_cities function."""
        # Logged in case:
        cities = self.nordvpn.get_cities("Some_Country")
        assert isinstance(cities, list)
        assert cities == ["Mock_City_1", "Mock_City_2"]

        # Logged out case:
        self.nordvpn.cmds.set_logged_in(False)
        with self.assertRaises(NotLoggedInError):
            self.nordvpn.get_cities("Some_Country")

    def test_connect_to_location(self):
        """Test the utils.connect_to_location function."""
        # Logged in case:
        result = self.nordvpn.connect_to_location("Some_Location")
        assert isinstance(result, str)
        assert "you are connected to" in result.lower()

        # Logged out case:
        self.nordvpn.cmds.set_logged_in(False)
        with self.assertRaises(NotLoggedInError):
            self.nordvpn.connect_to_location("Some_Country")

    def test_disconnect_from_nordvpn(self):
        """Test the utils.disconnect_from_nordvpn function."""
        # Logged and connected in case:
        self.nordvpn.cmds.set_connected(True)
        result = self.nordvpn.disconnect_from_nordvpn()
        assert isinstance(result, str)
        assert "you are disconnected" in result.lower()

        # Logged in case and disconnected case:
        self.nordvpn.cmds.set_connected(False)
        result = self.nordvpn.disconnect_from_nordvpn()
        assert isinstance(result, str)
        assert "you are not connected" in result.lower()

        # Logged out case:
        self.nordvpn.cmds.set_logged_in(False)
        with self.assertRaises(NotLoggedInError):
            self.nordvpn.disconnect_from_nordvpn()
