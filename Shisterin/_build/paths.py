r"""
Единая точка определения путей проекта.

Все пути вычисляются относительно расположения этого файла, поэтому папку
проекта можно свободно переносить в любое место диска.

    <корень проекта>\
        _build\paths.py      <- этот файл
        _build\config.json   <- ФИО, группа
        Скриншоты\
        УП_<Фамилия>.mpp / .doc / .docx / .pdf
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))   # папка _build
BASE = os.path.dirname(HERE)                        # корень проекта
BUILD = HERE
SHOTS = os.path.join(BASE, "Скриншоты")
CONFIG = os.path.join(HERE, "config.json")


def load_config():
    """Читает config.json (без BOM), при ошибке возвращает пустой словарь."""
    try:
        with open(CONFIG, encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception:
        return {}


def surname():
    """Фамилия для имени файлов: из config.json, иначе первое слово ФИО."""
    cfg = load_config()
    fio = (cfg.get("fio") or "").strip()
    return (cfg.get("surname") or (fio.split()[0] if fio else "Проект")).strip()


def fio():
    cfg = load_config()
    return (cfg.get("fio") or "Фамилия Имя Отчество").strip()


def group():
    cfg = load_config()
    return (cfg.get("group") or "________").strip()


BASENAME = "УП_%s" % surname()

MPP = os.path.join(BASE, BASENAME + ".mpp")
EXP_MPP = os.path.join(BASE, BASENAME + "_эксперимент.mpp")
DOCX = os.path.join(BASE, BASENAME + ".docx")
DOC = os.path.join(BASE, BASENAME + ".doc")
PDF = os.path.join(BASE, BASENAME + ".pdf")

if __name__ == "__main__":
    print("BASE      :", BASE)
    print("BUILD     :", BUILD)
    print("SHOTS     :", SHOTS)
    print("BASENAME  :", BASENAME)
    print("MPP       :", MPP, "->", os.path.exists(MPP))
    print("EXP_MPP   :", EXP_MPP, "->", os.path.exists(EXP_MPP))
    print("DOC       :", DOC, "->", os.path.exists(DOC))
    print("DOCX      :", DOCX, "->", os.path.exists(DOCX))
    print("PDF       :", PDF, "->", os.path.exists(PDF))
    print("ФИО / группа:", fio(), "/", group())
