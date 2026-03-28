# astrbot_plugin_anti_memes

基于 AstrBot 的指定群聊用户图片自动撤回插件 / An auto-image-recall plugin for specific users in QQ groups based on AstrBot.

> 本插件基于 Gemini 3.1 Pro 进行辅助设计与编辑，如有功能缺漏或异常行为，欢迎提交 Issue 或自行优化实现。

> [!NOTE]
> This repo is a plugin for [AstrBot](https://github.com/AstrBotDevs/AstrBot).
> 
> [AstrBot](https://github.com/AstrBotDevs/AstrBot) is an agentic assistant for both personal and group conversations. It can be deployed across dozens of mainstream instant messaging platforms, including QQ, Telegram, Feishu, DingTalk, Slack, LINE, Discord, Matrix, etc. In addition, it provides a reliable and extensible conversational AI infrastructure for individuals, developers, and teams. Whether you need a personal AI companion, an intelligent customer support agent, an automation assistant, or an enterprise knowledge base, AstrBot enables you to quickly build AI applications directly within your existing messaging workflows.

## ✨ 功能特性 (Features)

- 🎯 **精准打击**：支持设定特定群聊中的特定 QQ 用户，一旦检测到其发送图片（`[CQ:image]` 或纯图片组件）立即触发撤回。
- 🛡️ **双重保障**：采用“实时事件拦截 + 后台 10 秒轮询兜底”双轨机制，极大降低漏判率。
- 👥 **多群多目标并发**：支持同时监控 N 个群聊中的 N 个不同成员。加入防风控休眠机制，避免频繁调用 API 被限制。

## 📦 安装 (Installation)

将本仓库克隆或下载解压至 AstrBot 的 `data/plugins/` 目录下，确保文件夹名称与插件名（`astrbot_plugin_anti_memes`）完全一致，随后重启 AstrBot 主进程即可。

## 🛠️ 使用方法 (Usage)

本插件通过在 QQ 群聊中直接对机器人发送指令来进行配置与动态管理。

### 聊天指令配置
- **添加监控**：`/add_recall <群号> <QQ号>`
  - *示例*：`/add_recall 123456789 987654321`
- **移除监控**：`/del_recall <群号> <QQ号>`
  - *示例*：`/del_recall 123456789 987654321`
- **查看列表**：`/list_recall`
  - *作用*：由机器人返回当前正在执行的所有群号与用户映射规则。

> **⚠️ 注意事项**：
> 1. 由于撤回操作调用的是底层 `delete_msg` API，**机器人必须在目标群聊中拥有“管理员”或“群主”权限**，否则撤回指令将被腾讯服务器拒绝。
> 2. 本插件专门适配基于 NapCat / OneBot V11 协议的 QQ 平台实现。

## 📚 支持与文档 (Supports)

- [AstrBot Repo](https://github.com/AstrBotDevs/AstrBot)
- [AstrBot Plugin Development Docs (Chinese)](https://docs.astrbot.app/dev/star/plugin-new.html)
- [AstrBot Plugin Development Docs (English)](https://docs.astrbot.app/en/dev/star/plugin-new.html)

> This plugin was assisted and edited based on Gemini 3.1 Pro. If there are any missing features or unexpected behaviors, feel free to submit an issue or improve it yourself.

An auto-image-recall plugin for specific users in QQ groups based on AstrBot.

> [!NOTE]
> This repo is a plugin for [AstrBot](https://github.com/AstrBotDevs/AstrBot).
> 
> [AstrBot](https://github.com/AstrBotDevs/AstrBot) is an agentic assistant for both personal and group conversations. It can be deployed across dozens of mainstream instant messaging platforms, including QQ, Telegram, Feishu, DingTalk, Slack, LINE, Discord, Matrix, etc. In addition, it provides a reliable and extensible conversational AI infrastructure for individuals, developers, and teams. Whether you need a personal AI companion, an intelligent customer support agent, an automation assistant, or an enterprise knowledge base, AstrBot enables you to quickly build AI applications directly within your existing messaging workflows.

## ✨ Features

- 🎯 **Precise Targeting**: Supports specifying particular users in specific group chats. Once an image message (`[CQ:image]` or native image component) is detected, it will be recalled immediately.
- 🛡️ **Dual Protection Mechanism**: Combines real-time event interception with a 10-second background polling fallback, significantly reducing missed detections.
- 👥 **Multi-Group & Multi-Target Concurrency**: Supports monitoring multiple users across multiple groups simultaneously. Includes rate-limit-safe sleep mechanisms to avoid API restrictions.

## 📦 Installation

Clone or download this repository into the `data/plugins/` directory of AstrBot. Make sure the folder name exactly matches the plugin name (`astrbot_plugin_anti_memes`), then restart the AstrBot main process.

## 🛠️ Usage

This plugin is configured and managed dynamically via commands sent to the bot directly within QQ group chats.

### Chat Commands
- **Add monitoring**: `/add_recall <group_id> <qq_id>`
  - *Example*: `/add_recall 123456789 987654321`
- **Remove monitoring**: `/del_recall <group_id> <qq_id>`
  - *Example*: `/del_recall 123456789 987654321`
- **List rules**: `/list_recall`
  - *Description*: The bot will return all active group-user mapping rules currently in effect.

> **⚠️ Notes**:
> 1. The recall operation relies on the underlying `delete_msg` API. The bot **must have administrator or owner privileges** in the target group, otherwise the recall request will be rejected by Tencent servers.
> 2. This plugin is specifically designed for QQ platforms based on the NapCat / OneBot V11 protocol.

## 📚 Support & Documentation

- [AstrBot Repo](https://github.com/AstrBotDevs/AstrBot)
- [AstrBot Plugin Development Docs (Chinese)](https://docs.astrbot.app/dev/star/plugin-new.html)
- [AstrBot Plugin Development Docs (English)](https://docs.astrbot.app/en/dev/star/plugin-new.html)
