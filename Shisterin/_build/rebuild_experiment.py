"""Пересобрать эксперимент из актуального базового .mpp (с совещаниями)."""
import datetime, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
import paths
from reshoot_fixed import Shot, say

BASE = os.path.join(paths.BASE, "УП_Шистерин.mpp")
EXP = os.path.join(paths.BASE, "УП_Шистерин_эксперимент.mpp")

s = Shot()  # открывает paths.MPP (текущий) — переоткроем базу
try:
    s.app.FileClose(0)
    s.app.FileOpen(BASE)
    p = s.app.ActiveProject
    by_name = {r.Name: r for r in p.Resources}

    def snap():
        return {"finish": str(p.ProjectFinish), "cost": float(p.Cost),
                "work_MR": float(by_name["Мобильный разработчик"].Work),
                "work_TS": float(by_name["Тестировщик"].Work)}
    res = {"base": snap()}
    say("base", res["base"]["finish"][:10], res["base"]["cost"])

    for cal, base in (("Календарь МР (апрель)", "Стандартный"), ("Календарь ТС (апрель)", "Стандартный")):
        try: s.app.BaseCalendarCreate(cal, base)
        except Exception as e: say("cal create", cal, str(e)[:60])
    mr, ts = by_name["Мобильный разработчик"], by_name["Тестировщик"]
    try: mr.BaseCalendar = "Календарь МР (апрель)"
    except Exception as e: say("mr cal", e)
    try: ts.BaseCalendar = "Календарь ТС (апрель)"
    except Exception as e: say("ts cal", e)
    try:
        s.app.ResourceCalendarEditDays(p.Name, "Мобильный разработчик",
            datetime.datetime(2025,4,1), datetime.datetime(2025,4,30), 6, False)
    except Exception as e: say("mr days", e)
    try:
        s.app.ResourceCalendarEditDays(p.Name, "Тестировщик",
            datetime.datetime(2025,4,1), datetime.datetime(2025,4,30), 6, True, False, "09:00", "13:00")
    except Exception as e: say("ts days", e)
    res["after_cal"] = snap(); say("after cal", res["after_cal"]["finish"][:10], res["after_cal"]["cost"])

    n=0
    for i in range(1,p.Tasks.Count+1):
        t=p.Tasks.Item(i); nm=str(t.ResourceNames)
        if "Мобильный разработчик" in nm or "Тестировщик" in nm:
            t.Type=0; n+=1
    res["after_fixed_units"]=snap(); res["tasks_switched"]=n
    say("fixed units", n, res["after_fixed_units"]["finish"][:10], res["after_fixed_units"]["cost"])

    try:
        mr.PayRates.Add(datetime.datetime(2025,4,1), 3600, 5600)
        res["rate"]="ok"
    except Exception as e:
        res["rate"]=str(e)[:120]; say("rate err", res["rate"])
    res["after_rate"]=snap()
    say("after rate", res["after_rate"]["finish"][:10], res["after_rate"]["cost"], "delta", int(res["after_rate"]["cost"]-res["after_fixed_units"]["cost"]))

    if os.path.exists(EXP): os.remove(EXP)
    p.SaveAs(EXP)
    with open(os.path.join(paths.BUILD,"experiment.json"),"w",encoding="utf-8") as f:
        json.dump(res,f,ensure_ascii=False,indent=2)
    say("saved", EXP)
finally:
    try: s.app.FileQuit()
    except Exception: pass
