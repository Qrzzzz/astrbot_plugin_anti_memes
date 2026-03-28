import os
import json
import asyncio
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

# 定义配置文件的路径，存放在当前插件所在目录下
PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(PLUGIN_DIR, "config.json")

@register("anti_memes", "YourName", "轮询并精准撤回多群聊多用户的图片", "5.0.0")
class ImageRecaller(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # 配置结构: {"targets": {"群号1": [QQ号1, QQ号2], "群号2": [QQ号3]}}
        self.config = {"targets": {}} 
        self.active_bot = None  
        self.polling_task = None
        self.processed_msg_ids = set() 
        
        # 初始化时加载本地配置
        self._load_config()

    def _load_config(self):
        """加载本地 JSON 配置文件（兼容 WebUI 修改）"""
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
            except Exception as e:
                logger.error(f"加载配置文件失败: {e}")
        else:
            self._save_config()

    def _save_config(self):
        """保存配置到本地 JSON"""
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error(f"保存配置文件失败: {e}")

    async def initialize(self):
        self.polling_task = asyncio.create_task(self.poll_messages())
        logger.info("AntiMemes 插件已初始化，多群轮询任务已就绪。")

    async def terminate(self):
        if self.polling_task:
            self.polling_task.cancel()

    @filter.command("add_recall")
    async def add_recall(self, event: AstrMessageEvent, group_id: str, user_id: str):
        """添加要监控撤回的目标。用法: /add_recall <群号> <QQ号>"""
        self.active_bot = event.bot
        
        targets = self.config.setdefault("targets", {})
        # JSON 的 key 必须是字符串
        group_users = targets.setdefault(str(group_id), [])
        
        user_id_int = int(user_id)
        if user_id_int not in group_users:
            group_users.append(user_id_int)
            self._save_config()
            yield event.plain_result(f"✅ 添加成功！\n群聊 {group_id} 已新增监控用户: {user_id}")
        else:
            yield event.plain_result("⚠️ 该用户已经在当前群聊的监控列表中。")

    @filter.command("del_recall")
    async def del_recall(self, event: AstrMessageEvent, group_id: str, user_id: str):
        """移除监控目标。用法: /del_recall <群号> <QQ号>"""
        targets = self.config.get("targets", {})
        group_users = targets.get(str(group_id), [])
        
        user_id_int = int(user_id)
        if user_id_int in group_users:
            group_users.remove(user_id_int)
            # 如果该群没人了，直接清理掉这个群的 key
            if not group_users:
                del targets[str(group_id)]
            self._save_config()
            yield event.plain_result(f"🗑️ 移除成功！\n已取消监控群聊 {group_id} 中的用户: {user_id}")
        else:
            yield event.plain_result("⚠️ 未在监控列表中找到该用户。")

    @filter.command("list_recall")
    async def list_recall(self, event: AstrMessageEvent):
        """查看当前的监控列表。用法: /list_recall"""
        targets = self.config.get("targets", {})
        if not targets:
            yield event.plain_result("📭 当前监控列表为空。")
            return
            
        msg = "🔍 当前监控列表:\n"
        for gid, uids in targets.items():
            msg += f"- 群 {gid}: {', '.join(map(str, uids))}\n"
        yield event.plain_result(msg.strip())

    async def poll_messages(self):
        """后台轮询任务：多群遍历兜底扫描"""
        while True:
            await asyncio.sleep(10) 
            
            targets = self.config.get("targets", {})
            if not targets or not self.active_bot:
                continue
                
            for group_id_str, user_ids in targets.items():
                # 跳过空列表
                if not user_ids:
                    continue
                    
                group_id = int(group_id_str)
                
                try:
                    history_result = await self.active_bot.api.call_action(
                        "get_group_msg_history", 
                        group_id=group_id
                    )
                    
                    if not history_result or 'messages' not in history_result:
                        continue
                        
                    messages = history_result['messages']
                    
                    for msg in messages:
                        msg_id = msg.get("message_id")
                        sender_id = msg.get("sender", {}).get("user_id")
                        
                        # 判断是否为目标用户或已处理消息
                        if msg_id in self.processed_msg_ids or sender_id not in user_ids:
                            continue
                            
                        raw_message = msg.get("message", [])
                        has_image = False
                        
                        if isinstance(raw_message, list):
                            for node in raw_message:
                                if isinstance(node, dict) and node.get("type") == "image":
                                    has_image = True
                                    break
                        elif isinstance(raw_message, str):
                            if "[CQ:image" in raw_message:
                                has_image = True
                                
                        if has_image:
                            await self.active_bot.api.call_action("delete_msg", message_id=int(msg_id))
                            logger.info(f"[轮询兜底] 成功撤回群 {group_id} 用户 {sender_id} 的图片，消息ID: {msg_id}")
                        
                        self.processed_msg_ids.add(msg_id)
                        
                    if len(self.processed_msg_ids) > 2000:
                        self.processed_msg_ids = set(list(self.processed_msg_ids)[-1000:])

                except asyncio.CancelledError:
                    return
                except Exception as e:
                    logger.error(f"群 {group_id} 轮询任务异常: {e}")
                
                # 防风控机制：处理完一个群的历史记录后，微停 1 秒再请求下一个群，避免 API 限流
                await asyncio.sleep(1)

    @filter.event_message_type(filter.EventMessageType.GROUP_MESSAGE)
    async def on_group_message(self, event: AstrMessageEvent):
        """实时拦截机制：支持多群多目标"""
        targets = self.config.get("targets", {})
        if not targets:
            return

        message_obj = event.message_obj
        group_id_str = str(message_obj.group_id)
        
        # 1. 检查当前群是否在监控列表中
        if group_id_str not in targets:
            return
            
        # 2. 检查发信人是否在当前群的监控名单中
        sender_id = int(message_obj.sender.user_id)
        if sender_id not in targets[group_id_str]:
            return

        # 捕获最新激活的 bot 实例供轮询使用
        self.active_bot = event.bot

        msg_id = int(message_obj.message_id)
        if msg_id in self.processed_msg_ids:
            return

        raw_msg = message_obj.raw_message
        has_image = False
        
        if isinstance(raw_msg, str) and "[CQ:image" in raw_msg:
            has_image = True
        elif isinstance(raw_msg, list):
            has_image = any(isinstance(node, dict) and node.get("type") == "image" for node in raw_msg)

        if has_image:
            try:
                await event.bot.api.call_action("delete_msg", message_id=msg_id)
                logger.info(f"[实时拦截] 成功撤回群 {group_id_str} 用户 {sender_id} 的图片，消息ID: {msg_id}")
                self.processed_msg_ids.add(msg_id)
            except Exception as e:
                logger.error(f"实时撤回异常，将交由轮询兜底处理: {e}")
