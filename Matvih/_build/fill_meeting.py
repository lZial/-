"""Заполняет открытый диалог «Сведения о повторяющейся задаче»."""
import time

from pywinauto import Application

HWND = 133046


def main():
    app = Application(backend="win32").connect(handle=HWND)
    d = app.window(handle=HWND)
    d.set_focus()
    time.sleep(0.5)

    # название
    name = d.child_window(class_name="JWinproj-Edit", found_index=0)
    name.set_edit_text("Совещание")
    time.sleep(0.3)

    # длительность (второе поле с заголовком «1 день»)
    dur = d.child_window(title_re=".*день.*", class_name="JWinproj-Edit")
    dur.set_edit_text("1 ч")
    time.sleep(0.3)

    # еженедельно
    d.child_window(title="Е&женедельно", class_name="Button").click()
    time.sleep(0.8)

    # пятница
    fri = d.child_window(title="пятни&цам", class_name="Button")
    if not fri.is_checked():
        fri.click()
    time.sleep(0.3)

    # начало повторения
    start = d.child_window(title_re=".*02\\.02\\.26.*", class_name="Edit")
    start.set_edit_text("06.02.26")
    start.type_keys("{TAB}")
    time.sleep(0.8)

    # окончание по дату
    d.child_window(title="Окончан&ие:", class_name="Button").click()
    time.sleep(0.5)
    end = d.child_window(title_re=".*17\\.08\\.26.*", class_name="Edit")
    end.set_edit_text("14.08.26")
    end.type_keys("{TAB}")
    time.sleep(0.8)

    d.child_window(title="ОК", class_name="Button").click()
    print("OK нажат")
    time.sleep(4)


if __name__ == "__main__":
    main()
