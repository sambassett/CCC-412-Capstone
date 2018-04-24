# Code from http://timgolden.me.uk/python/win32_how_do_i/find-the-window-for-my-subprocess.html
import win32gui
import win32process

def get_hwnds():
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            hwnds.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)

    return hwnds
