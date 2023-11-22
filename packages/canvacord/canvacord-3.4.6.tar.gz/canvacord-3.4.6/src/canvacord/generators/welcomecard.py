from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageColor
import asyncio
import aiohttp
from io import BytesIO
import discord
from typing import Union
from colour import Color

async def getavatar(user: discord.Member) -> bytes:
    session = aiohttp.ClientSession(loop=asyncio.get_event_loop())
    disver = str(discord.__version__)
    if disver.startswith("1"):
        async with session.get(str(user.avatar_url)) as response:
            avatarbytes = await response.read()
        await session.close()
    elif disver.startswith("2"):
        async with session.get(str(user.display_avatar.url)) as response:
            avatarbytes = await response.read()
        await session.close()
    return avatarbytes

async def getbackground(background):
    session = aiohttp.ClientSession(loop=asyncio.get_event_loop())
    try:
        async with session.get(str(background)) as response:
            backgroundbytes = await response.read()
    except:
        background = "https://cdn.glitch.com/dff50ce1-3805-4fdb-a7a5-8cabd5e53756%2Fblankrank.png?v=1628032652421"
        async with session.get(str(background)) as response:
            backgroundbytes = await response.read()
    await session.close()
    return backgroundbytes

async def gettemplate(backtype, backdata=None):
    session = aiohttp.ClientSession(loop=asyncio.get_event_loop())
    if backdata == None:
        if backtype == "normal":
            background = "https://cdn.glitch.com/dff50ce1-3805-4fdb-a7a5-8cabd5e53756%2Fblankrank.png?v=1628032652421"
            async with session.get(str(background)) as response:
                backgroundbytes = await response.read()
        elif backtype == "transparent":
            background = "https://cdn.glitch.com/dff50ce1-3805-4fdb-a7a5-8cabd5e53756%2Fblankopacityrank.png?v=1628032645740"
            async with session.get(str(background)) as response:
                backgroundbytes = await response.read()
        elif backtype == "font":
            background = "https://cdn.glitch.com/dff50ce1-3805-4fdb-a7a5-8cabd5e53756%2FCalibri-Regular.ttf?v=1628033016557"
            async with session.get(str(background)) as response:
                backgroundbytes = await response.read()
        elif backtype == "welcome":
            background = "https://cdn.glitch.global/dff50ce1-3805-4fdb-a7a5-8cabd5e53756/thumbnails%2Fimage.png?1700612054798"
            async with session.get(str(background)) as response:
                backgroundbytes = await response.read()
    else:
        try:
            if backtype == "normal":
                async with session.get(str(backdata)) as response:
                    backgroundbytes = await response.read()
            elif backtype == "transparent":
                async with session.get(str(backdata)) as response:
                    backgroundbytes = await response.read()
            elif backtype == "font":
                async with session.get(str(backdata)) as response:
                    backgroundbytes = await response.read()
            elif backtype == "welcome":
                async with session.get(str(backdata)) as response:
                    backgroundbytes = await response.read()
        except:
            if backtype == "normal":
                background = "https://cdn.glitch.com/dff50ce1-3805-4fdb-a7a5-8cabd5e53756%2Fblankrank.png?v=1628032652421"
                async with session.get(str(background)) as response:
                    backgroundbytes = await response.read()
            elif backtype == "transparent":
                background = "https://cdn.glitch.com/dff50ce1-3805-4fdb-a7a5-8cabd5e53756%2Fblankopacityrank.png?v=1628032645740"
                async with session.get(str(background)) as response:
                    backgroundbytes = await response.read()
            elif backtype == "font":
                background = "https://cdn.glitch.com/dff50ce1-3805-4fdb-a7a5-8cabd5e53756%2FCalibri-Regular.ttf?v=1628033016557"
                async with session.get(str(background)) as response:
                    backgroundbytes = await response.read()
            elif backtype == "welcome":
                background = "https://cdn.glitch.global/dff50ce1-3805-4fdb-a7a5-8cabd5e53756/thumbnails%2Fimage.png?1700612054798"
                async with session.get(str(background)) as response:
                    backgroundbytes = await response.read()
    await session.close()
    return backgroundbytes

async def welcomecard(user:discord.Member, background=None, avatarcolor="white", topcolor="white", bottomcolor="white", backgroundcolor="black", font=None, toptext="Welcome {user_name}!", bottomtext="Enjoy your stay in {server}!"):
        toptext = toptext.replace("{user_name}", user.name)
        bottomtext = bottomtext.replace("{user_name}", user.name)
        toptext = toptext.replace("{server}", user.guild.name)
        bottomtext = bottomtext.replace("{server}", user.guild.name)
        ac = Color(avatarcolor)
        tc = Color(topcolor)
        bc = Color(bottomcolor)
        bgc = Color(backgroundcolor)
        medium_font = ImageFont.FreeTypeFont(BytesIO(await gettemplate("font", font)), 50, encoding="utf-8")
        with Image.open(BytesIO(await getavatar(user))) as im:
            im = im.resize((256, 256))
            rgbavatar = im.convert("RGB")
            if background == None:
                background = Image.new("RGB", (1024, 500), bgc.hex_l)
                draw = ImageDraw.Draw(background)
            else:
                with Image.open(BytesIO(await getbackground(background))) as background:
                    background = background.resize((934, 282))
                    draw = ImageDraw.Draw(background)
                    opacity = Image.open(BytesIO(await gettemplate("transparent"))).convert("RGBA")
                    newbackground = background.convert("RGBA")
                    width = (background.width - newbackground.width) // 2
                    height = (background.height - newbackground.height) // 2
                    background.paste(opacity, (width, height), opacity)
                    draw.ellipse((35, 57, 206, 226), fill=0)
            draw.ellipse([(384, 19), (640, 275)], fill=ac.hex_l)
            with Image.new("L", im.size, 0) as mask:
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.ellipse([(20, 20), im.size], fill=255)
                background.paste(rgbavatar, (374, 10), mask=mask)
            msg1 = toptext
            w = medium_font.getlength(msg1)
            draw.text(((1024-w)/2,300), msg1, fill=tc.hex_l, font=medium_font)
            msg2 = bottomtext
            w = medium_font.getlength(msg2)
            draw.text(((1024-w)/2,375), msg2, fill=bc.hex_l, font=medium_font)
            final_buffer = BytesIO()
            background.save(final_buffer, "png")
            final_buffer.seek(0)
            return final_buffer