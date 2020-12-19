# حقوق الطبع والنشر محفوضة لشركة بيكاتشو بوت ®™

from asyncio import sleep

from telethon.errors import rpcbaseerrors

from ..utils import admin_cmd, edit_or_reply, errors_handler, sudo_cmd
from . import BOTLOG, BOTLOG_CHATID, CMD_HELP


@bot.on(admin_cmd(outgoing=True, pattern="تنظيف$"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="تنظيف$"))
@errors_handler
async def fastpurger(purg):
    # For .purge command, purge all messages starting from the reply.
    chat = await purg.get_input_chat()
    msgs = []
    itermsg = purg.client.iter_messages(chat, min_id=purg.reply_to_msg_id)
    count = 0

    if purg.reply_to_msg_id is not None:
        async for msg in itermsg:
            msgs.append(msg)
            count += 1
            msgs.append(purg.reply_to_msg_id)
            if len(msgs) == 100:
                await purg.client.delete_messages(chat, msgs)
                msgs = []
    else:
        await edit_or_reply(
            purg,
            "**لم يتم تحديد رسالة.**",
        )
        return

    if msgs:
        await purg.client.delete_messages(chat, msgs)
    done = await purg.client.send_message(
        purg.chat_id,
        "اكتمل التنظيف السريع!\nتم حذف " + str(count) + " رسائل.",
    )

    if BOTLOG:
        await purg.client.send_message(
            BOTLOG_CHATID,
            "#التنظيف_السريع \nتم تنظيف " + str(count) + " ** رسائل بنجاح.**",
        )
    await sleep(2)
    await done.delete()


@bot.on(admin_cmd(outgoing=True, pattern="مسح$"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="مسح$"))
@errors_handler
async def delete_it(delme):
    """ بالنسبة لأمر .مسح ، احذف الرسالة التي تم الرد عليها. """
    msg_src = await delme.get_reply_message()
    if delme.reply_to_msg_id:
        try:
            await msg_src.delete()
            await delme.delete()
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "#مسح \nتم حذف الرسالة بنجاح"
                )
        except rpcbaseerrors.BadRequestError:
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "حسنًا ، لا يمكنني حذف رسالة"
                )


CMD_HELP.update(
    {
        "purge": "**Plugin : **`purge`\
        \n\n**Syntax : **`.purge reply to message to start purge from there`\
        \n**Function : **__Purges all messages starting from the reply.__\
        \n\n**Syntax : **`.purgeme <x>`\
        \n**Function : **__Deletes x amount of your latest messages.__\
        \n\n**Syntax : **`.del reply to message to delete`\
        \n**Function : **__Deletes the message you replied to.__"
    }
)
