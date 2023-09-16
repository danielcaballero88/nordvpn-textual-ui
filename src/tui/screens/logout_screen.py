from textual import app as ta
from textual import containers as tc
from textual import screen as ts
from textual import widgets as tw


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
        if event.button.id == "button-logout-cancel":
            self.app.pop_screen()
