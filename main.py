import customtkinter as ctk
import ctypes
import os
from PIL import Image

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class HideDesktopApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HideDesktop - Hide Mode")
        self.geometry("400x300")
        self.resizable(False, False)

        if os.path.exists("logo.ico"):
            self.iconbitmap("logo.ico")

        self.is_hidden = False
        
        # UI Layout
        self.label_status = ctk.CTkLabel(self, text="STATUS: VISIBLE", font=("Arial Black", 20))
        self.label_status.pack(pady=(20, 10))

        self.btn_toggle = ctk.CTkButton(self, text="HIDE NOW", 
                                        command=self.toggle_mode, 
                                        height=50, fg_color="#3B8ED0", font=("Arial", 14, "bold"))
        self.btn_toggle.pack(pady=10, padx=20, fill="x")

        ctk.CTkFrame(self, height=2, fg_color="gray30").pack(fill="x", padx=20, pady=20)

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
            self.is_hidden = False
            self.label_status.configure(text="STATUS: VISIBLE", text_color="white")
            self.btn_toggle.configure(fg_color="#3B8ED0") 
        else:
            ctypes.windll.user32.ShowWindow(hwnd, 0)
            self.is_hidden = True
            self.label_status.configure(text="STATUS: HIDDEN", text_color="#FF5555")
            self.btn_toggle.configure(fg_color="#FF5555") 

if __name__ == "__main__":
    app = HideDesktopApp()
    app.mainloop()