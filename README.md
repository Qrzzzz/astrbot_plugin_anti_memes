<div align="center">

# 🛡️ AstrBot Anti Memes Plugin

### 基于 AstrBot 的 QQ 指定用户图片自动检测与撤回插件

**QQ / OneBot V11 / aiohttp / 自动撤回 / 群组管理 / 双语文档**

[中文](./README.md) · [English](./README_EN.md) · [AstrBot](https://github.com/AstrBotDevs/AstrBot) · [Napneko API](https://napneko.github.io/api/4.18.1)

![AstrBot Plugin](https://img.shields.io/badge/AstrBot-Plugin-4B5563)
![Platform](https://img.shields.io/badge/Platform-QQ-12B7F5)
![Protocol](https://img.shields.io/badge/Protocol-OneBot%20V11-0EA5E9)
![License](https://img.shields.io/github/license/Qrzzzz/astrbot_plugin_anti_memes)

</div>

## 项目简介

`astrbot_plugin_anti_memes` 用于在 QQ 群聊中自动检测指定用户发送的图片消息，并在满足权限条件时自动触发撤回，适用于内容管理与群组秩序维护场景。

> 当前仅支持基于 QQ 的 aiohttp / OneBot V11 平台实现。

## 功能特性

- 🎯 **精准监控**：支持按「群号 + QQ 号」配置目标用户。
- 🛡️ **双重保障**：实时事件检测 + 后台轮询兜底，降低漏检概率。
- 👥 **多目标并发**：支持多个群、多个用户规则并行执行。

## 安装方法

1. 将本仓库克隆或下载到 AstrBot 的 `data/plugins/` 目录。
2. 确保文件夹名为 `astrbot_plugin_anti_memes`。
3. 重启 AstrBot 主进程加载插件。

## 使用说明

### 聊天指令

- 添加监控：`/add_recall <群号> <QQ号>`
  - 示例：`/add_recall 123456789 987654321`
- 移除监控：`/del_recall <群号> <QQ号>`
  - 示例：`/del_recall 123456789 987654321`
- 查看规则：`/list_recall`

### 注意事项

1. 撤回调用的是底层 `delete_msg` API，机器人需在目标群拥有管理员或群主权限。
2. 本插件仅适配 NapCat / OneBot V11 的 QQ 平台实现。

## 相关链接

- [AstrBot 项目主页](https://github.com/AstrBotDevs/AstrBot)
- [AstrBot 插件开发文档（中文）](https://docs.astrbot.app/dev/star/plugin-new.html)
- [Napneko API 文档](https://napneko.github.io/api/4.18.1)
