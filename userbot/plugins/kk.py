"""command: .kk By @Grandpaa_please """


import random

from telethon import events


@bot.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str == "الاوامر":
        r = random.randint(0, 0)
        logger.debug(r)
        if r == 0:
            await event.edit("قلب\nقلبي\nقلوب\nقمر\nاقمار\nقمور\nنجمه\nنظام شمسي\nغبي\nطياره\nرياضه\nتنويم\nحلويات\nساعه\nمربعات\nاحبك\nانمي\nدائره\nقرد\nقنابل\nقتل\nحزين\nتفكير\nتهكير")
        else:
            await event.edit("قلب\nقلبي\nقلوب\nقمر\nاقمار\nقمور\nنجمه\nنظام شمسي\nغبي\nطياره\nرياضه\nتنويم\nحلويات\nساعه\nمربعات\nاحبك\nانمي\nدائره\nقرد\nقنابل\nقتل\nحزين\nتفكير\nتهكير"")
