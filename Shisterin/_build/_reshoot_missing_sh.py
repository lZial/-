# -*- coding: utf-8 -*-
"""Досъёмка снимков 31, 32, 37, 39, 41, 42 для проекта Шистерина."""
import os, sys, time, traceback
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
from reshoot_fixed import Shot, capture, say


def shot_view(s, view, name, path):
    s.app.ViewApply(view)
    time.sleep(1.5)
    try:
        s.app.TimelineShow = False
    except Exception:
        pass
    try:
        s.app.ZoomTimescale(Entire=True)
    except Exception as e:
        say('zoom:', str(e)[:80])
    time.sleep(1.5)
    s.hide()
    time.sleep(0.5)
    size = capture(s.hwnd, path)
    say('OK', name, size)


def shot_stats(s, name, path):
    s.pre = set()
    s.show()
    if not s.menu('Проект', 'Сведения о проекте...'):
        raise RuntimeError('нет меню Сведения о проекте')
    h, title = s.wait_dialog()
    say('  диалог:', title)
    if not h:
        raise RuntimeError('нет диалога сведений')
    if not s.dlg_button(h, 'Статистика'):
        raise RuntimeError('нет кнопки Статистика')
    h2, t2 = s.wait_dialog()
    say('  статистика:', t2)
    if not h2:
        raise RuntimeError('нет окна статистики')
    time.sleep(1.0)
    size = capture(h2, path)
    say('OK', name, size)
    s.close_all()


def shot_task_tab(s, fragment, tid, tab, name, path):
    s.select_task(fragment, tid)
    s.pre = set()
    s.show()
    if not s.menu('Проект', 'Сведения о задаче...'):
        raise RuntimeError('нет меню Сведения о задаче')
    h, title = s.wait_dialog()
    say('  диалог:', title)
    if not h:
        raise RuntimeError('нет диалога задачи')
    if not s.dlg_tab(h, tab):
        raise RuntimeError('нет вкладки ' + tab)
    time.sleep(1.0)
    size = capture(h, path)
    say('OK', name, size)
    s.close_all()


def main():
    s = Shot()
    try:
        # 31 — использование ресурсов
        shot_view(s, 'Использование ресурсов', '31', os.path.join(paths.SHOTS, '31_использование_ресурсов.png'))
        # 32 — график ресурса
        shot_view(s, 'График ресурса', '32', os.path.join(paths.SHOTS, '32_график_ресурса.png'))
        # 37 — связь НН, вкладка «Предшественники»
        shot_task_tab(s, 'Создание репозитория', 8, 'Предшественники', '37',
                      os.path.join(paths.SHOTS, '37_связь_нн.png'))
        # 39 — статистика базового плана
        shot_stats(s, '39', os.path.join(paths.SHOTS, '39_статистика_проекта.png'))
        # 42 — тип задачи (вкладка «Дополнительно»)
        shot_task_tab(s, 'Создание репозитория', 8, 'Дополнительно', '42',
                      os.path.join(paths.SHOTS, '42_тип_задачи.png'))
        # 41 — статистика экспериментального файла
        s.app.FileOpen(paths.EXP_MPP)
        time.sleep(5)
        s.wait_ready()
        shot_stats(s, '41', os.path.join(paths.SHOTS, '41_затраты_после_изменения.png'))
    except Exception as e:
        say('FAIL', str(e)[:200])
        traceback.print_exc()
    finally:
        try:
            s.close_all()
            s.app.FileQuit()
        except Exception:
            pass


if __name__ == '__main__':
    main()
