# =====================================================================
#  DISCORD-ERINNERUNGEN
#  Hier stehen alle Nachrichten. Zum Ändern einfach den Text,
#  die Uhrzeit usw. anpassen und speichern ("Commit changes").
#
#  alle_tage:  1 = täglich, 2 = alle 2 Tage,
#             14 = alle 2 Wochen, 28 = alle 4 Wochen
#  uhrzeit:   immer in UTC
#  ab:        Startdatum im Format JAHR-MONAT-TAG
#  bild:      Dateiname im Repo (Groß-/Kleinschreibung beachten!)
#             oder None für kein Bild
# =====================================================================

NACHRICHTEN = [
    {"nr": 1,  "text": "😃 ARENAAAAA 😃",
     "alle_tage": 1,  "uhrzeit": "23:50", "ab": "2026-11-13", "bild": "arena.webp"},

    {"nr": 2,  "text": "Bear Trap 1 starts in 10 minutes",
     "alle_tage": 2,  "uhrzeit": "13:50", "ab": "2026-11-14", "bild": "bt10min.gif"},
    {"nr": 3,  "text": "Bear Trap 1 NOW!!",
     "alle_tage": 2,  "uhrzeit": "13:59", "ab": "2026-11-14", "bild": "bt1now.gif"},
    {"nr": 4,  "text": "Bear Trap 2 starts in 10 minutes",
     "alle_tage": 2,  "uhrzeit": "18:50", "ab": "2026-11-14", "bild": "bt10min.gif"},
    {"nr": 5,  "text": "Bear Trap 2 NOW!!",
     "alle_tage": 2,  "uhrzeit": "18:59", "ab": "2026-11-14", "bild": "bt2now.gif"},

    {"nr": 6,  "text": "Foundry 14 UTC starts in 10 minutes",
     "alle_tage": 14, "uhrzeit": "13:50", "ab": "2026-11-15", "bild": None},
    {"nr": 7,  "text": "Foundry 14 UTC NOW!! Burn them all noobs🔥🔥",
     "alle_tage": 14, "uhrzeit": "13:59", "ab": "2026-11-15", "bild": "foundry.gif"},
    {"nr": 8,  "text": "Foundry 19 UTC starts in 10 minutes",
     "alle_tage": 14, "uhrzeit": "18:50", "ab": "2026-11-15", "bild": None},
    {"nr": 9,  "text": "Foundry 19 UTC NOW!! Burn them all noobs🔥🔥",
     "alle_tage": 14, "uhrzeit": "18:59", "ab": "2026-11-15", "bild": "foundry.gif"},

    {"nr": 10, "text": "Crazy Hoe in 20 minutes! Empty your city!",
     "alle_tage": 14, "uhrzeit": "18:40", "ab": "2026-11-17", "bild": "CJ20min.gif"},
    {"nr": 11, "text": "Crazy Hoe NOW👹👹",
     "alle_tage": 14, "uhrzeit": "18:59", "ab": "2026-11-17", "bild": None},
    {"nr": 12, "text": "Crazy Hoe in 20 minutes! Empty your city!",
     "alle_tage": 14, "uhrzeit": "13:40", "ab": "2026-11-19", "bild": "CJ20min.gif"},
    {"nr": 13, "text": "Crazy Hoe NOW👹👹",
     "alle_tage": 14, "uhrzeit": "13:59", "ab": "2026-11-19", "bild": None},

    {"nr": 14, "text": "Borders open in 1 hour - SHIELD UP OR BURN🔥🔥",
     "alle_tage": 28, "uhrzeit": "09:00", "ab": "2026-12-05", "bild": None},
    {"nr": 15, "text": "Borders open in 10 minutes - SHIELD UP OR BURN🔥🔥",
     "alle_tage": 28, "uhrzeit": "09:50", "ab": "2026-12-05", "bild": "burn.gif"},

    {"nr": 16, "text": "Castle battle starts in 30 minutes - teleport to castle!",
     "alle_tage": 14, "uhrzeit": "11:30", "ab": "2026-11-21", "bild": None},
    {"nr": 17, "text": "Castle battle starts in 15 minutes! Set up your attack and defense squads - dont join with wrong marches!!",
     "alle_tage": 28, "uhrzeit": "11:45", "ab": "2026-12-05", "bild": None},
    {"nr": 18, "text": "Castle battle NOW!!",
     "alle_tage": 14, "uhrzeit": "11:59", "ab": "2026-11-21", "bild": None},

    {"nr": 19, "text": "SHIELD UP OR BURN🔥🔥",
     "alle_tage": 28, "uhrzeit": "17:01", "ab": "2026-12-05", "bild": None},
    {"nr": 20, "text": "Remember to SHIELD UP !!",
     "alle_tage": 28, "uhrzeit": "20:00", "ab": "2026-12-05", "bild": "burn.gif"},
]

# =====================================================================
#  Ab hier nichts ändern :)
# =====================================================================
import json, os, subprocess, time
from datetime import datetime, timedelta, timezone, date

FENSTER = timedelta(minutes=90)    # so weit schaut ein Lauf nach vorne
ZU_SPAET = timedelta(minutes=20)   # später als das wird nicht mehr gesendet


def jetzt():
    if os.environ.get("TEST_JETZT"):
        return datetime.fromisoformat(os.environ["TEST_JETZT"]).replace(tzinfo=timezone.utc)
    return datetime.now(timezone.utc)


def faellig(n, tag):
    tage = (tag - date.fromisoformat(n["ab"])).days
    return tage >= 0 and tage % n["alle_tage"] == 0


def zielzeit(n, tag):
    h, m = map(int, n["uhrzeit"].split(":"))
    return datetime(tag.year, tag.month, tag.day, h, m, tzinfo=timezone.utc)


def senden(n):
    if os.environ.get("TROCKEN"):
        print(f"[TEST] würde senden: Nr. {n['nr']} ({n['uhrzeit']}) {n['text']} | Bild: {n['bild']}")
        return
    cmd = ["curl", "-sS", "--fail-with-body",
           "--form-string", "payload_json=" + json.dumps({"content": n["text"]})]
    if n["bild"]:
        if os.path.exists(n["bild"]):
            cmd += ["-F", f"files[0]=@{n['bild']}"]
        else:
            print(f"WARNUNG: Bild '{n['bild']}' nicht im Repo gefunden – sende ohne Bild.")
    cmd.append(os.environ["DISCORD_WEBHOOK"])
    for versuch in range(3):
        if subprocess.run(cmd).returncode == 0:
            print(f"Gesendet: Nr. {n['nr']}")
            return
        time.sleep(5)
    raise SystemExit(f"FEHLER: Nr. {n['nr']} konnte nicht gesendet werden.")


def main():
    # Manueller Test über "Run workflow": eine Nachricht sofort senden
    if os.environ.get("EVENT") == "workflow_dispatch":
        nr = int(os.environ.get("TEST_NR") or 1)
        senden(next(n for n in NACHRICHTEN if n["nr"] == nr))
        return

    # Geplanter Lauf: Startzeit aus dem Zeitplan ermitteln
    minute, stunde = map(int, os.environ["CRON"].split()[:2])
    nun = jetzt()
    start = nun.replace(hour=stunde, minute=minute, second=0, microsecond=0)
    if start > nun + timedelta(minutes=5):
        start -= timedelta(days=1)

    plan = []
    for tag in (start.date(), start.date() + timedelta(days=1)):
        for n in NACHRICHTEN:
            z = zielzeit(n, tag)
            if start <= z < start + FENSTER and faellig(n, tag):
                plan.append((z, n))
    plan.sort(key=lambda x: (x[0], x[1]["nr"]))

    if not plan:
        print("Jetzt ist nichts fällig.")
    for z, n in plan:
        warten = (z - jetzt()).total_seconds()
        if warten > 0 and not os.environ.get("TROCKEN"):
            print(f"Warte {int(warten)} Sekunden bis {n['uhrzeit']} UTC (Nr. {n['nr']}) …")
            time.sleep(warten)
        elif warten < -ZU_SPAET.total_seconds():
            print(f"Zu spät für Nr. {n['nr']} – übersprungen.")
            continue
        senden(n)
        time.sleep(2)


if __name__ == "__main__":
    main()
