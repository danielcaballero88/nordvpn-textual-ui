from textual.app import App, ComposeResult
from textual.containers import Grid, ScrollableContainer
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Static

from src.nordvpn.nordvpn import Nordvpn

nordvpn = Nordvpn(test=True)


class QuitScreen(Screen):
    """Screen with a dialog to quit."""

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Are you sure you want to quit?", id="question"),
            Button("Quit", variant="error", id="quit"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        else:
            self.app.pop_screen()


class LoginBox(Static):
    logged_in = reactive(False)

    def compose(self) -> ComposeResult:
        yield Button("Login Button", id="login-button", variant="default")

    def watch_logged_in(self, val):
        print("PRINT: ", "LoginBox", "watch_logged_in", val)
        button = self.query_one(Button)
        if self.logged_in:
            button.label = f"Logged in: {nordvpn.check_account()['email']}"
            button.variant = "success"
        else:
            button.label = "Logged out"
            button.variant = "warning"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        print("PRINT: ", "LoginBox", "Button pressed: ", event.button)


class ConnectBox(Static):
    logged_in = reactive(False)
    connected = reactive(False)

    def compose(self) -> ComposeResult:
        yield Button(
            "Connect Button", id="connect-button", variant="default", disabled=True
        )

    def watch_logged_in(self, val):
        print("PRINT: ", "ConnectBox", "watch_logged_in", val)
        button = self.query_one(Button)
        button.disabled = not self.logged_in

        if self.connected:
            button.label = f"Connected: {nordvpn.get_status()['country']}"
            button.variant = "success"
        else:
            button.label = "Disconnected"
            button.variant = "warning"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        print("PRINT: ", "ConnectBox", "Button pressed: ", event.button)


class StatusHeader(Static):
    logged_in = reactive(False)

    def on_mount(self) -> None:
        self.logged_in = self.app.logged_in

    def watch_logged_in(self, val):
        print("PRINT: ", "StatusHeader", "watch_logged_in", val)
        self.query_one(LoginBox).logged_in = val
        self.query_one(ConnectBox).logged_in = val

    def compose(self) -> ComposeResult:
        yield LoginBox(classes="button-box")
        yield ConnectBox(classes="button-box")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        print("PRINT: ", "StatusHeader", "Button pressed: ", event.button)


class NordvpnTUI(App):
    CSS_PATH = "app.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "request_quit", "Quit"),
    ]

    logged_in = reactive(nordvpn.logged_in)

    def watch_logged_in(self, val):
        print("PRINT: ", "NordvpnTUI", "watch_logged_in", val)
        self.query_one(StatusHeader).logged_in = val

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield ScrollableContainer(StatusHeader())

    def action_request_quit(self) -> None:
        self.push_screen(QuitScreen())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        print("PRINT: ", "NordvpnTUI", "Button pressed: ", event.button)
        if event.button.id == "login-button":
            if not self.logged_in:
                self.log_in()
            else:
                self.log_out()

    def log_in(self):
        nordvpn.set_logged_in(True)
        self.logged_in = True

    def log_out(self):
        nordvpn.set_logged_in(False)
        self.logged_in = False


if __name__ == "__main__":
    app = NordvpnTUI()
    app.run()
