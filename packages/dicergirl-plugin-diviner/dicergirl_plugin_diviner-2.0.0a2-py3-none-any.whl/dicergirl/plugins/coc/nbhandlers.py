from .investigator import Investigator
from .coccards import coc_cards, coc_cache_cards, coc_rolls
from .cocutils import sc, ti, li
from dicergirl.utils.utils import format_msg, get_status, format_str
from dicergirl.handlers.on import on_startswith
from dicergirl.utils.parser import CommandParser, Commands, Only, Optional, Positional

from nonebot.matcher import Matcher
from nonebot.adapters import Bot as Bot
from nonebot.adapters.onebot.v11 import Bot as V11Bot
from nonebot.internal.matcher.matcher import Matcher
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent

coccommand = on_startswith(".coc", priority=3, block=True).handle()
ticommand = on_startswith(".ti", priority=3, block=True).handle()
licommand = on_startswith(".li", priority=3, block=True).handle()
sccommand = on_startswith(".sc", priority=3, block=True).handle()

async def coc_handler(matcher: Matcher, event: GroupMessageEvent):
    """ COC 车卡指令 """
    if not get_status(event) and not event.to_me:
        return

    args = format_msg(event.get_message(), begin=".coc", zh_en=True)
    qid = event.get_user_id()
    commands = CommandParser(
        Commands([
            Positional("roll", int, 1),
            Only("cache", False),
            Optional("set", int),
            Optional("age", int, 20),
            Optional("name", str),
            Optional("sex", str, "女"),
            ]),
        args=args,
        auto=True
        ).results
    toroll = commands["roll"]
    if toroll > 9:
        await matcher.send("超出预计的天命次数, 请检查你的天命表达式.\n使用`.help coc`获得帮助信息.")
        return

    if commands["set"] or commands["set"] == 0:
        coc_cards.update(event, coc_rolls[qid][commands["set"]], save=True)
        inv = Investigator().load(coc_rolls[qid][commands["set"]])
        await matcher.send(f"使用序列 {commands['set']} 卡:\n{inv.output()}")
        coc_rolls[qid] = {}
        return

    if commands["cache"]:
        if qid not in coc_rolls.keys():
            await matcher.send("未查询到缓存的人物卡.")
            return

        reply = "已缓存的天命人物卡:\n"
        for i, item in coc_rolls[qid].items():
            inv = Investigator().load(item)
            count = inv.rollcount()
            reply += f"天命编号: {i}\n"
            reply += inv.output() + "\n"
            reply += f"共计: {count[0]}/{count[1]}\n"
            i += 1

        await matcher.send(reply)
        return

    age = commands["age"]
    name = commands["name"]

    if not (15 <= age and age < 90):
        await matcher.send(Investigator().age_change(age))
        return

    reply = ""
    if qid in coc_rolls.keys():
        rolled = len(coc_rolls[qid].keys())
    else:
        coc_rolls[qid] = {}
        rolled = 0

    for i in range(toroll):
        inv = Investigator()
        inv.age_change(age)
        inv.sex = commands["sex"]

        if name:
            inv.name = name

        coc_rolls[qid][rolled+i] = inv.__dict__
        count = inv.rollcount()
        reply += f"天命编号: {rolled+i}\n"
        reply += inv.output() + "\n"
        reply += f"共计: {count[0]}/{count[1]}\n"

    if toroll == 1:
        coc_cache_cards.update(event, inv.__dict__, save=False)

    reply.rstrip("\n")
    await matcher.send(reply)

async def ticommandhandler(matcher: Matcher, event: MessageEvent):
    """ COC 临时疯狂检定指令 """
    if not get_status(event) and not event.to_me:
        return

    try:
        await matcher.send(ti())
    except:
        await matcher.send("未知错误, 执行`.debug on`获得更多信息.")

async def licommandhandler(matcher: Matcher, event: MessageEvent):
    """ COC 总结疯狂检定指令 """
    if not get_status(event) and not event.to_me:
        return

    try:
        await matcher.send(li())
    except:
        await matcher.send("未知错误, 执行`.debug on`获得更多信息.")

async def sccommandhandler(matcher: Matcher, event: GroupMessageEvent):
    """ COC 疯狂检定指令 """
    if not get_status(event) and not event.to_me:
        return

    args = format_str(event.get_message(), begin=".sc")
    scrs = sc(args, event)

    if isinstance(scrs, list):
        for scr in scrs:
            await matcher.send(scr)
    else:
        await matcher.send(scrs)

commands = {
    "coccommand": "coc_handler",
    "ticommand": "ticommandhandler",
    "licommand": "licommandhandler",
    "sccommand": "sccommandhandler"
    }