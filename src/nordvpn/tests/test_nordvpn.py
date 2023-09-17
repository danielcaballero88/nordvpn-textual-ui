import unittest

from src.nordvpn.exceptions import NotLoggedInError, NotLoggedOutError
from src.nordvpn.nordvpn import Nordvpn


class TestNordvpn(unittest.TestCase):
    """Tests for the NordvpnBase class when logged in."""

    def setUp(self):
        self.nordvpn = Nordvpn(test=True)
        self.nordvpn.run_login()
        self.nordvpn.disconnect_from_nordvpn()

    def test_get_logged_in(self):
        """Test the get_logged_in method."""
        # Logged in case:
        logged_in = self.nordvpn.get_logged_in()
        assert isinstance(logged_in, bool)
        assert logged_in

        # Logged out case:
        self.nordvpn.run_logout()
        logged_in = self.nordvpn.get_logged_in()
        assert isinstance(logged_in, bool)
        assert not logged_in

    def test_set_logged_in(self):
        """Test the set_logged_in_method."""
        assert self.nordvpn.get_logged_in()
        self.nordvpn.run_logout()
        assert not self.nordvpn.get_logged_in()

    def test_get_connected(self):
        """Test the get_connected method."""
        # Logged in and disconnected case:
        connected = self.nordvpn.get_connected()
        assert not connected
        # Logged in and connected case:
        self.nordvpn.connect_to_location("Mock_Country_3")
        connected = self.nordvpn.get_connected()
        assert connected
        # Logged out case:
        self.nordvpn.run_logout()
        connected = self.nordvpn.get_connected()
        assert not connected

    def test_check_account(self):
        """Test the check_account method."""
        # Logged in case:
        result = self.nordvpn.check_account()
        assert isinstance(result, dict)
        assert result.get("email") == "mock@mail.com"
        assert result.get("expiration") == "Expires on Jul 15th, 2025"

        # Logged out case:
        self.nordvpn.run_logout()
        with self.assertRaises(NotLoggedInError):
            self.nordvpn.check_account()

    def test_run_logout(self):
        """Test the run_logout function."""
        # Logged in case:
        output = self.nordvpn.run_logout()
        assert "you are logged out" in output.lower()

        # Logged out case:
        with self.assertRaises(NotLoggedInError):
            self.nordvpn.run_logout()

    def test_run_login(self):
        """Test the run_login function."""
        # Logged in case:
        with self.assertRaises(NotLoggedOutError):
            self.nordvpn.run_login()

        # Logged out case:
        self.nordvpn.run_logout()
        output = self.nordvpn.run_login()
        assert "continue in the browser" in output.lower()

    def test_get_status_if_connected(self):
        """Test the get_status function when connected."""
        self.nordvpn.connect_to_location("Mock_Country_1")
        # Logged in case:
        status = self.nordvpn.get_status()
        assert isinstance(status, dict)
        assert status == {
            "Status": "Connected",
            "Country": "Mock_Country_1",
            "City": "Mock_City_1_1",
            "IP": "123.123.123.1",
            "Uptime": "18 seconds",
        }

        # Logged out case:
        # logged in = False and connected = True is a non-case (cannot
        # be connected if logged out) but still it's good to add the
        # test case to ensure the code works.
        self.nordvpn.run_logout()
        with self.assertRaises(NotLoggedInError):
            self.nordvpn.get_status()

    def test_get_status_if_disconnected(self):
        """Test the get_status function when disconnected."""
        self.nordvpn.disconnect_from_nordvpn()
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
        self.nordvpn.run_logout()
        with self.assertRaises(NotLoggedInError):
            self.nordvpn.get_status()

    def test_get_countries(self):
        """Test the get_countries function."""
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
        self.nordvpn.run_logout()
        with self.assertRaises(NotLoggedInError):
            self.nordvpn.get_countries()

    def test_get_cities(self):
        """Test the get_cities function."""
        # Logged in case:
        cities = self.nordvpn.get_cities("Mock_Country_4")
        assert isinstance(cities, list)
        assert cities == ["Mock_City_4_1", "Mock_City_4_2"]

        # Logged out case:
        self.nordvpn.run_logout()
        with self.assertRaises(NotLoggedInError):
            self.nordvpn.get_cities("Some_Country")

    def test_connect_to_location(self):
        """Test the connect_to_location function."""
        # Logged in case:
        result = self.nordvpn.connect_to_location("Mock_Country_2")
        assert isinstance(result, str)
        assert "you are connected to" in result.lower()

        # Logged out case:
        self.nordvpn.run_logout()
        with self.assertRaises(NotLoggedInError):
            self.nordvpn.connect_to_location("Some_Country")

    def test_disconnect_from_nordvpn(self):
        """Test the disconnect_from_nordvpn function."""
        # Logged and connected in case:
        self.nordvpn.connect_to_location("Mock_Country_1")
        result = self.nordvpn.disconnect_from_nordvpn()
        assert isinstance(result, str)
        assert "you are disconnected" in result.lower()

        # Logged in case and disconnected case:
        self.nordvpn.disconnect_from_nordvpn()
        result = self.nordvpn.disconnect_from_nordvpn()
        assert isinstance(result, str)
        assert "you are not connected" in result.lower()

        # Logged out case:
        self.nordvpn.run_logout()
        with self.assertRaises(NotLoggedInError):
            self.nordvpn.disconnect_from_nordvpn()
