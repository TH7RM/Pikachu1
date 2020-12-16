# Copyright (C) 2019 The Raphielscape Company LLC.
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
# credits to @AvinashReddy3108
"""
This module updates the userbot based on upstream revision
Ported from Kensurbot
"""
import asyncio
import sys
from os import environ, execle, path, remove

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import CMD_HELP, runcmd

HEROKU_APP_NAME = Config.HEROKU_APP_NAME or None
HEROKU_API_KEY = Config.HEROKU_API_KEY or None
UPSTREAM_REPO_BRANCH = Config.UPSTREAM_REPO_BRANCH
UPSTREAM_REPO_URL = Config.UPSTREAM_REPO_URL

requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), "requirements.txt"
)


async def gen_chlog(repo, diff):
    ch_log = ""
    d_form = "%d/%m/%y"
    for c in repo.iter_commits(diff):
        ch_log += (
            f"  • {c.summary} ({c.committed_datetime.strftime(d_form)}) <{c.author}>\n"
        )
    return ch_log


async def print_changelogs(event, ac_br, changelog):
    changelog_str = (
        f"**التحديث الجديد متاح لـ {ac_br}:\n\nالتحديثات↡↡:**\n`{changelog}`"
    )
    if len(changelog_str) > 4096:
        await event.edit("`Changelog is too big, view the file to see it.`")
        with open("output.txt", "w+") as file:
            file.write(changelog_str)
        await event.client.send_file(
            event.chat_id,
            "output.txt",
            reply_to=event.id,
        )
        remove("output.txt")
    else:
        await event.client.send_message(
            event.chat_id,
            changelog_str,
            reply_to=event.id,
        )
    return True


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


async def deploy(event, repo, ups_rem, ac_br, txt):
    if HEROKU_API_KEY is not None:
        import heroku3

        heroku = heroku3.from_key(HEROKU_API_KEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if HEROKU_APP_NAME is None:
            await event.edit(
                "`Please set up the` **HEROKU_APP_NAME** `Var`"
                " to be able to deploy your userbot...`"
            )
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APP_NAME:
                heroku_app = app
                break
        if heroku_app is None:
            await event.edit(
                f"{txt}\n" "**بيانات اعتماد هيروكي غير صالحة لنشر التنصيب**"
            )
            return repo.__del__()
        await event.edit("**جاري تنصيب التحديث انتظر من فضلك ✔**")
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + HEROKU_API_KEY + "@"
        )
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec="HEAD:refs/heads/master", force=True)
        except Exception as error:
            await event.edit(f"{txt}\n`Here is the error log:\n{error}`")
            return repo.__del__()
        build = app.builds(order_by="created_at", sort="desc")[0]
        if build.status == "failed":
            await event.edit("**فشل التحديث \n" "تم إلغاؤه أو حدثت بعض الأخطاء ...**")
            await asyncio.sleep(5)
            return await event.delete()
        await event.edit("**جاري تنصيب التحديث انتظر من فضلك ✔️**")
    else:
        await event.edit("`Please set up`  **HEROKU_API_KEY**  ` Var...`")
    return


async def update(event, repo, ups_rem, ac_br):
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await update_requirements()
    await event.edit(
        "**تم التحديث بنجاح!**\n" "**جاري اعادة تشغيل البوت انتظر ثواني ↻**"
    )
    # Spin a new instance of bot
    args = [sys.executable, "-m", "userbot"]
    execle(sys.executable, *args, environ)
    return


@bot.on(admin_cmd(outgoing=True, pattern=r"تحديث($| (now|deploy))"))
@bot.on(sudo_cmd(pattern="تحديث($| (now|deploy))", allow_sudo=True))
async def upstream(event):
    "For .update command, check if the bot is up to date, update if specified"
    conf = event.pattern_match.group(1).strip()
    event = await edit_or_reply(
        event, "**التحقق من وجود تحديثات ، يرجى الانتظار ....**"
    )
    off_repo = UPSTREAM_REPO_URL
    force_update = False
    if HEROKU_API_KEY is None or HEROKU_APP_NAME is None:
        return await edit_or_reply(
            event, "`Set the required vars first to update the bot`"
        )
    try:
        txt = "`Oops.. Updater cannot continue due to "
        txt += "some problems occured`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\n`directory {error} is not found`")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n`Early failure! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError as error:
        if conf is None:
            return await event.edit(
                f"`Unfortunately, the directory {error} "
                "does not seem to be a git repository.\n"
                "But we can fix that by force updating the userbot using "
                ".update now.`"
            )
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_update = True
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    ac_br = repo.active_branch.name
    if ac_br != UPSTREAM_REPO_BRANCH:
        await event.edit(
            "**[UPDATER]:**\n"
            f"`Looks like you are using your own custom branch ({ac_br}). "
            "in that case, Updater is unable to identify "
            "which branch is to be merged. "
            "please checkout to any official branch`"
        )
        return repo.__del__()
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    # Special case for deploy
    if conf == "deploy":
        await event.edit("**جاري تنصيب بوت بيكاتشو ، يرجى الانتظار ....**")
        await deploy(event, repo, ups_rem, ac_br, txt)
        return
    if changelog == "" and not force_update:
        await event.edit(
            "\n**بيكاتشو  محدث لاخر اصدار مع**  " f"**{UPSTREAM_REPO_BRANCH}**\n"
        )
        return repo.__del__()
    if conf == "" and not force_update:
        await print_changelogs(event, ac_br, changelog)
        await event.delete()
        return await event.respond(
            "** اضغط ** [  `.تحديث deploy ` ]  ** لتحديث البوت الى الاصدار الجديد ** "
        )

    if force_update:
        await event.edit(
            "`Force-Syncing to latest stable userbot code, please wait...`"
        )
    if conf == "now":
        await event.edit("**جارٍ تحديث بوت بيكاتشو يرجى الانتظار ....**")
        await update(event, repo, ups_rem, ac_br)
    return


@bot.on(admin_cmd(outgoing=True, pattern=r"badcat$"))
@bot.on(sudo_cmd(pattern="badcat$", allow_sudo=True))
async def upstream(event):
    event = await edit_or_reply(event, "`Pulling the bad cat repo wait a sec ....`")
    off_repo = "https://github.com/TH7RM/pika"
    catcmd = f"rm -rf .git"
    try:
        await runcmd(catcmd)
    except BaseException:
        pass
    try:
        txt = "`Oops.. Updater cannot continue due to "
        txt += "some problems occured`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\n`directory {error} is not found`")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n`Early failure! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ac_br = repo.active_branch.name
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    await event.edit("**جاري تنصيب بوت بيكاتشو ، يرجى الانتظار ....**")
    await deploy(event, repo, ups_rem, ac_br, txt)


CMD_HELP.update(
    {
        "updater": "**Plugin : **`updater`"
        "\n\n  •  **Syntax : **`.update`"
        "\n  •  **Function :** Checks if the main userbot repository has any updates "
        "and shows a changelog if so."
        "\n\n  •  **Syntax : **`.update now`"
        "\n  •  **Function :** Update your userbot, "
        "if there are any updates in your userbot repository.if you restart these goes back to last time when you deployed"
        "\n\n  •  **Syntax : **`.update deploy`"
        "\n  •  **Function :** Deploy your userbot.So even you restart it doesnt go back to previous version"
        "\nThis will triggered deploy always, even no updates."
        "\n\n  •  **Syntax : **`.badcat`"
        "\n  •  **Function :** Shifts from official cat repo to jisan's repo(for gali commands)"
    }
)
