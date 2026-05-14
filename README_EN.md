# Image Precision Recall Assistant (AstrBot Plugin)

## Overview
`astrbot_plugin_anti_memes` monitors image messages from configured users in configured QQ groups, then calls OneBot v11 `delete_msg` to recall them (subject to bot permissions and adapter behavior).

## Supported Platform
- Only: `aiocqhttp` (QQ / OneBot v11).

## Functional Boundary
- Handles **image messages only**.
- Does not process text/voice/video messages.
- Recall success depends on:
  - bot admin/owner capability in target groups;
  - adapter support and policy for `delete_msg`.
- This release uses **real-time event detection only** (no active polling fallback).

## Installation
1. Place this repo under AstrBot plugins directory (e.g. `data/plugins/astrbot_plugin_anti_memes`).
2. Restart AstrBot.
3. Confirm plugin is loaded in plugin manager.

## WebUI Configuration
Managed via AstrBot official plugin config schema (`_conf_schema.json`):
- `targets`: dict mapping `group_id` (string) -> list of `user_id` (string).
- `enable_realtime_recall`: enable real-time detection (`true` by default).
- `enable_polling_fallback`: kept as config key, default `false` (not active in current implementation).
- `poll_interval_seconds`: polling interval key (not used in real-time-only mode).
- `processed_cache_size`: processed message ID cache limit.

## Commands
- `/add_recall <group_id> <qq_id>`
- `/del_recall <group_id> <qq_id>`
- `/list_recall`

> IDs must be numeric strings.

## Permission Requirements
- Rule-management commands are restricted to administrators (or equivalent privileged callers).
- Bot must have sufficient group privileges to recall messages.

## FAQ
### Why recall can fail?
Bot lacks privilege, message is not recallable/expired, API rejected, or message no longer exists.

### Why rules persist after restart?
Rules are saved in AstrBot plugin config, not in plugin source directory.

### Why polling fallback is not recommended?
Polling requires stable bot API access, stronger rate-limit handling, and adapter guarantees. Real-time mode is safer for marketplace-grade stability.

### Does it support NapCat / OneBot v11?
It should work where OneBot v11 `delete_msg` is supported. Validate in your own deployment.

## Safety & Compliance
Use only for moderation and group governance. Do not abuse or violate platform rules. Logs avoid storing image content, image URLs, or message body.

## Changelog
- `1.0.0`: marketplace-readiness refactor with normalized config, permission boundary, robust event flow, and ordered cache.
