from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.core.text import LabelBase
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
import urllib.request
import urllib.error
import os
import json
import hashlib
from datetime import datetime

from kivy.core.window import Window
Window.size = (360, 640)

APP_VERSION = "v2.0"

def check_for_update():
    try:
        url = "https://raw.githubusercontent.com/platinumpup/afterglow/main/latest_version.txt"
        with urllib.request.urlopen(url, timeout=5) as response:
            latest_version = response.read().decode('utf-8').strip()
        if APP_VERSION != latest_version:
            print(f"Your version {APP_VERSION} is outdated. Latest is {latest_version}. Please update!")
            return False
        return True
    except urllib.error.URLError:
        print("Could not check for updates (offline or server error). Allowing app to run.")
        return True  # or False if you want strict blocking


# Set up font
base_dir = os.path.dirname(os.path.abspath(__file__))
LabelBase.register(
    name="EncodeSansSC",
    fn_regular=os.path.join(base_dir, "fonts", "EncodeSansSC-Regular.ttf")
)

USERDATA_FILE = os.path.join(base_dir, "userdata.json")
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

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class SplashScreen(Screen):
    def on_enter(self):
        self.start_slogan_animation()

    def start_slogan_animation(self):
        # Remove previous slogan if any
        if hasattr(self, 'slogan_anchor'):
            self.remove_widget(self.slogan_anchor)

        # AnchorLayout centers slogan_box horizontally
        self.slogan_anchor = AnchorLayout(
            anchor_x='center',
            anchor_y='top',
            size_hint=(1, None),
            height=80,
            pos_hint={'center_y': 0.4}
        )
        self.add_widget(self.slogan_anchor)

        # BoxLayout inside AnchorLayout for left-aligned words
        self.slogan_box = BoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint=(None, None),
            height=50,
            width=0,  # will grow as labels are added
        )
        self.slogan_anchor.add_widget(self.slogan_box)

        self.slogan_labels = []
        words = ["dose.", "log.", "glow.", "repeat."]
        for word in words:
            lbl = Label(
                text=word,
                font_name="EncodeSansSC",
                font_size=32,
                color=(0, 1, 1, 1),
                opacity=0,
                size_hint=(None, None),
            )
            lbl.texture_update()
            lbl.size = lbl.texture_size
            self.slogan_box.add_widget(lbl)
            self.slogan_labels.append(lbl)

            # Increase width of slogan_box to fit this label plus spacing
            self.slogan_box.width += lbl.width + self.slogan_box.spacing

        # Total duration for slogan animation (0.5 sec per word)
        self.total_slogan_duration = len(words) * 0.5

        # Animate words one by one
        self.animate_slogan_word(0)

        # Schedule afterglow_label fade-in halfway through slogan animation
        Clock.schedule_once(self.start_afterglow_fade_in, self.total_slogan_duration / 2)

    def animate_slogan_word(self, index):
        if index >= len(self.slogan_labels):
            return
        label = self.slogan_labels[index]
        anim = Animation(opacity=1, duration=0.5)
        anim.bind(on_complete=lambda *_: self.animate_slogan_word(index + 1))
        anim.start(label)

    def start_afterglow_fade_in(self, dt):
        fade_duration = self.total_slogan_duration / .5
        anim = Animation(opacity=1, duration=fade_duration)
        anim.bind(on_complete=self.after_afterglow_fade_in)
        anim.start(self.ids.afterglow_label)

    def after_afterglow_fade_in(self, animation, widget):
        # Remove slogan once afterglow_label fully visible
        if hasattr(self, 'slogan_anchor'):
            self.remove_widget(self.slogan_anchor)
            del self.slogan_anchor
            del self.slogan_box
            del self.slogan_labels

        # Show options box
        anim = Animation(opacity=1, duration=1)
        anim.start(self.ids.options_box)

    def show_options(self):
        self.ids.options_box.opacity = 1

    def open_login(self):
        self.login_popup = LoginPopup()
        self.login_popup.open()

    def open_signup(self):
        self.signup_popup = SignUpPopup()
        self.signup_popup.open()

    def open_skip(self):
        self.skip_popup = SkipPopup()
        self.skip_popup.open()

class CommunityScreen(Screen):
    pass

class LogScreen(Screen):
    def on_kv_post(self, base_widget):
        self.ids.substance_spinner.values = sorted(SUBSTANCE_DOSES.keys())
        self.ids.substance_spinner.text = "Select Substance"

    def on_substance_selected(self, substance):
        unit = SUBSTANCE_DOSES.get(substance, "")
        self.ids.dose_input.hint_text = f"Enter dose ({unit})"

    def add_entry(self):
        app = App.get_running_app()
        substance = self.ids.substance_spinner.text
        dose = self.ids.dose_input.text
        time = self.ids.time_input.text or datetime.now().strftime("%H:%M:%S")
        notes = self.ids.meal_input.text.strip()

        if substance == "Select Substance" or not dose:
            return

        unit = SUBSTANCE_DOSES.get(substance, "")
        entry = f"[b]{substance}[/b]: {dose} {unit} at {time}"
        if notes:
            entry += f" | Notes: {notes}"
        entry += "\n"

        self.ids.ReadMe_label.text = entry + self.ids.ReadMe_label.text
        app.log_dosage(substance, float(dose), unit, datetime.now())

        self.ids.dose_input.text = ""
        self.ids.time_input.text = ""
        self.ids.meal_input.text = ""
        self.ids.substance_spinner.text = "Select Substance"

class ReadMeScreen(Screen):
    pass

class LoginPopup(Popup):
    username_input = ObjectProperty(None)
    password_input = ObjectProperty(None)
    login_status = ObjectProperty(None)

    def try_login(self):
        username = self.ids.username_input.text.strip()
        password = self.ids.password_input.text.strip()
        if not os.path.exists(USERDATA_FILE):
            self.ids.login_status.text = "[color=ff3333]No users registered.[/color]"
            return
        with open(USERDATA_FILE) as f:
            data = json.load(f)
        hashed = hash_password(password)
        if data.get(username) == hashed:
            self.dismiss()
            App.get_running_app().root.current = "main_screen"
        else:
            self.ids.login_status.text = "[color=ff3333]Invalid credentials.[/color]"

class SignUpPopup(Popup):
    new_username_input = ObjectProperty(None)
    new_password_input = ObjectProperty(None)
    signup_status = ObjectProperty(None)

    def try_signup(self):
        username = self.ids.new_username_input.text.strip()
        password = self.ids.new_password_input.text.strip()
        if not username or not password:
            self.ids.signup_status.text = "[color=ff3333]Fill all fields.[/color]"
            return
        data = {}
        if os.path.exists(USERDATA_FILE):
            with open(USERDATA_FILE) as f:
                data = json.load(f)
        if username in data:
            self.ids.signup_status.text = "[color=ff3333]Username exists.[/color]"
            return
        data[username] = hash_password(password)
        with open(USERDATA_FILE, 'w') as f:
            json.dump(data, f)
        self.dismiss()
        App.get_running_app().root.current = "main_screen"

class SkipPopup(Popup):
    def proceed_skip(self):
        self.dismiss()
        App.get_running_app().root.current = "main_screen"

class AfterGlowApp(App):
    readme_text = (
        "░█▀█░█▀▀░▀█▀░█▀▀░█▀▄░█▀▀░█░░░█▀█░█░█\n\n"
        "░█▀█░█▀▀░░█░░█▀▀░█▀▄░█░█░█░░░█░█░█▄█\n\n"
        "░▀░▀░▀░░░░▀░░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀\n\n"
        "AfterGlow © 2025 Platinumpup\n\n"
        "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
        "of this software and associated documentation files (the \"Software\"), to deal\n"
        "in the Software without restriction, including without limitation the rights\n"
        "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
        "copies of the Software, and to permit persons to whom the Software is\n"
        "furnished to do so, subject to the following conditions:\n\n"
        "The above copyright notice and this permission notice shall be included in all\n"
        "copies or substantial portions of the Software.\n\n"
        "MIT License\n\n"
        "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
        "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
        "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
        "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
        "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
        "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
        "SOFTWARE."
    )
    def build(self):
        if not check_for_update():
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self.stop(), 0.1)
            return Label(text="Update required.\nPlease download the latest version.", halign="center", valign="middle")
        
        self.title = "AfterGlow v2.0"
        self.icon = os.path.join(base_dir, "assets", "AfterGlow.ico")
        self.dosage_log = {substance: [] for substance in SUBSTANCE_DOSES}
        return Builder.load_file("afterglow.kv")

    def build(self):
        self.title = "AfterGlow v2.0"
        self.icon = os.path.join(base_dir, "assets", "AfterGlow.ico")
        self.dosage_log = {substance: [] for substance in SUBSTANCE_DOSES}
        return Builder.load_file("afterglow.kv")
    
    def on_splash_done(self):
        # Called after splash screen finishes
        from kivy.uix.screenmanager import FadeTransition
        self.sm.transition = FadeTransition(duration=0.3)
        self.sm.current = "log_screen"

    def log_dosage(self, substance, dose, unit, time):
        self.dosage_log[substance].append({
            "dose": dose,
            "unit": unit,
            "time": time
        })

    def get_total(self, substance, period="day"):
        now = datetime.now()
        total = 0.0
        for record in self.dosage_log.get(substance, []):
            delta = now - record["time"]
            if period == "day" and delta.days == 0:
                total += record["dose"]
            elif period == "week" and delta.days < 7:
                total += record["dose"]
        return round(total, 2)

if __name__ == "__main__":
    AfterGlowApp().run()
