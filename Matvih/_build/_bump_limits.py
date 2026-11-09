import sys
p='build_project.py'
s=open(p,encoding='utf-8').read()
s=s.replace('("ML-инженер", "МР", "Разработка", 2.0, 2200, 3500),','("ML-инженер", "МР", "Разработка", 3.0, 2200, 3500),')
s=s.replace('("CV-инженер", "БР", "Разработка", 1.5, 2100, 3300),','("CV-инженер", "БР", "Разработка", 2.0, 2100, 3300),')
s=s.replace('("Тестировщик", "ТС", "Тестирование", 1.5, 1700, 2600),','("Тестировщик", "ТС", "Тестирование", 2.0, 1700, 2600),')
s=s.replace('("ML-инженер", datetime.date(2025, 2, 3), datetime.date(2025, 6, 30), 2.0),','("ML-инженер", datetime.date(2025, 2, 3), datetime.date(2025, 6, 30), 3.0),')
s=s.replace('("CV-инженер", datetime.date(2025, 2, 17), datetime.date(2025, 6, 30), 1.5),','("CV-инженер", datetime.date(2025, 2, 17), datetime.date(2025, 6, 30), 2.0),')
s=s.replace('("Тестировщик", datetime.date(2025, 3, 3), datetime.date(2025, 6, 30), 1.5),','("Тестировщик", datetime.date(2025, 3, 3), datetime.date(2025, 6, 30), 2.0),')
open(p,'w',encoding='utf-8').write(s)
print('ok')
