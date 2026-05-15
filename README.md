# 图片精准撤回助手

发布级 AstrBot 插件：按“群号 + 用户 QQ”规则自动检测图片并执行撤回，支持 dry-run、诊断、统计、WebUI 配置与命令维护。

## 适用平台
- QQ / OneBot v11 / `aiocqhttp`

## 快速开始
1. 安装插件并重启 AstrBot。
2. 在 WebUI 确认插件已加载。
3. 管理员在群聊执行：`/am add <QQ号>`。
4. 可先执行：`/am dryrun on` 做演练。

## 指令
- `/am help`
- `/am status`
- `/am add <QQ号>` 或 `/am add <群号> <QQ号>` 或 `/am add @某人`
- `/am del <QQ号>` 或 `/am del <群号> <QQ号>`
- `/am list [群号]`
- `/am dryrun on|off`
- `/am diagnose`
- 兼容：`/add_recall` `/del_recall` `/list_recall`

## WebUI 配置
核心配置：`rules`、`enable_realtime_recall`、`dry_run`、`protect_bot_self`、`protect_admins`。

高级配置：`enable_polling_fallback`（实验功能，默认关闭）、`poll_interval_seconds`、`processed_cache_size`。

## 权限与边界
- 仅管理员/群管理可修改规则。
- 默认保护 bot 自身和群管理。
- 不记录图片 URL、正文、内容，只记录必要 ID 与错误类型。

## FAQ
- 撤回失败：通常是权限不足、平台拒绝、消息不可撤回。
- 未触发：检查是否命中群号、用户、图片类型和 `enable_realtime_recall`。
- 普通成员不可配置：这是安全限制。
- NapCat：若提供 OneBot v11 `delete_msg` 通常可用，需自测。
- QQ 官方机器人：本插件不支持。

## 安全声明
仅用于群管理与合规场景，禁止骚扰与滥用。

## 更新日志
见 [CHANGELOG.md](./CHANGELOG.md)。
