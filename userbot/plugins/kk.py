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
                "ترحيب\nمسح ترحيب\nلسته ترحيب\nحظر\nالغاء حظر\nالمحظورين\nكتم\nالغاء كتم\nرفع القيود \nتثبيت\nالغاء تثبيت\nالغاء تثبيت الكل\nتنظيف\nنسخ\nاعاده\nاعادة التشغيل\nايقاف التشغيل\nسليب+ رقم الوقت\nتحديث\nبحث+ اسم الاغنيه \nصوره + اسم الصوره لي تبحث عنها\nايدي\nبنك\nسرعه النت\nترجمه ar\nترجمه en \n تكرار+ الرقم+ الكلمه\nسبام+الرقم + الكلمه\nسماح \nرفض \nالكل\nكشف\nالايدي\nمعلومات الكروب\nالبوتات\nالادمنيه \nمغادره\nرابط الحساب\nمعلومات الحساب\nتاك\nللكل\nتلكراف ميديا\nتلكراف نص"
            )
        else:
            await event.edit(
                "ترحيب\nمسح ترحيب\nلسته ترحيب\nحظر\nالغاء حظر\nالمحظورين\nكتم\nالغاء كتم\nرفع القيود \nتثبيت\nالغاء تثبيت\nالغاء تثبيت الكل\nتنظيف\nنسخ\nاعاده\nاعادة التشغيل\nايقاف التشغيل\nسليب+ رقم الوقت\nتحديث\nبحث+ اسم الاغنيه \nصوره + اسم الصوره لي تبحث عنها\nايدي\nبنك\nسرعه النت\nترجمه ar\nترجمه en \n تكرار+ الرقم+ الكلمه\nسبام+الرقم + الكلمه\nسماح \nرفض \nالكل\nكشف\nالايدي\nمعلومات الكروب\nالبوتات\nالادمنيه \nمغادره\nرابط الحساب\nمعلومات الحساب\nتاك\nللكل\nتلكراف ميديا\nتلكراف نص"
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
                " **ههلااو كلبي💞اضغط ع الامر للنسخ** \n\n`.قمر` \n\n`.اقمار`\n\n`.قمور`\n\n`.نظام شمسي`\n\n`.غبي`\n\n`.تنويم`\n\n`.حلويات`\n\n`.ساعه`\n\n`.رياضه`\n\n`.الارض`\n\n`.نجمه`\n\n`.مربعات`\n\n`.مطر`\n\n`.احبك`\n\n`.شرطه`\n\n`.دائره`\n\n`.انمي`\n\n`.قرد`\n\n`.ايد`\n\n`.قتل`\n\n`.قنابل`\n\n`.قلب`\n\n`.قلبي`\n\n`.قلوب`\n\n`.حزين`\n\n`.محح`\n\n`.تفكير`\n\n`.تهكير`"
            )
        else:
            await event.edit(
                "**ههلااو كلبي💞اضغط ع الامر للنسخ** \n\n`.قمر` \n\n`.اقمار`\n\n`.قمور`\n\n`.نظام شمسي`\n\n`.غبي`\n\n`.تنويم`\n\n`.حلويات`\n\n`.ساعه`\n\n`.رياضه`\n\n`.الارض`\n\n`.نجمه`\n\n`.مربعات`\n\n`.مطر`\n\n`.احبك`\n\n`.شرطه`\n\n`.دائره`\n\n`.انمي`\n\n`.قرد`\n\n`.ايد`\n\n`.قتل`\n\n`.قنابل`\n\n`.قلب`\n\n`.قلبي`\n\n`.قلوب`\n\n`.حزين`\n\n`.محح`\n\n`.تفكير`\n\n`.تهكير`"
            )


@bot.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str == "بيكا":
        r = random.randint(0, 3)
        logger.debug(r)
        if r == 0:
            await event.edit("بيكا بيكااا ")
        else:
            await event.edit("بيكا بيكااا ")
