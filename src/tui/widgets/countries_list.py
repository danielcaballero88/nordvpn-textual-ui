from textual import app as ta
from textual import reactive as tr
from textual import widgets as tw

from ..nordvpn_instance import nordvpn


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
        print("PRINT: ", "CountriesList", "compose")
        yield tw.OptionList(*self.countries)

    def highlight_country(self, name):
        k = 0
        for k, val in enumerate(self.countries):
            if val == name:
                break
        self.query_one(tw.OptionList).highlighed = k
