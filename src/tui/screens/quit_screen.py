from textual import app as ta
from textual import containers as tc
from textual import screen as ts
from textual import widgets as tw


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
        else:  # button-quit-cancel
            self.app.pop_screen()
