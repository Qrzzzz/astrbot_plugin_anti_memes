# astrbot_plugin_anti_memes

基于 AstrBot 的指定群聊用户图片自动撤回插件 / An auto-image-recall plugin for specific users in QQ groups based on AstrBot.

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
