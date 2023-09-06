from textual.app import App, ComposeResult
from textual.containers import Grid, ScrollableContainer
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Static


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
    def __init__(self, logged_in: bool, *args, **kwargs):
        self.logged_in = reactive(logged_in)
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        if self.logged_in:
            msg = "Log out"
            variant = "warning"
        else:
            msg = "Log in"
            variant = "success"
        yield Button(msg, id="login-button", variant=variant)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button = event.button
        if button.id == "login-button":
            if self.logged_in:
                self.logged_in = False
                button.label = "Log in"
                button.variant = "success"
            else:
                self.logged_in = True
                button.label = "Log out"
                button.variant = "warning"


class ConnectBox(Static):
    def compose(self) -> ComposeResult:
        yield Button("Connect", id="connect-button", variant="success")


class StatusHeader(Static):
    def compose(self) -> ComposeResult:
        yield LoginBox(False, classes="button-box")
        yield ConnectBox(classes="button-box")


class NordvpnTUI(App):
    CSS_PATH = "app.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "request_quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield ScrollableContainer(StatusHeader())

    def action_request_quit(self) -> None:
        self.push_screen(QuitScreen())


if __name__ == "__main__":
    app = NordvpnTUI()
    app.run()
