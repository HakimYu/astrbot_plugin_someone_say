from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import At, Node, Plain, Nodes
from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
import random


@register("someone_say", "HakimYu", "让某人说话", "1.0.3")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

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

        await event.send(event.chain_result([Node(
            uin=at,
            name=atName,
            content=[
                Plain(content),
            ]
        )]))
        event.stop_event()

    @filter.command("everyone_say")
    async def everyone_say(self, event: AstrMessageEvent, content: str, num: int = 10):
        """让大家说话，以合并转发消息的形式发送出来"""
        msgs = []
        assert isinstance(event, AiocqhttpMessageEvent)
        client = event.bot  # 得到 client
        g = await client.get_group_member_list(group_id=event.get_group_id())
        random.shuffle(g)

        count = 0
        node_list = []

        for person in g:
            if count >= 50 or count >= num:
                break
            node_list.append(Node(uin=person["user_id"],
                                  name=person["nickname"],
                                  content=[Plain(content)]))
            count += 1
        await event.send(event.chain_result([Nodes(node_list)]))
        event.stop_event()
