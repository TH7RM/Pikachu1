"""command: .kk By @Grandpaa_please """


import random

from telethon import events


@bot.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str == "المطور":
        r = random.randint(0, 1)
        logger.debug(r)
        if r == 0:
            await event.edit("pikapikaa\n\n Developer》 @llllflf")
        else:
            await event.edit("pikapikaa\n\n Developer》 ")
