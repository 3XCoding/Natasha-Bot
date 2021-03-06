#Made By @Don_Sflix

import os
import math
import time
from info import ADMINS
import heroku3
import requests
from pyrogram import Client, filters
from databasevs.users_chats_db import db

#=====================================================
BOT_START_TIME = time.time()
CMD = ['.', '/']
HEROKU_API_KEY = (os.environ.get("HEROKU_API_KEY", ""))
#=====================================================

@Client.on_message(filters.private & filters.user(ADMINS) & filters.command("dyno", CMD))         
async def bot_status_cmd(client,message):
    if HEROKU_API_KEY:
        try:
            server = heroku3.from_key(HEROKU_API_KEY)

            user_agent = (
                'Mozilla/5.0 (Linux; Android 10; SM-G975F) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/80.0.3987.149 Mobile Safari/537.36'
            )
            accountid = server.account().id
            headers = {
            'User-Agent': user_agent,
            'Authorization': f'Bearer {HEROKU_API_KEY}',
            'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
            }

            path = "/accounts/" + accountid + "/actions/get-quota"

            request = requests.get("https://api.heroku.com" + path, headers=headers)

            if request.status_code == 200:
                result = request.json()

                total_quota = result['account_quota']
                quota_used = result['quota_used']

                quota_left = total_quota - quota_used
                
                total = math.floor(total_quota/3600)
                used = math.floor(quota_used/3600)
                hours = math.floor(quota_left/3600)
                minutes = math.floor(quota_left/60 % 60)
                days = math.floor(hours/24)

                usedperc = math.floor(quota_used / total_quota * 100)
                leftperc = math.floor(quota_left / total_quota * 100)

#---------text--------π₯

                quota_details = f"""
π©ππ πΊπππππ:

β§ ππΎππ°π» π³ππ½πΎ : {total}π§ππππ π΅ππΎπΎ π³πππ!
 
β§ π³ππ½πΎ πππ΄π³ : {used} π§ππππ ( {usedperc}% )
        
β§ π³ππ½πΎ ππ΄πΌπ°πΈπ½πΈπ½πΆ : {hours} π§ππππ ( {leftperc}% )
        
β§ π°πΏπΏππΎππΈπΌπ°ππ΄ π³π°ππ : {days} Days left!"""

#----------end---------π―

            else:
                quota_details = ""
        except:
            print("Check your Heroku API key")
            quota_details = ""
    else:
        quota_details = ""

    uptime = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - BOT_START_TIME))

    try:
        t, u, f = shutil.disk_usage(".")
        total = humanbytes(t)
        used = humanbytes(u)
        free = humanbytes(f)

        disk = "\n**π«πππ π«ππππππ**\n\n" \
            f"β§ USED  :  {used} / {total}\n" \
            f"β§ FREE  :  {free}\n\n"
    except:
        disk = ""

    await message.reply_text(
        "<u> πππΏπΏπ²π»π πππ?πππ πΌπ³ ππΌππΏ ππΌπ</u>\n\n"
        "π«ππππͺπππππ πΊπππππ:\n"
        f"β§ π±πΎπ ππΏππΈπΌπ΄ : {uptime}\n"
        f"{quota_details}"
        f"{disk}",
        quote=True,
        parse_mode="md"
    )
