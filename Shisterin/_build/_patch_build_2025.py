# -*- coding: utf-8 -*-
"""Сдвиг проекта на 2025 год и исправление доступности ресурсов."""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
p = "build_project.py"
s = open(p, encoding="utf-8").read()

# 1. Все даты на год назад
s = s.replace("2026", "2025")

# 2. Старт проекта — понедельник 03.02.2025
s = s.replace("P_START = datetime.datetime(2025, 2, 2, 9, 0, 0)",
              "P_START = datetime.datetime(2025, 2, 3, 9, 0, 0)")

# 3. Праздники 2025 года (с переносами)
old_holidays = """HOLIDAYS = [
    datetime.date(2025, 1, 1), datetime.date(2025, 1, 2), datetime.date(2025, 1, 5),
    datetime.date(2025, 1, 6), datetime.date(2025, 1, 7), datetime.date(2025, 1, 8),
    datetime.date(2025, 2, 23), datetime.date(2025, 3, 8), datetime.date(2025, 5, 1),
    datetime.date(2025, 5, 9), datetime.date(2025, 6, 12), datetime.date(2025, 11, 4),
]"""
new_holidays = """HOLIDAYS = [
    datetime.date(2025, 1, 1), datetime.date(2025, 1, 2), datetime.date(2025, 1, 3),
    datetime.date(2025, 1, 6), datetime.date(2025, 1, 7), datetime.date(2025, 1, 8),
    datetime.date(2025, 2, 24), datetime.date(2025, 3, 10), datetime.date(2025, 5, 1),
    datetime.date(2025, 5, 2), datetime.date(2025, 5, 8), datetime.date(2025, 5, 9),
    datetime.date(2025, 6, 12), datetime.date(2025, 11, 4),
]"""
assert old_holidays in s
s = s.replace(old_holidays, new_holidays, 1)

# 4. Бригады: лимиты соответствуют пиковой параллельной загрузке
s = s.replace('("Мобильный разработчик", "МР", "Разработка", 2.0, 2200, 3500),',
              '("Мобильный разработчик", "МР", "Разработка", 4.0, 2200, 3500),')
s = s.replace('("Бэкенд-разработчик", "БР", "Разработка", 1.5, 2100, 3300),',
              '("Бэкенд-разработчик", "БР", "Разработка", 3.5, 2100, 3300),')
s = s.replace('("Тестировщик", "ТС", "Тестирование", 1.5, 1700, 2600),',
              '("Тестировщик", "ТС", "Тестирование", 4.0, 1700, 2600),')

# 5. Окна доступности: те же лимиты
old_av = """AVAILABILITY = [
    ("Архитектор", datetime.date(2025, 2, 2), datetime.date(2025, 6, 30), 1.0),
    ("Мобильный разработчик", datetime.date(2025, 2, 2), datetime.date(2025, 6, 30), 2.0),
    ("Бэкенд-разработчик", datetime.date(2025, 2, 16), datetime.date(2025, 6, 30), 1.5),
    ("Тестировщик", datetime.date(2025, 3, 2), datetime.date(2025, 6, 30), 1.5),
    ("Специалист по ИБ", datetime.date(2025, 2, 16), datetime.date(2025, 5, 29), 1.0),
    ("Маркетолог", datetime.date(2025, 5, 4), datetime.date(2025, 7, 31), 1.0),
    ("Технический писатель", datetime.date(2025, 5, 18), datetime.date(2025, 6, 30), 0.5),
]"""
new_av = """AVAILABILITY = [
    ("Архитектор", datetime.date(2025, 2, 3), datetime.date(2025, 6, 30), 1.0),
    ("Мобильный разработчик", datetime.date(2025, 2, 3), datetime.date(2025, 6, 30), 4.0),
    ("Бэкенд-разработчик", datetime.date(2025, 2, 17), datetime.date(2025, 6, 30), 3.5),
    ("Тестировщик", datetime.date(2025, 3, 3), datetime.date(2025, 6, 30), 4.0),
    ("Специалист по ИБ", datetime.date(2025, 2, 17), datetime.date(2025, 5, 29), 1.0),
    ("Маркетолог", datetime.date(2025, 5, 5), datetime.date(2025, 7, 31), 1.0),
    ("Технический писатель", datetime.date(2025, 5, 19), datetime.date(2025, 6, 30), 0.5),
]"""
assert old_av in s
s = s.replace(old_av, new_av, 1)

# 6. Проценты в окнах доступности + явный MaxUnits
old_setup = """    def setup_availability(self):
        for name, d1, d2, units in AVAILABILITY:
            r = self.res_by_name.get(name)
            if r is None:
                continue
            r.Availabilities.Add(datetime.datetime(d1.year, d1.month, d1.day),
                                 datetime.datetime(d2.year, d2.month, d2.day), units)"""
new_setup = """    def setup_availability(self):
        for name, d1, d2, units in AVAILABILITY:
            r = self.res_by_name.get(name)
            if r is None:
                continue
            # единицы доступности задаются в процентах (100 = 100 %)
            r.Availabilities.Add(datetime.datetime(d1.year, d1.month, d1.day),
                                 datetime.datetime(d2.year, d2.month, d2.day),
                                 units * 100.0)
            r.MaxUnits = units"""
assert old_setup in s
s = s.replace(old_setup, new_setup, 1)

open(p, "w", encoding="utf-8").write(s)
print("patched; 2026 left:", s.count("2026"))
