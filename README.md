# Daily Planner Bot

A Python bot that reads my weekly schedule from a spreadsheet and sends me a daily briefing on Telegram every morning. No servers, no cost — runs entirely on GitHub Actions.

This is a personal productivity tool I built and use daily.

---

## How it works

1. GitHub Actions triggers the script every day at 07:00 AM (Brasília time)
2. The script opens a local `.xlsx` file and finds the tasks for today
3. It groups them by category, formats the message with Markdown, and sends it to my Telegram

The message looks something like this:

```
Tarefas por ordem de Prioridade:

🙏 Devocional
📖 Palavra

🎯 The three of the day:
  • Aula de Inglês online (40 min)
  • Caça de aplicações (40 min)
  • LeetCode (1 hora)

⏳ With the rest of the time:
  • System Designer (40 min)
  • Atividades open english (25 min)
  • Bible is Open (1 hora)
  • Mock interview IA (25 min)
```

---

## Tech

- **Python 3.11**
- **openpyxl** — reads the `.xlsx` spreadsheet
- **urllib** — sends the Telegram message (no external HTTP library needed)
- **GitHub Actions** — schedules and runs the script daily
- **Telegram Bot API** — delivers the message

---

## Spreadsheet structure

The file `brain_organization.xlsx` has a sheet called `Dados_SMS` with this format:

| Dia | (unused) | Categoria | Tarefa | Ativo |
|---|---|---|---|---|
| Segunda | Monday | Devocional | Palavra | SIM |
| Segunda | Monday | The three of the day: | Aula de Inglês online (40 min) | SIM |
| Segunda | Monday | With the rest of the time: | System Designer (40 min) | SIM |

- **Dia** — day of the week in Portuguese
- **Categoria** — message section (used to group tasks, in order of priority)
- **Tarefa** — the task description
- **Ativo** — `SIM` to include, anything else to skip

---

## GitHub Actions workflow

```yaml
on:
  schedule:
    - cron: '0 10 * * *'  # 07:00 AM Brasília (UTC-3)
  workflow_dispatch:        # can also be triggered manually
```

The `workflow_dispatch` trigger is useful for testing without waiting for the scheduled run.

---

## Setup

**1. Create a Telegram bot**
Talk to [@BotFather](https://t.me/BotFather) on Telegram, create a bot, and copy the token.

**2. Get your Chat ID**
Send a message to your bot, then open:
```
https://api.telegram.org/bot<TOKEN>/getUpdates
```
Your `chat_id` will be in the response.

**3. Add secrets to GitHub**
In your repository: `Settings → Secrets → Actions`

| Secret | Value |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Your bot token |
| `TELEGRAM_CHAT_ID` | Your chat ID |

**4. Add your spreadsheet**
Put `brain_organization.xlsx` in the root of the repository following the structure above.

---

## Known limitations

- No error handling yet — a malformed row in the spreadsheet will break the script silently
- The day mapping assumes the GitHub runner returns weekday names in English (which it does on `ubuntu-latest`, but worth noting)
- Sheet name and spreadsheet filename are hardcoded

These are on the roadmap to improve.
