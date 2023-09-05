from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Button, Footer, Header, Pretty, Static


class LoginBox(Static):
    def compose(self) -> ComposeResult:
        yield Button("Log in", id="login-button", variant="success")
        yield Pretty({"a": 1, "b": 2}, id="login-info")


class ConnectBox(Static):
    def compose(self) -> ComposeResult:
        yield Pretty({"a": 1, "b": 2}, id="login-info")
        yield Button("Connect", id="connect-button", variant="success")


class StatusHeader(Static):
    def compose(self) -> ComposeResult:
        yield LoginBox()
        yield ConnectBox()


class NordvpnTUI(App):
    CSS_PATH = "placeholder.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield ScrollableContainer(StatusHeader())


if __name__ == "__main__":
    app = NordvpnTUI()
    app.run()
