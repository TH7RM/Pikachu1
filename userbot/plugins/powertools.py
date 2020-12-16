import sys
from os import execl
from time import sleep

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import BOTLOG, BOTLOG_CHATID, CMD_HELP, HEROKU_APP, bot


@bot.on(admin_cmd(pattern="اعادة التشغيل$"))
@bot.on(sudo_cmd(pattern="اعادة التشغيل$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#إعادة_بدء \n إعادة تشغيل البوت"
        )
    await edit_or_reply(
        event,
        "**جاري اعادة تشغيل البوت انتضر 10 ثواني وبعدها اكتب ** `.ايدي` او `.بنك`",
    )
    await bot.disconnect()
    execl(sys.executable, sys.executable, *sys.argv)


@bot.on(admin_cmd(pattern="ايقاف التشغيل$"))
@bot.on(sudo_cmd(pattern="ايقاف التغشيل$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if HEROKU_APP is not None:
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID, "#SHUTDOWN \n" "Bot shut down"
            )
        await edit_or_reply(event, "**جارٍ الإيقاف ... شغِّلني يدويًا لاحقًا**")
        HEROKU_APP.process_formation()["userbot"].scale(0)
    else:
        await edit_or_reply(
            event,
            "**اضبط HEROKU_APP_NAME و HEROKU_API_KEY لتعمل هذه الوظيفة بشكل صحيح**",
        )
        await bot.disconnect()


@bot.on(admin_cmd(pattern="سليب( [0-9]+)?$"))
@bot.on(sudo_cmd(pattern="سليب( [0-9]+)?$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if " " not in event.pattern_match.group(1):
        return await edit_or_reply(event, "Syntax: `.sleep time`")
    counter = int(event.pattern_match.group(1))
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "**تضع الروبوت في وضع السكون لمدة** " + str(counter) + " **ثانية**",
        )
    event = await edit_or_reply(event, f"**حسنًا ، دعني أنام لمدة {counter} ثوانٍ**")
    sleep(counter)
    await event.edit("**حسنًا ، أنا مستيقظ الآن.😍**")


CMD_HELP.update(
    {
        "powertools": "**Plugin : **`powertools`\
        \n\n  •  **Syntax : **`.restart`\
        \n  •  **Function : **__Restarts the bot !!__\
        \n\n  •  **Syntax : **`.sleep <seconds>`\
        \n  •  **Function: **__Userbots get tired too. Let yours snooze for a few seconds.__\
        \n\n  •  **Syntax : **`.shutdown`\
        \n**  •  Function : **__To turn off the dyno of heroku. you cant turn on by bot you need to got to heroku and turn on or use__ @hk_heroku_bot"
    }
)
