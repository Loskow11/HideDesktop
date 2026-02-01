import customtkinter as ctk
import ctypes
import keyboard
import os
import sys
import threading
import winreg
from PIL import Image

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class HideDesktopApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HideDesktop - Hide Mode")
        self.geometry("400x380")
        self.resizable(False, False)

        self.icon_path = resource_path("logo.ico")
        if os.path.exists(self.icon_path):
            self.iconbitmap(self.icon_path)

        self.is_hidden = False
        self.current_hotkey = "ctrl+alt+p" 
        self.original_wallpaper = None 
        self.black_wallpaper_path = self.create_black_image()

        self.label_status = ctk.CTkLabel(self, text="STATUS: VISIBLE", font=("Arial Black", 20))
        self.label_status.pack(pady=(20, 10))

        self.btn_toggle = ctk.CTkButton(self, text=f"HIDE NOW ({self.current_hotkey})", 
                                        command=self.toggle_mode, 
                                        height=50, fg_color="#3B8ED0", font=("Arial", 14, "bold"))
        self.btn_toggle.pack(pady=10, padx=20, fill="x")

        ctk.CTkFrame(self, height=2, fg_color="gray30").pack(fill="x", padx=20, pady=20)

        self.lbl_config = ctk.CTkLabel(self, text="Keyboard Shortcut:")
        self.lbl_config.pack()

        self.btn_record = ctk.CTkButton(self, text=f"Change ({self.current_hotkey})", 
                                        command=self.start_recording_thread, 
                                        fg_color="gray40", hover_color="gray50")
        self.btn_record.pack(pady=5)

        self.var_change_wallpaper = ctk.BooleanVar(value=True)
        self.check_wallpaper = ctk.CTkCheckBox(self, text="Enable Black Wallpaper", variable=self.var_change_wallpaper)
        self.check_wallpaper.pack(pady=15)

        keyboard.add_hotkey(self.current_hotkey, self.toggle_mode)

    def start_recording_thread(self):
        self.btn_record.configure(text="Press any keys...", fg_color="#E59400")
        self.btn_toggle.configure(state="disabled") 
        threading.Thread(target=self.wait_for_keys, daemon=True).start()

    def wait_for_keys(self):
        keyboard.remove_hotkey(self.current_hotkey)
        new_key = keyboard.read_hotkey(suppress=False)
        self.current_hotkey = new_key
        keyboard.add_hotkey(self.current_hotkey, self.toggle_mode)
        
        self.btn_record.configure(text=f"Change ({self.current_hotkey})", fg_color="gray40")
        self.btn_toggle.configure(text=f"HIDE NOW ({self.current_hotkey})", state="normal")

    def create_black_image(self):
        filename = "black_generated.png"
        path = os.path.abspath(filename)
        if not os.path.exists(path):
            img = Image.new('RGB', (100, 100), color='black')
            img.save(path)
        return path

    def get_wallpaper_api(self):
        ubuff = ctypes.create_unicode_buffer(512)
        ctypes.windll.user32.SystemParametersInfoW(0x0073, 512, ubuff, 0)
        return ubuff.value

    def get_wallpaper_registry(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(key, "WallPaper")
            winreg.CloseKey(key)
            return value
        except Exception:
            return None

    def set_wallpaper(self, path):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)

    def find_desktop_handle(self):
        user32 = ctypes.windll.user32
        progman = user32.FindWindowW("Progman", None)
        shell_view = user32.FindWindowExW(progman, 0, "SHELLDLL_DefView", None)
        
        if not shell_view:
            user32.SendMessageTimeoutW(progman, 0x052C, 0, 0, 0, 1000, ctypes.byref(ctypes.c_void_p()))
            workerw = 0
            def enum_proc(hwnd, lParam):
                nonlocal workerw
                sh_view = user32.FindWindowExW(hwnd, 0, "SHELLDLL_DefView", None)
                if sh_view: workerw = hwnd
                return True
            user32.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(enum_proc), 0)
            shell_view = user32.FindWindowExW(workerw, 0, "SHELLDLL_DefView", None)
            
        return user32.FindWindowExW(shell_view, 0, "SysListView32", None)

    def toggle_mode(self):
        hwnd = self.find_desktop_handle()
        
        if self.is_hidden:
            ctypes.windll.user32.ShowWindow(hwnd, 5)
            
            if self.var_change_wallpaper.get() and self.original_wallpaper and os.path.exists(self.original_wallpaper):
                if self.original_wallpaper != self.black_wallpaper_path:
                    self.set_wallpaper(self.original_wallpaper)
            
            self.is_hidden = False
            self.label_status.configure(text="STATUS: VISIBLE", text_color="white")
            self.btn_toggle.configure(fg_color="#3B8ED0") 
        else:
            found_wallpaper = None

            if self.var_change_wallpaper.get():
                path1 = self.get_wallpaper_api()
                if path1 and os.path.exists(path1) and path1 != self.black_wallpaper_path:
                    found_wallpaper = path1
                else:
                    path2 = self.get_wallpaper_registry()
                    if path2 and os.path.exists(path2) and path2 != self.black_wallpaper_path:
                        found_wallpaper = path2
                
                if found_wallpaper:
                    self.original_wallpaper = found_wallpaper
                    self.set_wallpaper(self.black_wallpaper_path)
                else:
                    self.var_change_wallpaper.set(False)

            ctypes.windll.user32.ShowWindow(hwnd, 0)
            self.is_hidden = True
            self.label_status.configure(text="STATUS: HIDDEN", text_color="#FF5555")
            self.btn_toggle.configure(fg_color="#FF5555") 

if __name__ == "__main__":
    app = HideDesktopApp()
    app.mainloop()