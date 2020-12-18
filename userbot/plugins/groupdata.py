import asyncio
import io
from asyncio import sleep
from datetime import datetime
from math import sqrt

from emoji import emojize
from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    ChannelPublicGroupNaError,
    ChatAdminRequiredError,
    UserAdminInvalidError,
)
from telethon.tl import functions
from telethon.tl.functions.channels import GetFullChannelRequest, GetParticipantsRequest
from telethon.tl.functions.messages import GetFullChatRequest, GetHistoryRequest
from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
    ChannelParticipantsKicked,
    ChatBannedRights,
    MessageActionChannelMigrateFrom,
    UserStatusEmpty,
    UserStatusLastMonth,
    UserStatusLastWeek,
    UserStatusOffline,
    UserStatusOnline,
    UserStatusRecently,
)
from telethon.utils import get_input_location

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import BOTLOG, BOTLOG_CHATID, CMD_HELP


@bot.on(admin_cmd(outgoing=True, pattern="مغادره$"))
async def kickme(leave):
    await leave.edit("تم مغادرة المجموعة بأمر من المطور جاو عزيزي")
    await leave.client.kick_participant(leave.chat_id, "me")


@bot.on(admin_cmd(pattern="الادمنيه ?(.*)"))
@bot.on(sudo_cmd(pattern="الادمنيه ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mentions = "**المشرفين في هذه المجموعة:**: \n"
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
    input_str = event.pattern_match.group(1)
    to_write_chat = await event.get_input_chat()
    chat = None
    if input_str:
        mentions_heading = "الادمنيه في {} المجموعة: \n".format(input_str)
        mentions = mentions_heading
        try:
            chat = await event.client.get_entity(input_str)
        except Exception as e:
            await edit_or_reply(event, str(e))
            return None
    else:
        chat = to_write_chat
        if not event.is_group:
            await edit_or_reply(event, "هل أنت متأكد من أن هذه مجموعة?")
            return
    try:
        async for x in event.client.iter_participants(
            chat, filter=ChannelParticipantsAdmins
        ):
            if not x.deleted and isinstance(x.participant, ChannelParticipantCreator):
                mentions += "\n 𓆩المالك𓆪 [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id
                )
        mentions += "\n"
        async for x in event.client.iter_participants(
            chat, filter=ChannelParticipantsAdmins
        ):
            if x.deleted:
                mentions += "\n `{}`".format(x.id)
            else:
                if isinstance(x.participant, ChannelParticipantAdmin):
                    mentions += "\n 💞 [{}](tg://user?id={}) `{}`".format(
                        x.first_name, x.id, x.id
                    )
    except Exception as e:
        mentions += " " + str(e) + "\n"
    if reply_message:
        await reply_message.reply(mentions)
    else:
        await event.client.send_message(event.chat_id, mentions)
    await event.delete()


@bot.on(admin_cmd(pattern="البوتات ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="البوتات ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mentions = "**البوتات في هذه المجموعة**: \n"
    input_str = event.pattern_match.group(1)
    to_write_chat = await event.get_input_chat()
    chat = None
    if not input_str:
        chat = to_write_chat
    else:
        mentions = "Bots in {} Group: \n".format(input_str)
        try:
            chat = await event.client.get_entity(input_str)
        except Exception as e:
            await edit_or_reply(event, str(e))
            return None
    try:
        async for x in event.client.iter_participants(
            chat, filter=ChannelParticipantsBots
        ):
            if isinstance(x.participant, ChannelParticipantAdmin):
                mentions += "\n [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id
                )
            else:
                mentions += "\n ⫺ [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id
                )
    except Exception as e:
        mentions += " " + str(e) + "\n"
    await edit_or_reply(event, mentions)


@bot.on(admin_cmd(pattern=r"الاعضاء ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern=r"الاعضاء ?(.*)", allow_sudo=True))
async def get_users(show):
    if show.fwd_from:
        return
    mentions = "**المستخدمون في هذه المجموعة**: \n"
    reply_to_id = None
    if show.reply_to_msg_id:
        reply_to_id = show.reply_to_msg_id
    input_str = show.pattern_match.group(1)
    await show.get_input_chat()
    if not input_str:
        if not show.is_group:
            await edit_or_reply(show, "`هل أنت متأكد من أن هذه مجموعة؟`")
            return
    else:
        mentions_heading = "Users in {} Group: \n".format(input_str)
        mentions = mentions_heading
        try:
            chat = await show.client.get_entity(input_str)
        except Exception as e:
            await edit_delete(show, f"`{str(e)}`", 10)
    catevent = await edit_or_reply(show, "`الحصول على قائمة المستخدمين انتظر...`  ")
    try:
        if not show.pattern_match.group(1):
            async for user in show.client.iter_participants(show.chat_id):
                if not user.deleted:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
                else:
                    mentions += f"\nDeleted Account `{user.id}`"
        else:
            async for user in show.client.iter_participants(chat.id):
                if not user.deleted:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
                else:
                    mentions += f"\nالحسابات المحذوفه `{user.id}`"
    except Exception as e:
        mentions += " " + str(e) + "\n"
    if len(mentions) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(mentions)) as out_file:
            out_file.name = "users.text"
            await show.client.send_file(
                show.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Users list",
                reply_to=reply_to_id,
            )
            await catevent.delete()
    else:
        await catevent.edit(mentions)


@bot.on(admin_cmd(pattern="معلومات الكروب(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="معلومات الكروب(?: |$)(.*)", allow_sudo=True))
async def info(event):
    catevent = await edit_or_reply(event, "**جاري جلب معلومات الدردشة ...**")
    chat = await get_chatinfo(event, catevent)
    caption = await fetch_info(chat, event)
    try:
        await catevent.edit(caption, parse_mode="html")
    except Exception as e:
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID, f"**خطأ في المعلومات : **\n`{str(e)}`"
            )
        await catevent.edit("**لقد حدث خطأ غير متوقع.**")


@bot.on(admin_cmd(pattern="رفع القيود ?(.*)"))
@bot.on(sudo_cmd(pattern="رفع القيود ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str:
        logger.info("TODO: Not yet Implemented")
    else:
        if event.is_private:
            return False
        et = await edit_or_reply(event, "البحث في قوائم المشاركين.")
        p = 0
        async for i in bot.iter_participants(
            event.chat_id, filter=ChannelParticipantsKicked, aggressive=True
        ):
            rights = ChatBannedRights(until_date=0, view_messages=False)
            try:
                await bot(
                    functions.channels.EditBannedRequest(event.chat_id, i, rights)
                )
            except FloodWaitError as ex:
                logger.warn("sleeping for {} seconds".format(ex.seconds))
                await asyncio.sleep(ex.seconds)
            except Exception as ex:
                await et.edit(str(ex))
            else:
                p += 1
        await et.edit("{}: {} غير محظور".format(event.chat_id, p))


@bot.on(admin_cmd(pattern="الاحصائيات ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="الاحصائيات ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return False
    input_str = event.pattern_match.group(1)
    if input_str:
        chat = await event.get_chat()
        if not chat.admin_rights and not chat.creator:
            await edit_or_reply(event, "**أنت لست مسؤولاً هنا!**")
            return False
    p = 0
    b = 0
    c = 0
    d = 0
    e = []
    m = 0
    n = 0
    y = 0
    w = 0
    o = 0
    q = 0
    r = 0
    et = await edit_or_reply(event, "البحث في قوائم المشاركين.")
    async for i in bot.iter_participants(event.chat_id):
        p += 1
        #
        # Note that it's "reversed". You must set to ``True`` the permissions
        # you want to REMOVE, and leave as ``None`` those you want to KEEP.
        rights = ChatBannedRights(until_date=None, view_messages=True)
        if isinstance(i.status, UserStatusEmpty):
            y += 1
            if "y" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("أحتاج امتيازات المشرف لأداء هذا الإجراء!")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusLastMonth):
            m += 1
            if "m" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("أحتاج امتيازات المشرف لأداء هذا الإجراء!")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusLastWeek):
            w += 1
            if "w" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("أحتاج امتيازات المشرف لأداء هذا الإجراء!")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusOffline):
            o += 1
            if "o" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("أحتاج امتيازات المشرف لأداء هذا الإجراء!")
                    e.append(str(e))
                    break
                else:
                    c += 1
        if isinstance(i.status, UserStatusOnline):
            q += 1
            if "q" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("أحتاج امتيازات المشرف لأداء هذا الإجراء!")
                    e.append(str(e))
                    break
                else:
                    c += 1
        if isinstance(i.status, UserStatusRecently):
            r += 1
            if "r" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("أحتاج امتيازات المشرف لأداء هذا الإجراء!")
                    e.append(str(e))
                    break
        if i.bot:
            b += 1
            if "b" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("أحتاج امتيازات المشرف لأداء هذا الإجراء!")
                    e.append(str(e))
                    break
                else:
                    c += 1
        elif i.deleted:
            d += 1
            if "d" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("أحتاج امتيازات المشرف لأداء هذا الإجراء!")
                    e.append(str(e))
        elif i.status is None:
            n += 1
    if input_str:
        required_string = """المطرودين {} / {} المستخدمين
الحسابات المحذوفة: {}
اخر ظهور منذ زمن طويل: {}
اخر ظهور منذ شهر: {}
اخر ظهور منذ اسبوع: {}
غير  متصل: {}
متصل: {}
اخر ظهور قبل قليل: {}
البوتات: {}
لا شيء: {}"""
        await et.edit(required_string.format(c, p, d, y, m, w, o, q, r, b, n))
        await asyncio.sleep(5)
    await et.edit(
        """العدد: {} مستخدماَ
الحسابات المحذوفة: {}
اخر ظهور منذ زمن طويل: {}
اخر ظهور منذ شهر: {}
اخر ظهور منذ اسبوع: {}
غير  متصل: {}
متصل: {}
اخر ظهور قبل قليل: {}
البوتات: {}
لا شيء: {}""".format(
            p, d, y, m, w, o, q, r, b, n
        )
    )


# Ported by ©[NIKITA](t.me/kirito6969) and ©[EYEPATCH](t.me/NeoMatrix90)
@bot.on(admin_cmd(pattern=f"المحذوفين ?(.*)"))
@bot.on(sudo_cmd(pattern="المحذوفين ?(.*)", allow_sudo=True))
async def rm_deletedacc(show):
    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = (
        "**لم يتم العثور على زومبي أو حسابات محذوفة في هذه المجموعة ، المجموعة نظيفة**"
    )
    if con != "clean":
        event = await edit_or_reply(
            show, "**البحث عن حسابات شبح / محذوفة / زومبي ...**"
        )
        async for user in show.client.iter_participants(show.chat_id):
            if user.deleted:
                del_u += 1
                await sleep(0.5)
        if del_u > 0:
            del_status = f"**تم العثور  {del_u} حساب (حسابات) شبح / محذوف / زومبي في هذه المجموعة ،\
                           \nقم بتنظيفها باستخدام**  `.zombies clean`"
        await event.edit(del_status)
        return
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_delete(show, "أنا لست مشرفًا هنا!**", 5)
        return
    event = await edit_or_reply(
        show, "**حذف الحسابات المحذوفة...\nأوه أستطيع أن أفعل ذلك؟!؟!**"
    )
    del_u = 0
    del_a = 0
    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client.kick_participant(show.chat_id, user.id)
                await sleep(0.5)
                del_u += 1
            except ChatAdminRequiredError:
                await edit_delete(event, "**ليس لدي حقوق حظر في هذه المجموعة**", 5)
                return
            except UserAdminInvalidError:
                del_a += 1
    if del_u > 0:
        del_status = f"تم تنظيف **{del_u}** حساب (حسابات) محذوفة"
    if del_a > 0:
        del_status = f"تم تنظيف **{del_u}** حساب (حسابات) محذوفة \
        \n**{del_a}** لا تتم إزالة حسابات المشرف المحذوفة"
    await edit_delete(event, del_status, 5)
    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID,
            f"#نظف\
            \n{del_status}\
            \nالمجموعة: {show.chat.title}(`{show.chat_id}`)",
        )


async def ban_user(chat_id, i, rights):
    try:
        await bot(functions.channels.EditBannedRequest(chat_id, i, rights))
        return True, None
    except Exception as exc:
        return False, str(exc)


async def get_chatinfo(event, catevent):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChatRequest(chat))
    except BaseException:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await catevent.edit("**قناة / مجموعة غير صالحة**")
            return None
        except ChannelPrivateError:
            await catevent.edit("**هذه قناة / مجموعة خاصة أو محظور من هناك**")
            return None
        except ChannelPublicGroupNaError:
            await catevent.edit("**القناة أو المجموعة الخارقة غير موجودة**")
            return None
        except (TypeError, ValueError) as err:
            await catevent.edit(str(err))
            return None
    return chat_info


async def fetch_info(chat, event):
    # chat.chats is a list so we use get_entity() to avoid IndexError
    chat_obj_info = await event.client.get_entity(chat.full_chat.id)
    broadcast = (
        chat_obj_info.broadcast if hasattr(chat_obj_info, "broadcast") else False
    )
    chat_type = "قناة" if broadcast else "المجموعة"
    chat_title = chat_obj_info.title
    warn_emoji = emojize(":warning:")
    try:
        msg_info = await event.client(
            GetHistoryRequest(
                peer=chat_obj_info.id,
                offset_id=0,
                offset_date=datetime(2010, 1, 1),
                add_offset=-1,
                limit=1,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
    except Exception as e:
        msg_info = None
        print("Exception:", e)
    # No chance for IndexError as it checks for msg_info.messages first
    first_msg_valid = (
        True
        if msg_info and msg_info.messages and msg_info.messages[0].id == 1
        else False
    )
    # Same for msg_info.users
    creator_valid = True if first_msg_valid and msg_info.users else False
    creator_id = msg_info.users[0].id if creator_valid else None
    creator_firstname = (
        msg_info.users[0].first_name
        if creator_valid and msg_info.users[0].first_name is not None
        else "حساب محذوف"
    )
    creator_username = (
        msg_info.users[0].username
        if creator_valid and msg_info.users[0].username is not None
        else None
    )
    created = msg_info.messages[0].date if first_msg_valid else None
    former_title = (
        msg_info.messages[0].action.title
        if first_msg_valid
        and isinstance(msg_info.messages[0].action, MessageActionChannelMigrateFrom)
        and msg_info.messages[0].action.title != chat_title
        else None
    )
    try:
        dc_id, location = get_input_location(chat.full_chat.chat_photo)
    except Exception as e:
        dc_id = "غير معروف"
        str(e)

    # this is some spaghetti I need to change
    description = chat.full_chat.about
    members = (
        chat.full_chat.participants_count
        if hasattr(chat.full_chat, "participants_count")
        else chat_obj_info.participants_count
    )
    admins = (
        chat.full_chat.admins_count if hasattr(chat.full_chat, "admins_count") else None
    )
    banned_users = (
        chat.full_chat.kicked_count if hasattr(chat.full_chat, "kicked_count") else None
    )
    restrcited_users = (
        chat.full_chat.banned_count if hasattr(chat.full_chat, "banned_count") else None
    )
    members_online = (
        chat.full_chat.online_count if hasattr(chat.full_chat, "online_count") else 0
    )
    group_stickers = (
        chat.full_chat.stickerset.title
        if hasattr(chat.full_chat, "stickerset") and chat.full_chat.stickerset
        else None
    )
    messages_viewable = msg_info.count if msg_info else None
    messages_sent = (
        chat.full_chat.read_inbox_max_id
        if hasattr(chat.full_chat, "read_inbox_max_id")
        else None
    )
    messages_sent_alt = (
        chat.full_chat.read_outbox_max_id
        if hasattr(chat.full_chat, "read_outbox_max_id")
        else None
    )
    exp_count = chat.full_chat.pts if hasattr(chat.full_chat, "pts") else None
    username = chat_obj_info.username if hasattr(chat_obj_info, "username") else None
    bots_list = chat.full_chat.bot_info  # this is a list
    bots = 0
    supergroup = (
        "<b>نعم</b>"
        if hasattr(chat_obj_info, "megagroup") and chat_obj_info.megagroup
        else "لا"
    )
    slowmode = (
        "<b>نعم</b>"
        if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled
        else "لا"
    )
    slowmode_time = (
        chat.full_chat.slowmode_seconds
        if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled
        else None
    )
    restricted = (
        "<b>نعم</b>"
        if hasattr(chat_obj_info, "restricted") and chat_obj_info.restricted
        else "لا"
    )
    verified = (
        "<b>نعم</b>"
        if hasattr(chat_obj_info, "verified") and chat_obj_info.verified
        else "لا"
    )
    username = "@{}".format(username) if username else None
    creator_username = "@{}".format(creator_username) if creator_username else None
    # end of spaghetti block

    if admins is None:
        # use this alternative way if chat.full_chat.admins_count is None,
        # works even without being an admin
        try:
            participants_admins = await event.client(
                GetParticipantsRequest(
                    channel=chat.full_chat.id,
                    filter=ChannelParticipantsAdmins(),
                    offset=0,
                    limit=0,
                    hash=0,
                )
            )
            admins = participants_admins.count if participants_admins else None
        except Exception as e:
            print("Exception:", e)
    if bots_list:
        for bot in bots_list:
            bots += 1

    caption = "<b>معلومات الدردشة:</b>\n"
    caption += f"ايدي: <code>{chat_obj_info.id}</code>\n"
    if chat_title is not None:
        caption += f"اسم {chat_type}: {chat_title}\n"
    if former_title is not None:  # Meant is the very first title
        caption += f"الاسم السابق: {former_title}\n"
    if username is not None:
        caption += f"نوع {chat_type}: عامة\n"
        caption += f"الرابط: {username}\n"
    else:
        caption += f" نوع {chat_type}:خاصة\n"
    if creator_username is not None:
        caption += f"المنشئ: {creator_username}\n"
    elif creator_valid:
        caption += (
            f'المنشئ: <a href="tg://user?id={creator_id}">{creator_firstname}</a>\n'
        )
    if created is not None:
        caption += f"الانشاء: <code>{created.date().strftime('%b %d, %Y')} - {created.time()}</code>\n"
    else:
        caption += f"الانشاء: <code>{chat_obj_info.date.date().strftime('%b %d, %Y')} - {chat_obj_info.date.time()}</code> {warn_emoji}\n"
    caption += f"مركز البيانات: {dc_id}\n"
    if exp_count is not None:
        chat_level = int((1 + sqrt(1 + 7 * exp_count / 14)) / 2)
        caption += f"{chat_type} مستوى: <code>{chat_level}</code>\n"
    if messages_viewable is not None:
        caption += f"الرسائل القابلة للعرض: <code>{messages_viewable}</code>\n"
    if messages_sent:
        caption += f"الرسائل المرسلة: <code>{messages_sent}</code>\n"
    elif messages_sent_alt:
        caption += f"الرسائل المرسلة: <code>{messages_sent_alt}</code> {warn_emoji}\n"
    if members is not None:
        caption += f"الاعضاء: <code>{members}</code>\n"
    if admins is not None:
        caption += f"المشرفين: <code>{admins}</code>\n"
    if bots_list:
        caption += f"البوتات: <code>{bots}</code>\n"
    if members_online:
        caption += f"المتصلون: <code>{members_online}</code>\n"
    if restrcited_users is not None:
        caption += f"المقيدون: <code>{restrcited_users}</code>\n"
    if banned_users is not None:
        caption += f"المحظورين: <code>{banned_users}</code>\n"
    if group_stickers is not None:
        caption += f'ملصقات {chat_type}: <a href="t.me/addstickers/{chat.full_chat.stickerset.short_name}">{group_stickers}</a>\n'
    caption += "\n"
    if not broadcast:
        caption += f"الارسال البطيء: {slowmode}"
        if (
            hasattr(chat_obj_info, "slowmode_enabled")
            and chat_obj_info.slowmode_enabled
        ):
            caption += f", <code>{slowmode_time}s</code>\n\n"
        else:
            caption += "\n\n"
    if not broadcast:
        caption += f"المجموعة خارقه: {supergroup}\n\n"
    if hasattr(chat_obj_info, "restricted"):
        caption += f"محدد: {restricted}\n"
        if chat_obj_info.restricted:
            caption += f"> Platform: {chat_obj_info.restriction_reason[0].platform}\n"
            caption += f"> Reason: {chat_obj_info.restriction_reason[0].reason}\n"
            caption += f"> Text: {chat_obj_info.restriction_reason[0].text}\n\n"
        else:
            caption += "\n"
    if hasattr(chat_obj_info, "scam") and chat_obj_info.scam:
        caption += "Scam: <b>Yes</b>\n\n"
    if hasattr(chat_obj_info, "verified"):
        caption += f"تم التحقق بواسطة تلكرام: {verified}\n\n"
    if description:
        caption += f"الوصف: \n<code>{description}</code>\n"
    return caption


CMD_HELP.update(
    {
        "groupdata": "**Plugin : **`groupdata`\
    \n\n**Syntax : **`.kickme`\
    \n**Usage : **__Throws you away from that chat_\
    \n\n**Syntax : **`.admins or .admins <username of group >`\
    \n**Usage : **__Retrieves a list of admins in the chat.__\
    \n\n**Syntax : **`.bots or .bots <username of group >`\
    \n**Usage : **__Retrieves a list of bots in the chat.__\
    \n\n**Syntax : **`.users or .users <name of member>`\
    \n**Function : **__Retrieves all (or queried) users in the chat.__\
    \n\n**Syntax : **`.unbanall`\
    \n**Function: **__Unbans everyone who are blocked in that group __\
    \n\n**Syntax : **`.ikuck`\
    \n**Function: **__stats of the group like no of users no of deleted users.__\
    \n\n**Syntax : **`.chatinfo or .chatinfo <username of group>`\
    \n**Function : **__Shows you the total information of the required chat.__\
    \n\n**Syntax : **`.zombies`\
    \n**Function : **__Searches for deleted accounts in a group. Use `.zombies clean` to remove deleted accounts from the group.__"
    }
)
