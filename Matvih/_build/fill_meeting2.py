"""Заполняет открытый диалог повторяющейся задачи (поиск по позиции)."""
import time
import sys

from pywinauto import Application

hwnd = int(sys.argv[1])
app = Application(backend="win32").connect(handle=hwnd)
d = app.window(handle=hwnd)
d.set_focus()
time.sleep(0.4)

name = d.child_window(class_name="JWinproj-Edit", found_index=0)
name.set_edit_text("Совещание")
time.sleep(0.3)

dur = d.child_window(class_name="JWinproj-Edit", found_index=1)
dur.set_edit_text("1 ч")
dur.type_keys("{TAB}")
time.sleep(0.5)

d.child_window(title="Е&женедельно", class_name="Button").click()
time.sleep(0.8)

fri = d.child_window(title="пятни&цам", class_name="Button")
if not fri.is_checked():
    fri.click()
time.sleep(0.3)

start = d.child_window(title_re=".*02\\.02\\.26.*", class_name="Edit")
start.set_edit_text("06.02.26")
start.type_keys("{TAB}")
time.sleep(1.0)

d.child_window(title="ОК", class_name="Button").click()
print("OK")
time.sleep(4)
