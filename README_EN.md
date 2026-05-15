# 🛡️ Image Precision Recall Assistant (`astrbot_plugin_anti_memes`)

A production-oriented AstrBot plugin for QQ group moderation on **OneBot v11 / aiocqhttp**. It detects image messages from configured users in configured groups and applies rule-based actions (recall / dry-run), with WebUI config and command management.

---

## ✨ Highlights

- 🎯 **Precise scope control**: target by group + user + image messages only.
- 🧠 **Rule-based config**: modern `rules` model with legacy `targets` compatibility.
- 🧪 **Dry-run mode**: verify behavior safely before real recalls.
- 🧰 **Diagnostics support**: quick checks for platform/permission/config issues.
- 🔒 **Safe defaults**: protect bot self and admins by default.

---

## 🧩 Supported Platform

- ✅ QQ / OneBot v11 / `aiocqhttp`
- ⚠️ Other adapters are not guaranteed

---

## 🚀 Quick Start

1. Install the plugin and restart AstrBot.
2. Confirm plugin is loaded in WebUI.
3. Run `/am help` in a group.
4. Add a rule as admin: `/am add <qq>` (uses current group by default).
5. Start with dry-run: `/am dryrun on`.
6. Turn off dry-run after validation: `/am dryrun off`.

---

## 💬 Commands

### Main command group

- `/am help`
- `/am status`
- `/am add <qq>`
- `/am add <group> <qq>`
- `/am add @user`
- `/am del <qq>`
- `/am del <group> <qq>`
- `/am list [group]`
- `/am dryrun on|off`
- `/am diagnose`

### Legacy compatibility

- `/add_recall <group> <qq>`
- `/del_recall <group> <qq>`
- `/list_recall`

> ℹ️ Rule management commands require admin/moderator privileges.

---

## ⚙️ WebUI Config Notes

### Core options

- `rules`
- `enable_realtime_recall`
- `dry_run`
- `protect_bot_self`
- `protect_admins`

### Advanced options

- `enable_polling_fallback` (experimental, disabled by default)
- `poll_interval_seconds`
- `processed_cache_size`
- `stop_event_after_recall`

---

## 🔐 Security & Boundaries

- Admin/moderator-only management operations.
- No logging of image URL/content or full message body.
- Logs keep only minimal IDs and error categories for diagnostics.

---

## ❓ FAQ

- **Recall failed?** Usually permission, platform rejection, or recall window issues.
- **Not triggered?** Check group/user matching, image presence, and config flags.
- **NapCat support?** Usually works if OneBot v11 + `delete_msg` is stable.
- **Official QQ bot support?** Not supported.

---

## 📜 Compliance

Use this plugin for legitimate moderation and compliance scenarios only.

---

## 📝 Changelog

See [CHANGELOG.md](./CHANGELOG.md).
