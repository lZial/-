"""Досъёмка недостающих скриншотов (отдельный экземпляр MS Project)."""
import os
import sys
import time
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot as S

from pywinauto.keyboard import send_keys


def main():
    s = S.Shooter()
    # первым делом закрываем возможные всплывающие списки
    keys_to_pid("{ESC}{ESC}", s.pid)
    time.sleep(1.0)
    try:
        s.shot_dialog("01_сведения_о_проекте", ("Проект", "Сведения о проекте..."))
        s.shot_dialog("02_сведения_о_задаче", ("Проект", "Сведения о задаче..."), select_id=39)
        s.shot_dialog("07_вставить_столбец", ("Вставка", "Столбец..."), select_id=34)
        s.shot_dialog("17_отчеты", ("Отчет", "Отчеты..."))
        s.shot_dialog("22_формат_отрезка", ("Формат", "Формат отрезка..."), select_id=41)
        s.shot_dialog("24_связи_задач", ("Правка", "Связи..."), select_id=41)
        # ресурсная диаграмма
        try:
            s.ribbon_tab("Вид")
            s.ribbon_dropdown("Использование ресурсов", "Диаграмма использования ресурсов")
            time.sleep(1.2)
            s.fit_whole()
            size = s.grab_window(os.path.join(S.OUT, "32_диаграмма_использования_ресурсов.png"))
            S.L("OK   %-38s %s (ресурсная диаграмма)" % ("32_диаграмма_использования_ресурсов", size))
        except Exception as e:
            S.L("FAIL %-38s %s" % ("32_диаграмма_использования_ресурсов", str(e)[:100]))
        # повторно основной вид Ганта
        try:
            s.ribbon_tab("Вид")
            s.ribbon_click("Диаграмма Ганта")
            s.fit_whole()
            time.sleep(1.0)
        except Exception:
            pass
    except Exception:
        traceback.print_exc()
    S.L("---- досъёмка завершена")


if __name__ == "__main__":
    main()
