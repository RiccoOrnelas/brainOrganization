
import openpyxl
from datetime import datetime
import urllib.request
import urllib.parse
import os

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID   = os.environ["TELEGRAM_CHAT_ID"]
EXCEL     = "brain_organization.xlsx"

DAY_MAP = {
    "Monday":"Segunda","Tuesday":"Terça","Wednesday":"Quarta",
    "Thursday":"Quinta","Friday":"Sexta","Saturday":"Sábado","Sunday":"Domingo"
}

def get_schedule():
    today = DAY_MAP[datetime.now().strftime("%A")]
    wb = openpyxl.load_workbook(EXCEL)
    ws = wb["Dados_SMS"]
    tasks = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        dia, _, categoria, tarefa, ativo = row
        if dia == today and str(ativo).upper() == "SIM":
            tasks.setdefault(categoria, []).append(tarefa)
    icons = {"Inglês":"🇺🇸","Estudos Tech":"💻","Estudos Bíblicos":"📖"}
    lines = [f"🧠 *Programação de {today}*\n"]
    for cat, icon in icons.items():
        if cat in tasks:
            lines.append(f"{icon} *{cat}*")
            lines += [f"  • {t}" for t in tasks[cat]]
            lines.append("")
    return "\n".join(lines).strip()

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }).encode()
    with urllib.request.urlopen(url, data=data) as r:
        print(r.read().decode())

if __name__ == "__main__":
    msg = get_schedule()
    print(msg)
    send_telegram(msg)
