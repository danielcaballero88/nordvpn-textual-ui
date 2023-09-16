from textual import app as ta
from textual import containers as tc
from textual import reactive as tr
from textual import widgets as tw

from ...nordvpn_instance import nordvpn


class ConnectBox(tw.Static):
    """Container for the connect button."""

    logged_in = tr.reactive(False)
    connected = tr.reactive(False)
    selected_country = tr.reactive(None)

    def compose(self) -> ta.ComposeResult:
        yield tc.Vertical(
            tw.Button("Connect", id="button-connect", variant="success", disabled=True),
            tw.Button(
                "Disconnect", id="button-disconnect", variant="warning", disabled=True
            ),
        )

    def watch_logged_in(self, val):
        print("PRINT: ", "ConnectBox", "watch_logged_in", val)
        self.update_buttons()

    def watch_connected(self, val):
        print("PRINT: ", "ConnectBox", "watch_connected", val)
        self.update_buttons()

    def watch_selected_country(self, val):
        print("PRINT: ", "ConnectBox", "watch_selected_country", val)
        self.update_buttons()

    def update_buttons(self):
        print(
            "PRINT: ",
            "ConnectBox",
            "update_buttons",
            self.logged_in,
            self.connected,
            self.selected_country,
        )
        self.update_button_connect()
        self.update_button_disconnect()

    def update_button_connect(self) -> None:
        button = self.query_one("#button-connect")
        if not self.logged_in:
            print("######### 1 #########")
            button.label = "Connect"
            button.variant = "default"
            button.disabled = True
            return

        if self.connected:
            print("######### 2 #########")
            button.label = f"Connected: {nordvpn.get_status()['Country']}"
            button.variant = "success"
            button.disabled = True
        elif self.selected_country is not None:
            print("######### 3 #########")
            button.label = f"Connect to {self.selected_country}"
            button.variant = "warning"
            button.disabled = False
        else:
            print("######### 4 #########")
            button.label = "Connect to ..."
            button.variant = "warning"
            button.disabled = True

    def update_button_disconnect(self) -> None:
        button = self.query_one("#button-disconnect")
        if not self.logged_in:
            button.variant = "default"
            button.disabled = True
            return

        if self.connected:
            button.variant = "warning"
            button.disabled = False
        else:
            button.variant = "default"
            button.disabled = True

    def on_button_pressed(self, event: tw.Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        print("PRINT: ", "ConnectBox", "Button pressed: ", event.button)
