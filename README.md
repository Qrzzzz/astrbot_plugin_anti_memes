# 🛡️ 图片精准撤回助手（astrbot_plugin_anti_memes）

一个面向 **AstrBot v4.16+** 的 QQ 群管理插件：根据「群号 + 用户 QQ」规则自动检测图片并执行处理（撤回 / 演练），支持 WebUI 配置、命令维护、诊断与基础统计。

---

## ✨ 功能概览

- 🎯 **精准命中**：只处理目标群、目标用户、目标消息类型（图片）。
- 🧠 **规则化管理**：支持新版 `rules`，兼容旧版 `targets` 自动迁移读取。
- 🧪 **Dry-Run 演练**：先验证命中逻辑，不真正撤回。
- 🧰 **可诊断**：支持快速排查平台、权限、配置问题。
- 🔒 **安全默认**：默认保护 Bot 自身与群管理成员。
- 🧱 **工程化结构**：核心逻辑模块化，便于维护与扩展。

---

## 🧩 适用平台

- ✅ QQ / OneBot v11 / `aiocqhttp`
- ⚠️ 其他平台或适配器不保证可用

---

## 🚀 快速开始

1. 安装插件并重启 AstrBot。
2. 在 WebUI 确认插件已加载。
3. 先在群聊执行：`/am help` 检查命令可用。
4. 管理员添加规则：`/am add <QQ号>`（默认当前群）。
5. 建议先开启演练：`/am dryrun on`。
6. 验证命中后再关闭演练：`/am dryrun off`。

---

## 💬 指令说明

### 主指令组

- `/am help`
- `/am status`
- `/am add <QQ号>`
- `/am add <群号> <QQ号>`
- `/am add @某人`
- `/am del <QQ号>`
- `/am del <群号> <QQ号>`
- `/am list [群号]`
- `/am dryrun on|off`
- `/am diagnose`

### 兼容旧指令

- `/add_recall <群号> <QQ号>`
- `/del_recall <群号> <QQ号>`
- `/list_recall`

> ℹ️ 规则管理类操作需要管理员权限；普通成员无法修改规则是预期安全行为。

---

## ⚙️ WebUI 配置建议

### 核心配置（常用）

- `rules`：规则列表（推荐通过模板项维护）
- `enable_realtime_recall`：是否开启实时检测
- `dry_run`：演练模式
- `protect_bot_self`：保护 Bot 自身消息
- `protect_admins`：保护群主/管理员

### 高级配置（谨慎调整）

- `enable_polling_fallback`：轮询兜底（实验功能，默认关闭）
- `poll_interval_seconds`：轮询间隔
- `processed_cache_size`：去重缓存大小
- `stop_event_after_recall`：撤回成功后是否停止事件传播

---

## 🔐 权限与安全边界

- 仅管理员/群管理可进行配置操作。
- 默认不处理 Bot 自身与管理成员消息（可配置关闭）。
- 不记录图片 URL、图片内容或消息正文。
- 日志仅保留必要 ID 与错误类型，便于诊断与审计。

---

## 🧭 常见问题（FAQ）

### 1) 为什么撤回失败？

常见原因：
- Bot 在目标群缺少管理权限
- 平台/适配器拒绝 `delete_msg`
- 消息已过可撤回窗口或已被处理

可用 `/am diagnose` 辅助排查。

### 2) 为什么没有触发？

请检查：
- 是否命中目标群、目标用户
- 消息是否确实包含图片
- `enable_realtime_recall` 是否开启
- 是否被保护策略（bot/admin）拦截

### 3) 为什么普通成员不能配置？

这是安全设计，防止误操作或滥用。

### 4) 支持 NapCat 吗？

若 NapCat 提供稳定 OneBot v11 且支持 `delete_msg`，通常可用；请结合实际环境自测。

### 5) 支持 QQ 官方机器人吗？

不支持。本插件定位于 QQ / OneBot v11 / `aiocqhttp` 生态。

---

## 📜 安全与合规声明

本插件仅用于群管理和合规治理场景。请勿用于骚扰、滥用或侵犯他人权益的行为。

---

## 📝 更新日志与贡献

- 更新记录：见 [CHANGELOG.md](./CHANGELOG.md)
- 欢迎通过 Issue / PR 提交反馈与改进建议
