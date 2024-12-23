from pathlib import Path

from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment as ms
from nonebot.params import CommandArg

from src.const.path import ASSETS, build_path
from src.utils.network import Request
from src.utils.generate import generate

import os


AnnounceMatcher = on_command("jx3_announce", aliases={"维护公告", "更新公告", "公告", "更新"}, force_whitespace=True, priority=5)

@AnnounceMatcher.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    """
    获取维护公告的图片：

    Example：-维护公告
    """
    if args.extract_plain_text() != "":
        return
    if os.path.exists(build_path(ASSETS, ["image", "jx3", "update.png"])):
        img = Request(Path(build_path(ASSETS, ["image", "jx3", "update.png"])).as_uri()).local_content
        await AnnounceMatcher.finish(ms.image(img))
    else:
        store_path = await generate(
            "https://jx3.xoyo.com/launcher/update/latest.html", 
            "div", 
            viewport={"height": 1920, "width": 1080}, 
            first=True,
            output_path=build_path(ASSETS, ["image", "jx3", "update.png"])
        )
        if not isinstance(store_path, str):
            return
        img = Request(Path(store_path).as_uri()).local_content
        await AnnounceMatcher.finish(ms.image(img))

BetaAnnounceMatcher = on_command("jx3_beta_announce", aliases={"体服公告"}, priority=5, force_whitespace=True)

@BetaAnnounceMatcher.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    """
    获取体服维护公告。
    """
    if args.extract_plain_text() != "":
        return
    image = Request(
        Path(
            await generate(
                "https://jx3.xoyo.com/launcher/update/latest_exp.html",
                "div",
                viewport={"height": 1920, "width": 1080},
                first=True
            )
        ).as_uri()
    ).local_content
    await AnnounceMatcher.finish(ms.image(image))