import os
import shutil
from web_dl import urlDownloader
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "5425537073:AAGAXtosFuJoFmEyhiUQ_I4TEFF-W-P1syA"
API_ID = "13221029"
API_HASH = "8ee3c5bfe718a463900933d8f6ef0158"

Bot = Client(
    "WebDL-Bot",
    bot_token = BOT_TOKEN,
    api_id = API_ID,
    api_hash = API_HASH
)

START_TXT = """
Hi {}, I am Web Downloader Bot.
I can download all the components (.html, .css, img, xml, video, javascript..) from URLs.
Send any URL,
for ex: 'https://www.google.com'
"""

START_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Owner', url='https://t.me/JefersonBP2801'),
        ]]
    )


@Bot.on_message(filters.command(["start"]))
async def start(bot, update):
    text = START_TXT.format(update.from_user.mention)
    reply_markup = START_BTN
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )




@Bot.on_message(filters.private & filters.text & ~filters.regex('/start'))
async def webdl(_, m):

    if not m.text.startswith('http'):
        return await m.reply("the URL must start with 'http' or 'https'")

    msg = await m.reply('Processing..')
    url = m.text
    name = dir = str(m.chat.id)
    if not os.path.isdir(dir):
        os.makedirs(dir)

    obj = urlDownloader(imgFlg=True, linkFlg=True, scriptFlg=True)
    res = obj.savePage(url, dir)
    if not res:
        return await msg.edit('something went wrong!')

    shutil.make_archive(name, 'zip', base_dir=dir)
    await m.reply_document(name+'.zip')
    await msg.delete()

    shutil.rmtree(dir)
    os.remove(name+'.zip')



Bot.run()