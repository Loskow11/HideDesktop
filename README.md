# 🛡️ HideDesktop (Panic Button)

**HideDesktop** is a stealth productivity tool designed for Windows. It allows users to instantly hide all desktop icons and switch the wallpaper to a neutral black background with a single global hotkey. Perfect for presentations, privacy, or minimizing distractions.

## 🚀 Features

* **Global Hotkey:** Toggle visibility instantly (Default: `Ctrl+Alt+P`), even when the app is minimized.
* **Stealth Mode:** Hides all desktop icons via Win32 API manipulation.
* **Wallpaper Automation:** Automatically switches to a black background and restores the original wallpaper upon restoration.
* **Customizable:** Record your own hotkey combination directly in the UI.
* **Multithreaded:** Non-blocking input recording for smooth UX.
* **Portable:** Single `.exe` file, no installation required.

## 🛠️ Tech Stack

* **Python 3.12**
* **CustomTkinter** (Modern UI)
* **Win32 API (ctypes)** (System manipulation)
* **Pillow** (Image processing)
* **Keyboard** (Global hook)

## 📦 Installation & Usage

1.  Download the latest `HideDesktop.exe` from the [Releases](https://github.com/Loskow11/HideDesktop/releases) page.
2.  Run the executable.
3.  Press `Ctrl+Alt+P` (or configure your own key) to hide/show desktop icons.

## ⚠️ Disclaimer

This tool is for educational and productivity purposes. It interacts with Windows `Shell_TrayWnd` and `Progman`.

---
*Developed by Loskow*