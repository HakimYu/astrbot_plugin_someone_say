from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import At, Node, Plain


@register("someone_say", "HakimYu", "让某人说话", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    def _create_forward_node(self, user_id: str, nickname: str, content: str) -> dict:
        """创建转发节点"""
        return {
            "type": "node",
            "data": {
                "user_id": user_id,
                "nickname": nickname,
                "content": [{"type": "text", "data": {"text": content}}]
            }
        }

    @filter.command("someone_say")
    async def someone_say(self, event: AstrMessageEvent, atStr: str, content: str):
        """让某人说话，以合并转发消息的形式发送出来"""
        # 自动提取第一个@的QQ号
        at = None
        atName = None
        index = 0
        for seg in event.get_messages():
            if isinstance(seg, At):
                if index == 0:
                    index += 1
                    continue
                else:
                    at = seg.qq
                    atName = seg.name
                    index += 1
                break
        if at is None:
            yield event.plain_result("请@一个用户")
            return
        if event.get_platform_name() == "aiocqhttp":
            from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
            assert isinstance(event, AiocqhttpMessageEvent)
            client = event.bot  # 得到 client
            # 构造合并转发节点
            node = self._create_forward_node(str(at), atName, content)
            forward_payloads = {
                "group_id": int(event.get_group_id()),
                "messages": [node]
            }
            send_ret = await client.api.call_action('send_group_forward_msg', **forward_payloads)
            logger.info(f"send_group_forward_msg: {send_ret}")
            yield
