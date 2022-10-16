import discord
from discord.ext import commands
import requests
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL.Image import Resampling
from datetime import datetime, time, timedelta
import asyncio

token="five"
client = commands.Bot(command_prefix="")
updateTime = time(22, 1, 0)  # 11:01 PM bri'ish time

@client.event
async def on_ready():
    print("Bot online")
    
async def called_once_a_day():
    getImage()
    channel = client.get_channel(1031184476631486494)
    await channel.send("NEW INTEGRAL DROPPED!", file=discord.File("int.png"))
    channel = client.get_channel(914952610467946506)
    await channel.send("NEW INTEGRAL DROPPED!", file=discord.File("int.png"))

async def background_task():
    now = datetime.utcnow()
    if now.time() > updateTime:
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()
        await asyncio.sleep(seconds)
    while True:
        now = datetime.utcnow()
        target_time = datetime.combine(now.date(), updateTime)
        seconds_until_target = (target_time - now).total_seconds()
        await asyncio.sleep(seconds_until_target)
        await called_once_a_day()
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()
        await asyncio.sleep(seconds)

def getImage():
    url = "https://www.sammserver.com/iotd/int.svg"
    r = requests.get(url, allow_redirects=True)
    open('int.svg', 'wb').write(r.content)

    s1 = 10
    s2 = 10
    sample = Resampling.BICUBIC
    svg = svg2rlg("int.svg")
    svg.scale(s1,s1)
    print("success")
    png = renderPM.drawToPIL(svg, dpi = 72*s1)

    og = [png.width, png.height]
    og = [o*s2 for o in og]
    png = png.resize(og, resample=sample) 

    png.save("int.png")

client.loop.create_task(background_task())
client.run(token)