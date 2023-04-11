import discord
import os
from discord.ext import commands, tasks

TOKEN = "YOUR_TOKEN"
YOUR_USER_ID = "YOUR_USER_ID" # Should be an 18-digit integer
VIDEO_DIR = "./video_cache/"

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    send_new_videos.start()

@tasks.loop(seconds=300) # Checks for new videos every 5 minutes
async def send_new_videos():
    user = await bot.fetch_user(YOUR_USER_ID)
    video_files = os.listdir(VIDEO_DIR) # Looks for new video files in video directory
    print(video_files)
    for video_file in video_files: # Loops through found videos
        with open(VIDEO_DIR+video_file, 'rb') as f:
            await user.send(file=discord.File(f)) # Sends video files to specified user
        os.remove(VIDEO_DIR+video_file) # Deletes local file to avoid clogging local storage

bot.run(TOKEN)
