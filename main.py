from astrbot.api.event import filter, AstrMessageEvent, MessageChain
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import At, Node, Plain


@register("someone_say", "HakimYu", "让某人说话", "1.0.1")
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
