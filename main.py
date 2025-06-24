from kivy.app import App
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import datetime
import os

# Register font
base_dir = os.path.dirname(os.path.abspath(__file__))
LabelBase.register(
    name="Orbitron",
    fn_regular=os.path.join(base_dir, "fonts", "Orbitron-Bold.ttf")
)

# Substance dose map
SUBSTANCE_DOSES = {
    "Meth": "grams",
    "LSD": "tabs",
    "Cocaine": "grams",
    "GHB": "mL",
    "MDMA": "mg",
    "Mushrooms": "grams",
    "Ketamine": "mg",
    "DMT": "mg",
    "Heroin": "grams",
}

class LogScreen(Screen):
    def on_kv_post(self, base_widget):
        self.ids.substance_spinner.values = sorted(SUBSTANCE_DOSES.keys())
        self.ids.substance_spinner.text = "Select Substance"
        # Visual setup already handled in .kv file

    def on_substance_selected(self, substance):
        dose_unit = SUBSTANCE_DOSES.get(substance, "")
        self.ids.dose_input.hint_text = f"Enter dose ({dose_unit})"

def add_entry(self):
    substance = self.ids.substance_spinner.text
    dose = self.ids.dose_input.text
    time = self.ids.time_input.text or datetime.now().strftime("%H:%M:%S")
    notes = self.ids.meal_input.text.strip()

    if substance == "Select Substance":
        self.ids.history_label.text = "[color=ff3333]Please select a substance![/color]"
        return
    if not dose:
        self.ids.history_label.text = "[color=ff3333]Please enter a dose![/color]"
        return

    dose_unit = SUBSTANCE_DOSES.get(substance, "")
    dose_text = f"{dose} {dose_unit}".strip()

    entry = f"[b]{substance}[/b]: {dose_text} at {time}"
    if notes:
        entry += f" | Notes: {notes}"
    entry += "\n"

    self.ids.history_label.text = entry + self.ids.history_label.text

class CommunityScreen(Screen):
    pass

class AfterGlowApp(App):
    def build(self):
        self.title = "AfterGlow v1.3"
        self.icon = os.path.join(base_dir, "assets", "AfterGlow.ico")
        from kivy.core.window import Window
        Window.size = (360, 640)  # typical smartphone size in pixels
        sm = ScreenManager()
        sm.add_widget(LogScreen(name="log_screen"))
        sm.add_widget(CommunityScreen(name="community_screen"))
        return sm

if __name__ == "__main__":
    Builder.load_file("afterglow.kv")
    AfterGlowApp().run()
