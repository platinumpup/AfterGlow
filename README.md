┌──────────────────────────────────┐                                       
  ░█▀█░█▀▀░▀█▀░█▀▀░█▀▄░█▀▀░█░░░█▀█░█░█  
  ░█▀█░█▀▀░░█░░█▀▀░█▀▄░█░█░█░░░█░█░█▄█  
  ░▀░▀░▀░░░░▀░░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀                                         
└──────────────────────────────────┘

                      ©2025 Zachery Silas
                      All rights reserved

Welcome to the AfterGlow app

## Overview
AfterGlow is a harm reduction tracking app built with Kivy, designed for mobile and desktop use. It tracks substances, doses, and logs history with a modern neon turquoise UI.

## Setup Instructions

### Dependencies
- Python 3.7 or higher
- Kivy 2.3.1 (or latest)
- Optional: `cryptography` package for encryption features

### Installation
1. Clone or download this repo.
2. Add your font files (`Orbitron-Regular.ttf`) into the `fonts/` directory.
3. Add your app icon (e.g., `AfterGlow.ico`) into the `assets/` directory.
4. Run the app with `python main.py`.

### Build for Android
Use [Buildozer](https://buildozer.readthedocs.io/en/latest/) or [KivyMD's instructions](https://kivy.org/doc/stable/guide/packaging-android.html). Key points:
- Create `buildozer.spec` file
- Include your font and assets in the build
- Build and deploy APK

### Build for iOS
Use [Kivy-ios](https://github.com/kivy/kivy-ios) toolchain.
- Set up your environment with Xcode
- Use kivy-ios toolchain to create the project
- Include assets and fonts
- Build & deploy via Xcode

### Build for macOS
Use [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/) or [Briefcase](https://briefcase.readthedocs.io/en/latest/) to package the app.

### Notes
- The app window is fixed to a smartphone resolution of 360x640 for dev/testing.
- Customize fonts and icons by replacing the files in the `fonts/` and `assets/` folders.

=======


5. For mobile platforms (iOS/Android), refer to platform-specific Kivy build instructions (see docs/build_instructions.txt).

---

Usage
-----

1. **Logging Entries:**
- Select a substance from the dropdown menu.
- Enter the dose (units adjust automatically depending on substance).
- Optionally enter the time of intake.
- Add any meal notes.
- Press "Add Entry" to save the record.

2. **Viewing History:**
- Press "Refresh History" to view logged entries.
- History will display all saved substance intake logs.

3. **Community:**
- Press "Community" to visit the community page.
- Use the "Open Discord" button to join the AfterGlow Discord server for chat and support.

4. **Notifications:**
- The app provides gentle notifications for potential interactions or warnings about combinations.

5. **Account/Login:**
- Currently in development. Discord-based login planned for future releases.

---

Customization
-------------

- Update or replace the font by placing your `.ttf` file in the `fonts/` folder and adjusting the font registration in `main.py`.
- Replace the app icon by placing your `.ico` file in the `assets/` folder.
- Adjust theme colors by editing the Kivy `.kv` files.

---

Support & Contributions
-----------------------

- Open issues and feature requests on the GitHub repository.
- Contributions are welcome via pull requests.

---

AfterGlow v2.0©


=======

MIT License

Copyright© 2025 Zachery Silas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
