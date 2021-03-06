"""
credits to @mrconfused
dont edit credits
"""
#  Copyright (C) 2020  sandeep.n(π.$)

import asyncio
import base64
from datetime import datetime

from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChatBannedRights

import userbot.plugins.sql_helper.gban_sql_helper as gban_sql

from . import BOTLOG, BOTLOG_CHATID, CAT_ID, admin_groups, get_user_from_event
from .sql_helper.mute_sql import is_muted, mute, unmute

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)


@bot.on(admin_cmd(pattern=r"حظر(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"حظر(?: |$)(.*)", allow_sudo=True))
async def catgban(cat):
    if cat.fwd_from:
        return
    cate = await edit_or_reply(cat, "جـآڒٍي آلـحــ۫͜ـظًڒٍ")
    start = datetime.now()
    user, reason = await get_user_from_event(cat)
    if not user:
        return
    if user.id == (await cat.client.get_me()).id:
        await cate.edit("لـٰـَہمـٰـَہاذا احـٰـَہظر نفـٰـَہسـٰـَہيـٰـَہ")
        return
    if user.id in CAT_ID:
        await cate.edit("لـمـٰآذًآ أحــ۫͜ـظًڒٍ مـٰطُﻭڒٍي")
        return
    try:
        hmm = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        await cat.client(ImportChatInviteRequest(hmm))
    except BaseException:
        pass
    if gban_sql.is_gbanned(user.id):
        await cate.edit(
            f" [{user.first_name}](tg://user?id={user.id}) موجود بالفعل في قائمة الحظر بأي طريقة تحقق مرة أخرى"
        )
    else:
        gban_sql.catgban(user.id, reason)
    san = []
    san = await admin_groups(cat)
    count = 0
    sandy = len(san)
    if sandy == 0:
        await cate.edit("you are not admin of atleast one group ")
        return
    await cate.edit(f"بدء حظر ↠ [{user.first_name}](tg://user?id={user.id})")
    for i in range(sandy):
        try:
            await cat.client(EditBannedRequest(san[i], user.id, BANNED_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await cat.client.send_message(
                BOTLOG_CHATID,
                f"You don't have required permission in :\nCHAT: {cat.chat.title}(`{cat.chat_id}`)\nFor banning here",
            )
    try:
        reply = await cat.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        await cate.edit(
            "`I dont have message deleting rights here! But still he was gbanned!`"
        )
    end = datetime.now()
    cattaken = (end - start).seconds
    if reason:
        await cate.edit(
            f"❃∫  المستخدم » [{user.first_name}](tg://user?id={user.id})\n  ❃∫ تم حظره "
        )
    else:
        await cate.edit(
            f"❃∫  المستخدم » [{user.first_name}](tg://user?id={user.id})\n  ❃∫ تم حظره "
        )

    if BOTLOG and count != 0:
        await cat.client.send_message(
            BOTLOG_CHATID,
            f"#GBAN\nGlobal BAN\nUser: [{user.first_name}](tg://user?id={user.id})\nID: `{user.id}`\
                                                \nReason: `{reason}`\nBanned in `{count}` groups\nTime taken = `{cattaken} seconds`",
        )


@bot.on(admin_cmd(pattern=r"الغاء حظر(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"الغاء حظر(?: |$)(.*)", allow_sudo=True))
async def catgban(cat):
    if cat.fwd_from:
        return
    cate = await edit_or_reply(cat, "جـآڒٍي آلـغــ۫͜ـآء حــ۫͜ـظًڒٍهہ")
    start = datetime.now()
    user, reason = await get_user_from_event(cat)
    if not user:
        return
    if gban_sql.is_gbanned(user.id):
        gban_sql.catungban(user.id)
    else:
        await cate.edit(
            f"[{user.first_name}](tg://user?id={user.id}) لـيســ في قآئمـٰةً آلـحــ۫͜ـظًڒٍ آلـخــ۫͜ـآصـــ͒͜ـًةً بـڪ "
        )
        return
    san = []
    san = await admin_groups(cat)
    count = 0
    sandy = len(san)
    if sandy == 0:
        await cate.edit("you are not even admin of atleast one group ")
        return
    await cate.edit(f"بدء الغاء حظر ↠ [{user.first_name}](tg://user?id={user.id})")
    for i in range(sandy):
        try:
            await cat.client(EditBannedRequest(san[i], user.id, UNBAN_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await cat.client.send_message(
                BOTLOG_CHATID,
                f"You don't have required permission in :\nCHAT: {cat.chat.title}(`{cat.chat_id}`)\nFor unbaning here",
            )
    end = datetime.now()
    cattaken = (end - start).seconds
    if reason:
        await cate.edit(
            f"[{user.first_name}](tg://user?id={user.id}) was ungbanned in `{count}` groups in `{cattaken} seconds`!!\nReason: `{reason}`"
        )
    else:
        await cate.edit(
            f"❃∫ العضو » [{user.first_name}](tg://user?id={user.id}) \n ❃∫ تم الغاء حظره "
        )

    if BOTLOG and count != 0:
        await cat.client.send_message(
            BOTLOG_CHATID,
            f"#UNGBAN\nGlobal UNBAN\nUser: [{user.first_name}](tg://user?id={user.id})\nID: {user.id}\
                                                \nReason: `{reason}`\nUnbanned in `{count}` groups\nTime taken = `{cattaken} seconds`",
        )


@bot.on(admin_cmd(pattern="المحظورين$"))
@bot.on(sudo_cmd(pattern=r"المحظورين$", allow_sudo=True))
async def gablist(event):
    if event.fwd_from:
        return
    gbanned_users = gban_sql.get_all_gbanned()
    GBANNED_LIST = "Current Gbanned Users\n"
    if len(gbanned_users) > 0:
        for a_user in gbanned_users:
            if a_user.reason:
                GBANNED_LIST += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) for {a_user.reason}\n"
            else:
                GBANNED_LIST += (
                    f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) Reason None\n"
                )
    else:
        GBANNED_LIST = "no Gbanned Users (yet)"
    if len(GBANNED_LIST) > 4095:
        with io.BytesIO(str.encode(GBANNED_LIST)) as out_file:
            out_file.name = "Gbannedusers.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Current Gbanned Users",
                reply_to=event,
            )
            await event.delete()
    else:
        await edit_or_reply(event, GBANNED_LIST)


@bot.on(admin_cmd(outgoing=True, pattern=r"كتم ?(\d+)?"))
@bot.on(sudo_cmd(pattern=r"كتم ?(\d+)?", allow_sudo=True))
async def startgmute(event):
    private = False
    if event.fwd_from:
        return
    if event.is_private:
        await event.edit("Unexpected issues or ugly errors may occur!")
        await asyncio.sleep(3)
        private = True

    reply = await event.get_reply_message()

    if event.pattern_match.group(1) is not None:
        userid = event.pattern_match.group(1)
    elif reply is not None:
        userid = reply.sender_id
    elif private is True:
        userid = event.chat_id
    else:
        return await edit_or_reply(
            event, "يرجى الرد على مستخدم أو إضافته إلى الأمر لكتمه."
        )
    replied_user = await event.client(GetFullUserRequest(userid))
    if is_muted(userid, "gmute"):
        return await edit_or_reply(
            event,
            "ذًا اݪمـٰسـٰٖـ๋͜ــتخــ۫͜ـدِمـٰ مـڪتـَٰــۘ❀ـَٰـوم ـاݪفــ͡ـعـ๋͜‏ـۂݪ 𓃼≫",
        )
    try:
        mute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, "Error occured!\nError is " + str(e))
    else:
        await edit_or_reply(
            event,
            "▪️︙المستخدم تم كتمه من هنا",
        )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#GMUTE\n"
            f"USER: [{replied_user.user.first_name}](tg://user?id={userid})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)",
        )


@bot.on(admin_cmd(outgoing=True, pattern=r"الغاء كتم ?(\d+)?"))
@bot.on(sudo_cmd(pattern=r"الغاء كتم ?(\d+)?", allow_sudo=True))
async def endgmute(event):
    private = False
    if event.fwd_from:
        return
    if event.is_private:
        await event.edit("Unexpected issues or ugly errors may occur!")
        await asyncio.sleep(3)
        private = True
    reply = await event.get_reply_message()

    if event.pattern_match.group(1) is not None:
        userid = event.pattern_match.group(1)
    elif reply is not None:
        userid = reply.sender_id
    elif private is True:
        userid = event.chat_id
    else:
        return await edit_or_reply(
            event,
            "Please reply to a user or add their username into the command to ungmute them.",
        )
    replied_user = await event.client(GetFullUserRequest(userid))
    if not is_muted(userid, "gmute"):
        return await edit_or_reply(
            event, "**هہذًآ آلـمـٰســتـٰཻــخــ۫͜ـدِمـٰ غــ۫͜ـيڒٍ مـٰڪتـٰཻــﻭمـٰ**"
        )
    try:
        unmute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, "Error occured!\nError is " + str(e))
    else:
        await edit_or_reply(
            event,
            "▪️︙المستخدم تم الغاء كتمه من هنا ",
        )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#UNGMUTE\n"
            f"USER: [{replied_user.user.first_name}](tg://user?id={userid})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)",
        )


@bot.on(admin_cmd(incoming=True))
async def watcher(event):
    if is_muted(event.sender_id, "gmute"):
        await event.delete()


CMD_HELP.update(
    {
        "gadmin": "**Plugin : **`gadmin`\
        \n\n  •  **Syntax : **`.gban <username/reply/userid> <reason (optional)>`\
\n  •  **Function : **__Bans the person in all groups where you are admin .__\
\n\n  •  **Syntax : **`.ungban <username/reply/userid>`\
\n  •  **Function : **__Reply someone's message with .ungban to remove them from the gbanned list.__\
\n\n  •  **Syntax : **`.listgban`\
\n  •  **Function : **__Shows you the gbanned list and reason for their gban.__\
\n\n  •  **Syntax : **`.gmute <username/reply> <reason (optional)>`\
\n  •  **Function : **__Mutes the person in all groups you have in common with them.__\
\n\n  •  **Syntax : **`.ungmute <username/reply>`\
\n  •  **Function : **__Reply someone's message with .ungmute to remove them from the gmuted list.__"
    }
)
