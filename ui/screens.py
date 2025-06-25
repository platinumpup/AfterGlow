from kivy.uix.screenmanager import Screen
from kivy.properties import DictProperty

class LogScreen(Screen):
    substance_dose_map = DictProperty({
        "Meth": "mg",
        "LSD": "tabs",
        "Cocaine": "grams",
        "GHB": "mL",
        "MDMA": "mg",
        "Mushrooms": "grams",
        "Ketamine": "mg",
        "DMT": "mg",
        "Heroin": "grams",
    })

    def on_kv_post(self, base_widget):
        self.ids.substance_spinner.values = sorted(self.substance_dose_map.keys())
        self.ids.substance_spinner.text = "Select Substance"

    def on_substance_selected(self, substance):
        dose_unit = self.substance_dose_map.get(substance, "")
        self.ids.dose_input.hint_text = f"Enter dose ({dose_unit})"

class CommunityScreen(Screen):
    pass
