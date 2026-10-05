# DSB Bot

GitHub Actions ruft den Bot alle fünf Minuten auf. Die gespeicherten Pläne liegen im Ordner `plans/` dieses Repositories. Der Abrufstatus wird in `.plan_state.json` gespeichert, damit bereits bekannte Pläne bei späteren Läufen nicht erneut gemeldet werden.

## Einrichtung

Unter **Settings → Secrets and variables → Actions** müssen folgende Repository-Secrets angelegt werden:

- `DSB_USER`
- `DSB_PASS`

Optional:

- `DSB_TEACHER_USER` und `DSB_TEACHER_PASS` (nur gemeinsam)
- `DISCORD_WEBHOOK_WARN`
- `DISCORD_WEBHOOK_PLANS`
- `DISCORD_PING_ROLE_ID`

Ein zusätzlicher GitHub-Token ist nicht nötig. Der Workflow verwendet `GITHUB_TOKEN`; dafür hat der Workflow `contents: write` gesetzt. Der erste Lauf kann über **Actions → Fetch substitution plans → Run workflow** manuell gestartet werden. Geplante Ausführungen beginnen, sobald der Workflow auf dem Standard-Branch liegt.
