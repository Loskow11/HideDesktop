import ctypes
import os
import time

def find_desktop_handle():
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

def toggle_mode(hide=True):
    hwnd = find_desktop_handle()
    mode = 0 if hide else 5
    ctypes.windll.user32.ShowWindow(hwnd, mode)

if __name__ == "__main__":
    print("Testing hide...")
    toggle_mode(True)
    time.sleep(2)
    print("Testing show...")
    toggle_mode(False)