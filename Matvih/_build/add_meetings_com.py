"""Добавить серию совещаний как задачи (COM, без UI диалога)."""
import datetime, os, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'.')
import paths
from reshoot_fixed import Shot, say

TARGET = os.path.join(paths.BASE, f"УП_{__import__('json').load(open(os.path.join(paths.BUILD,'config.json'),encoding='utf-8-sig')).get('surname','Матвих')}.mpp")
# first friday 2025-02-07, last 2025-08-15
dates = []
d = datetime.date(2025,2,7)
while d <= datetime.date(2025,8,15):
    dates.append(d); d += datetime.timedelta(days=7)

paths.MPP = TARGET
s=Shot()
try:
    p=s.app.ActiveProject
    # remove existing meetings if rerun
    to_del=[t.ID for t in p.Tasks if 'Совещание' in str(t.Name)]
    for tid in sorted(to_del, reverse=True):
        try: p.Tasks.UniqueID  # noop
        except: pass
    # insert at top
    sumt = p.Tasks.Add('Совещание', 1)
    sumt.OutlineLevel = 1
    # make following as children by adding after and indenting? easier: add then OutlineIndent
    created=[]
    for i,dt in enumerate(dates,1):
        t = p.Tasks.Add(f'Совещание {i}', 1+i)
        t.Duration = '1h'
        t.Start = datetime.datetime(dt.year,dt.month,dt.day,9,0,0)
        created.append(t)
    # indent children
    try:
        # select children
        for i in range(2, 2+len(dates)):
            p.Tasks.Item(i).OutlineIndent()
    except Exception as e:
        say('indent err', e)
    say('tasks', p.Tasks.Count, 'meetings', len([t for t in p.Tasks if 'Совещание' in str(t.Name)]))
    s.app.FileSave(); say('saved')
finally:
    try: s.app.FileQuit()
    except: pass
