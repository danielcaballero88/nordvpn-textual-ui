from textual import app as ta
from textual import containers as tc
from textual import reactive as tr
from textual import widgets as tw

from ...nordvpn_instance import nordvpn


class LoginBox(tw.Static):
    """Container for the log in button."""

    logged_in = tr.reactive(False)

    def compose(self) -> ta.ComposeResult:
        yield tc.Vertical(
            tw.Button("Log in", id="button-login", variant="success"),
            tw.Button("Log out", id="button-logout", variant="warning"),
        )

    def watch_logged_in(self, val):
        print("PRINT: ", "LoginBox", "watch_logged_in", val)
        self.update_button_login()
        self.update_button_logout()

    def update_button_login(self) -> None:
        button = self.query_one("#button-login")
        if self.logged_in:
            button.label = f"{nordvpn.check_account()['email']}"
            button.variant = "success"
            button.disabled = True
        else:
            button.label = "Log in"
            button.variant = "success"
            button.disabled = False

    def update_button_logout(self) -> None:
        button = self.query_one("#button-logout")
        if self.logged_in:
            button.label = "Log out"
            button.variant = "warning"
            button.disabled = False
        else:
            button.label = "Logged out"
            button.variant = "default"
            button.disabled = True

    def on_button_pressed(self, event: tw.Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        print("PRINT: ", "LoginBox", "Button pressed: ", event.button)
