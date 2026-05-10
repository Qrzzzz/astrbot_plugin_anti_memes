<div align="center">

# 🛡️ AstrBot Anti Memes Plugin

### Auto-detect and recall image messages from specified QQ users in AstrBot

**QQ / OneBot V11 / aiohttp / Auto Recall / Moderation / Bilingual Docs**

[English](./README_EN.md) · [中文](./README.md) · [AstrBot](https://github.com/AstrBotDevs/AstrBot) · [Napneko API](https://napneko.github.io/api/4.18.1)

![AstrBot Plugin](https://img.shields.io/badge/AstrBot-Plugin-4B5563)
![Platform](https://img.shields.io/badge/Platform-QQ-12B7F5)
![Protocol](https://img.shields.io/badge/Protocol-OneBot%20V11-0EA5E9)
![License](https://img.shields.io/github/license/Qrzzzz/astrbot_plugin_anti_memes)

</div>

## Overview

`astrbot_plugin_anti_memes` monitors image messages sent by configured users in configured QQ groups and triggers recall automatically (with sufficient bot permissions). It is designed for moderation and group management scenarios.

> Only QQ platforms based on aiohttp / OneBot V11 are currently supported.

## Features

- 🎯 **Targeted Monitoring**: Configure targets by `group_id + qq_id`.
- 🛡️ **Dual Safeguard**: Real-time event interception plus background polling fallback.
- 👥 **Concurrent Rules**: Supports multiple users across multiple groups simultaneously.

## Installation

1. Clone or download this repository into AstrBot `data/plugins/`.
2. Ensure the directory name is exactly `astrbot_plugin_anti_memes`.
3. Restart AstrBot to load the plugin.

## Usage

### Chat Commands

- Add rule: `/add_recall <group_id> <qq_id>`
  - Example: `/add_recall 123456789 987654321`
- Remove rule: `/del_recall <group_id> <qq_id>`
  - Example: `/del_recall 123456789 987654321`
- List rules: `/list_recall`

### Notes

1. Message recall relies on the underlying `delete_msg` API; the bot must be group admin/owner.
2. This plugin is specifically adapted for NapCat / OneBot V11 QQ implementations.

## Links

- [AstrBot Repository](https://github.com/AstrBotDevs/AstrBot)
- [AstrBot Plugin Development Docs (Chinese)](https://docs.astrbot.app/dev/star/plugin-new.html)
- [Napneko API Docs](https://napneko.github.io/api/4.18.1)
