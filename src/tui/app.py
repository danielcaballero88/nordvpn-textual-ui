from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Button, Footer, Header, Static


class LoginBox(Static):
    def compose(self) -> ComposeResult:
        yield Button("Log in", id="login-button", variant="success")


class ConnectBox(Static):
    def compose(self) -> ComposeResult:
        yield Button("Connect", id="connect-button", variant="success")


class StatusHeader(Static):
    def compose(self) -> ComposeResult:
        yield LoginBox(classes="button-box")
        yield ConnectBox(classes="button-box")


class NordvpnTUI(App):
    CSS_PATH = "app.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield ScrollableContainer(StatusHeader())


if __name__ == "__main__":
    app = NordvpnTUI()
    app.run()
