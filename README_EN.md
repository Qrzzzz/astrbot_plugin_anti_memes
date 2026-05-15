# Image Precision Recall Assistant

Production-oriented AstrBot plugin for rule-based image recall in QQ groups (OneBot v11 / aiocqhttp), with dry-run, diagnostics, stats, WebUI config, and command management.

## Platform
- QQ / OneBot v11 / `aiocqhttp` only

## Commands
- `/am help`
- `/am add <qq>` or `/am add <group> <qq>` or `/am add @user`
- `/am del ...`
- `/am list [group]`
- `/am dryrun on|off`
- `/am diagnose`
- Legacy compatibility: `/add_recall` `/del_recall` `/list_recall`

## Notes
- Polling fallback is experimental and disabled by default.
- Bot needs delete permission in target groups.
- Use for moderation only.
