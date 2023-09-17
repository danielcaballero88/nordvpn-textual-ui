from textual import app as ta
from textual import containers as tc
from textual import reactive as tr
from textual import widgets as tw

from src.nordvpn.exceptions import NotLoggedInError

from . import screens as s
from . import widgets as w
from .nordvpn_instance import nordvpn


class NordvpnTUI(ta.App):
    """Main textual app."""

    CSS_PATH = [
        "app.tcss",
        "screens/screens.tcss",
        "widgets/status_header/status_header.tcss",
    ]
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "request_quit", "Quit"),
    ]

    logged_in = tr.reactive(nordvpn.get_logged_in())
    connected = tr.reactive(nordvpn.get_connected())
    selected_country = tr.reactive(None)

    def watch_logged_in(self, val):
        print("PRINT: ", "NordvpnTUI", "watch_logged_in", val)
        self.query_one(w.StatusHeader).logged_in = val
        self.query_one(w.CountriesList).logged_in = val

    def watch_connected(self, val):
        print("PRINT: ", "NordvpnTUI", "watch_connected", val)
        try:
            connected_country = nordvpn.get_status()["Country"]
        except NotLoggedInError:
            connected_country = None
        self.query_one(w.StatusHeader).connected = val
        self.query_one(w.CountriesList).connected_country = connected_country

    def watch_selected_country(self, val):
        print("PRINT: ", "NordvpnTUI", "watch_selected_country", val)
        self.query_one(w.StatusHeader).selected_country = self.selected_country

    def compose(self) -> ta.ComposeResult:
        yield tw.Header()
        yield tw.Footer()
        yield tc.Container(w.StatusHeader(), w.CountriesList())

    def action_request_quit(self) -> None:
        self.push_screen(s.QuitScreen(classes="confirm-decision-screen"))

    def on_button_pressed(self, event: tw.Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        print("PRINT: ", "NordvpnTUI", "Button pressed: ", event.button)
        if event.button.id == "button-login":
            self.log_in()
        elif event.button.id == "button-logout":
            self.push_screen(s.LogoutScreen(classes="confirm-decision-screen"))
        elif event.button.id == "button-logout-confirm":
            self.pop_screen()
            self.disconnect()
            self.log_out()
        elif event.button.id == "button-connect":
            self.connect()
        elif event.button.id == "button-disconnect":
            self.disconnect()

    def on_option_list_option_selected(self, event) -> None:
        print(
            "PRINT: ",
            "NordvpnTUI",
            "option selected: ",
            event.option_index,
            event.option.prompt,
        )
        self.selected_country = event.option.prompt

    def log_in(self):
        print("PRINT: ", "NordvpnTUI", "log_in")
        nordvpn.run_login()
        self.logged_in = True

    def log_out(self):
        print("PRINT: ", "NordvpnTUI", "log_out")
        nordvpn.run_logout()
        self.logged_in = False

    def connect(self):
        print("PRINT: ", "NordvpnTUI", "connect")
        nordvpn.connect_to_location(self.selected_country)
        self.connected = True

    def disconnect(self):
        print("PRINT: ", "NordvpnTUI", "disconnect")
        nordvpn.disconnect_from_nordvpn()
        self.connected = False

    def on_click(self, event) -> None:
        print("PRINT: ", "NordvpnTUI", "click", event)


if __name__ == "__main__":
    app = NordvpnTUI()
    app.run()
