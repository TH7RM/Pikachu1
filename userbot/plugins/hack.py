"""command: .hack & .thack """
# thx to @r4v4n4
import asyncio

from telethon.tl.functions.users import GetFullUserRequest

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import ALIVE_NAME, CMD_HELP

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"


@bot.on(admin_cmd(pattern=r"تهكير$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"تهكير$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await event.client(GetFullUserRequest(reply_message.sender_id))
        idd = reply_message.sender_id
        if idd == 1488639682:
            await edit_or_reply(
                event, "** هذا هو مطوري** \n ** لايمكنني اختراق حساب مطوري**"
            )
        else:
            event = await edit_or_reply(event, "جاري التهكير..")
            animation_chars = [
                "**الاتصال بخادم خاص تم الاستيلاء عليه ...**",
                "**الهدف المحدد.**",
                "**تهكير... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ **",
                "**تهكير... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ **",
                "**تهكير... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ **",
                "**تهكير... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ **",
                "**تهكير... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ **",
                "**تهكير... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ **",
                "**تهكير... 84%\n█████████████████████▒▒▒▒ **",
                "**تهكير... 100%\n█████████مهكر███████████ **",
                f"**تم اختراق الحساب المستهدف ......\n\nأدفع 69$ الى** {DEFAULTUSER} . **لإزالة هذا الاختراق ..**",
            ]
            animation_interval = 3
            animation_ttl = range(11)
            for i in animation_ttl:
                await asyncio.sleep(animation_interval)
                await event.edit(animation_chars[i % 11])
    else:
        await edit_or_reply(event, "لم يتم تحديد الهدف \n لا يمكن اختراق الحساب")


CMD_HELP.update(
    {
        "hack": "**Plugin : **`hack`\
        \n\n**Syntax : **`.hack reply to a person`\
        \n**Function : **__shows an animation of hacking progess bar__\
        \n\n**Syntax : **`.thack reply to a person`\
        \n**Function : **__shows an animation of Telegram account hacking to a replied person__\
        \n\n**Syntax : **`.wahack reply to a person`\
        \n**Function : **__shows an animation of whatsapp account hacking to a replied person__\
    "
    }
)
