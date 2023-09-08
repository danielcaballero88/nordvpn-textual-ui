from textual import app as ta
from textual import containers as tc
from textual import reactive as tr
from textual import screen as ts
from textual import widgets as tw

from src.nordvpn.nordvpn import Nordvpn

nordvpn = Nordvpn(test=True)
nordvpn.run_login()
nordvpn.connect_to_location("Mock_Country_2")


class QuitScreen(ts.Screen):
    """Screen with a dialog to quit."""

    def compose(self) -> ta.ComposeResult:
        yield tc.Grid(
            tw.Label(
                "Are you sure you want to quit?",
                id="quit-question",
                classes="confirmation-question",
            ),
            tw.Button("Quit", variant="error", id="button-quit-confirm"),
            tw.Button("Cancel", variant="primary", id="button-quit-cancel"),
            classes="confirmation-dialog",
            id="quit-dialog",
        )

    def on_button_pressed(self, event: tw.Button.Pressed) -> None:
        if event.button.id == "button-quit-confirm":
            self.app.exit()
        else:
            self.app.pop_screen()


class LogoutScreen(ts.Screen):
    """Screen with a dialog to logout."""

    def compose(self) -> ta.ComposeResult:
        yield tc.Grid(
            tw.Label(
                "Are you sure you want to log out?",
                id="logout-question",
                classes="confirmation-question",
            ),
            tw.Button("Log out", variant="error", id="button-logout-confirm"),
            tw.Button("Cancel", variant="primary", id="button-logout-cancel"),
            classes="confirmation-dialog",
            id="logout-dialog",
        )

    def on_button_pressed(self, event: tw.Button.Pressed) -> None:
        print("PRINT: ", "LogoutScreen", "Button pressed: ", event.button)
        self.app.pop_screen()
        if event.button.id == "button-logout-confirm":
            self.app.log_out()


class LoginBox(tw.Static):
    """Container for the log in button."""

    logged_in = tr.reactive(False)

    def compose(self) -> ta.ComposeResult:
        yield tw.Button("Login Button", id="button-login", variant="default")

    def watch_logged_in(self, val):
        print("PRINT: ", "LoginBox", "watch_logged_in", val)
        button = self.query_one(tw.Button)
        if self.logged_in:
            button.label = f"Logged in: {nordvpn.check_account()['email']}"
            button.variant = "success"
        else:
            button.label = "Logged out"
            button.variant = "warning"

    def on_button_pressed(self, event: tw.Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        print("PRINT: ", "LoginBox", "Button pressed: ", event.button)


class ConnectBox(tw.Static):
    """Container for the connect button."""

    logged_in = tr.reactive(False)
    connected = tr.reactive(False)
    selected_country = tr.reactive(None)

    def compose(self) -> ta.ComposeResult:
        yield tw.Button(
            "Connect Button", id="button-connect", variant="default", disabled=True
        )

    def watch_logged_in(self, val):
        print("PRINT: ", "ConnectBox", "watch_logged_in", val)
        self.update_disabled_status()

    def watch_connected(self, val):
        print("PRINT: ", "ConnectBox", "watch_connected", val)
        button = self.query_one(tw.Button)
        if self.connected:
            button.label = f"Connected: {nordvpn.get_status()['Country']}"
            button.variant = "success"
        else:
            button.label = "Disconnected"
            button.variant = "warning"

    def watch_selected_country(self, val):
        print("PRINT: ", "ConnectBox", "watch_selected_country", val)
        self.update_disabled_status()

    def update_disabled_status(self):
        button = self.query_one(tw.Button)
        if self.logged_in and self.selected_country is not None:
            button.disabled = False
        else:
            button.disabled = True

    def on_button_pressed(self, event: tw.Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        print("PRINT: ", "ConnectBox", "Button pressed: ", event.button)


class StatusHeader(tw.Static):
    """Widget for the top bar to log in/out and connect/disconnect."""

    logged_in = tr.reactive(False)
    connected = tr.reactive(False)
    selected_country = tr.reactive(None)

    def on_mount(self) -> None:
        self.logged_in = self.app.logged_in

    def watch_logged_in(self, val):
        print("PRINT: ", "StatusHeader", "watch_logged_in", val)
        self.query_one(LoginBox).logged_in = val
        self.query_one(ConnectBox).logged_in = val

    def watch_connected(self, val):
        print("PRINT: ", "StatusHeader", "watch_connected", val)
        self.query_one(ConnectBox).connected = val

    def watch_selected_country(self, val):
        print("PRINT: ", "StatusHeader", "watch_selected_country", val)
        self.query_one(ConnectBox).selected_country = self.selected_country

    def compose(self) -> ta.ComposeResult:
        yield LoginBox(classes="button-box")
        yield ConnectBox(classes="button-box")

    def on_button_pressed(self, event: tw.Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        print("PRINT: ", "StatusHeader", "Button pressed: ", event.button)


class CountriesList(tw.Static):
    """Widget for the list of countries to connect to."""

    logged_in = tr.reactive(False)
    countries = tr.reactive([])
    connected_country = tr.reactive(None)

    def on_mount(self) -> None:
        self.logged_in = self.app.logged_in

    def watch_logged_in(self, val):
        if self.logged_in:
            self.countries = nordvpn.get_countries()
        else:
            self.countries = ["not logged in!"]
        print("PRINT: ", "CountriesList", "watch_logged_in", val)

    def watch_countries(self, val):
        print("PRINT: ", "CountriesList", "watch_countries", val)
        try:
            for widget in self.query(tw.OptionList):  # pylint: disable=not-an-iterable
                widget.remove()
        except Exception as exc:
            print("PRINT: ", "CountriesList", "watch_countries", exc)
        self.mount(tw.OptionList(*self.countries))

    def watch_connected_country(self, val):
        print("PRINT: ", "CountriesList", "watch_connected_country", val)
        if val is None:
            self.query_one(tw.OptionList).disabled = False
        else:  # connected to some country
            for k, country in enumerate(self.countries):
                if country == val:
                    break
            else:
                # found a country
                self.query_one(tw.OptionList).highlighted = k
                self.disabled = True

    def compose(self) -> ta.ComposeResult:
        yield tw.OptionList(*self.countries)

    def highlight_country(self, name):
        for k, val in enumerate(self.countries):
            if val == name:
                break
        self.query_one(tw.OptionList).highlighed = k


class NordvpnTUI(ta.App):
    """Main textual app."""

    CSS_PATH = "app.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "request_quit", "Quit"),
    ]

    logged_in = tr.reactive(nordvpn.get_logged_in())
    connected = tr.reactive(nordvpn.get_connected())
    selected_country = tr.reactive(None)

    def watch_logged_in(self, val):
        print("PRINT: ", "NordvpnTUI", "watch_logged_in", val)
        self.query_one(StatusHeader).logged_in = val
        self.query_one(CountriesList).logged_in = val

    def watch_connected(self, val):
        print("PRINT: ", "NordvpnTUI", "watch_connected", val)
        connected_country = nordvpn.get_status()["Country"]
        self.query_one(StatusHeader).connected = val
        self.query_one(CountriesList).connected_country = connected_country

    def watch_selected_country(self, val):
        print("PRINT: ", "NordvpnTUI", "watch_selected_country", val)
        self.query_one(StatusHeader).selected_country = self.selected_country

    def compose(self) -> ta.ComposeResult:
        yield tw.Header()
        yield tw.Footer()
        yield tc.Container(StatusHeader(), CountriesList())

    def action_request_quit(self) -> None:
        self.push_screen(QuitScreen(classes="confirm-decision-screen"))

    def on_button_pressed(self, event: tw.Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        print("PRINT: ", "NordvpnTUI", "Button pressed: ", event.button)
        if event.button.id == "button-login":
            if not self.logged_in:
                self.log_in()
            else:
                self.push_screen(LogoutScreen(classes="confirm-decision-screen"))
        elif event.button.id == "button-logout-confirm":
            self.log_out()
        elif event.button.id == "button-connect":
            if not self.connected:
                print("PRINT: ", "NordvpnTUI", "connecting to: ", self.selected_country)
            else:  # connected
                ...

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
        nordvpn.run_login()
        self.logged_in = True

    def log_out(self):
        nordvpn.run_logout()
        self.logged_in = False

    def on_click(self, event) -> None:
        print("PRINT: ", "NordvpnTUI", "click", event)


if __name__ == "__main__":
    app = NordvpnTUI()
    app.run()
