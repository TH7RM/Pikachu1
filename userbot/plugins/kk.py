"""command: .kk By @Grandpaa_please """


import random

from telethon import events


@bot.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str == "الاوامر":
        r = random.randint(0, 3)
        logger.debug(r)
        if r == 0:
            await event.edit(
                "قمر\nاقمار\nقمور\nنظام شمسي\nغبي\nتنويم\nحلويات\nساعه\nرياضه\nالارض\nنجمه\nمربعات\nمطر\nاحبك\nشرطه\nدائره\nانمي\nقرد\nايد\nقتل\nقنابل\nقلب\nقلبي\nقلوب\nحزين\nمحح\nتفكير\nتهكير\nترحيب\nمسح ترحيب\nلسته ترحيب\nحظر\nالغاء حظر\nالمحظورين\nكتم\nالغاء كتم\nرفع القيود"
            )
        else:
            await event.edit(
                "قمر\nاقمار\nقمور\nنظام شمسي\nغبي\nتنويم\nحلويات\nساعه\nرياضه\nالارض\nنجمه\nمربعات\nمطر\nاحبك\nشرطه\nدائره\nانمي\nقرد\nايد\nقتل\nقنابل\nقلب\nقلبي\nقلوب\nحزين\nمحح\nتفكير\nتهكير\nترحيب\nمسح ترحيب\nلسته ترحيب\nحظر\nالغاء حظر\nالمحظورين\nكتم\nالغاء كتم\nرفع القيود"
            )

            
@bot.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str == "اوامر التحشيش":
        r = random.randint(0, 3)
        logger.debug(r)
        if r == 0:
            await event.edit(
                "قمر\nاقمار\nقمور\nنظام شمسي\nغبي\nتنويم\nحلويات\nساعه\nرياضه\nالارض\nنجمه\nمربعات\nمطر\nاحبك\nشرطه\nدائره\nانمي\nقرد\nايد\nقتل\nقنابل\nقلب\nقلبي\nقلوب\nحزين\nمحح\nتفكير\nتهكير\nترحيب\nمسح ترحيب\nلسته ترحيب\nحظر\nالغاء حظر\nالمحظورين\nكتم\nالغاء كتم\nرفع القيود"
            )
        else:
            await event.edit(
                "قمر\nاقمار\nقمور\nنظام شمسي\nغبي\nتنويم\nحلويات\nساعه\nرياضه\nالارض\nنجمه\nمربعات\nمطر\nاحبك\nشرطه\nدائره\nانمي\nقرد\nايد\nقتل\nقنابل\nقلب\nقلبي\nقلوب\nحزين\nمحح\nتفكير\nتهكير\nترحيب\nمسح ترحيب\nلسته ترحيب\nحظر\nالغاء حظر\nالمحظورين\nكتم\nالغاء كتم\nرفع القيود"
            )
