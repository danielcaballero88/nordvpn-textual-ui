from textual import app as ta
from textual import reactive as tr
from textual import widgets as tw

from .connect_box import ConnectBox
from .login_box import LoginBox


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
