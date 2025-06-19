from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import At


@register("someone_say", "HakimYu", "让某人说话", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("someone_say")
    async def someone_say(self, event: AstrMessageEvent, at: At, content: str):
        """让某人说话，以合并转发消息的形式发送出来"""
        logger.info(at)
        logger.info(content)
        return
