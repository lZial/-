import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')

# mapping by key phrases -> (new number prefix or None)
MAP = [
    ('Введение', None),
    ('Обзор предметной области', '1'),
    ('Назначение и области применения', '1.1'),
    ('Целевая аудитория', '1.2'),
    ('Обзор существующих решений', '1.3'),
    ('Анализ рынка и конкурентов', '1.3'), # if variant
    ('Необходимость реализации', '1.4'),
    ('Архитектура и интеграции', '1.5'),
    ('Нормативное регулирование', '1.6'),
    ('Анализ модели жизненного цикла', '2'),
    ('Понятие жизненного цикла', '2.1'),
    ('Обзор моделей жизненного цикла', '2.2'),
    ('Сравнительный анализ моделей', '2.3'),
    ('Этапы итерационной модели', '2.4'),
    ('Этапы модели жизненного цикла', '2.4'),
    ('Области применения итерационной', '2.5'),
    ('Преимущества и недостатки', '2.6'),
    ('Обоснование выбора', '2.7'),
    ('Основные этапы и задачи проекта', '3'),
    ('Состав этапов проекта', '3.1'),
    ('Характеристика этапов', '3.2'),
    ('Описание этапов', '3.2'),
    ('Перечень задач проекта', '3.3'),
    ('Вехи проекта', '3.4'),
    ('Связи, ограничения и календарь', '3.5'),
    ('Повторяющаяся задача', '3.6'),
    ('Реализация проекта', '4'),
    ('Эксперименты с копией', '4.17'),
    ('Риски проекта', '5'),
    ('Понятие и классификация рисков', '5.1'),
    ('Процесс управления рисками', '5.2'),
    ('Реестр рисков проекта', '5.3'),
    ('Итоговые отчёты', '6'),
    ('Заключение', '7'),
    ('Список использованных источников', '8'),
]

def fix(path):
    s=open(path,encoding='utf-8').read()
    # first fix syntax: heading(doc, ""1  ...") or heading(doc, ""1.4 ...")
    s=re.sub(r'heading\(doc,\s*""(\d+(?:\.\d+)?)\s+([^"]+)"', r'heading(doc, "\1 \2"', s)
    # also cases like ""1.4
    s=s.replace('""','"')
    # now normalize by content
    def repl(m):
        text=m.group(1)
        # strip existing leading number
        body=re.sub(r'^\d+(?:\.\d+)?\s+','',text).strip()
        num=None
        for key,n in MAP:
            if key.lower() in body.lower() or key.lower() in text.lower():
                num=n; body_final=body if body else text; break
        else:
            # keep as-is (Приложение etc.)
            if 'Приложение' in text or text.strip()=='Введение':
                return m.group(0)
            return m.group(0)
        if num is None:
            return 'heading(doc, "%s", %s)' % (body, m.group(2))
        return 'heading(doc, "%s %s", %s)' % (num, body, m.group(2))
    s=re.sub(r'heading\(doc,\s*"([^"]+)",\s*(\d)\)', repl, s)
    open(path,'w',encoding='utf-8').write(s)
    print('fixed',path)

for root in [r'D:\UP_MobileBank\_build', r'D:\UP_NeuralDefects\_build']:
    for fn in ('make_report2.py','make_report2_part2.py'):
        fix(os.path.join(root,fn))
