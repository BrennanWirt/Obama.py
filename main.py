import os
import requests
import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--test-type")
driver = webdriver.Chrome(options=chrome_options)
driver.get('http://talkobamato.me/')


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = commands.Bot(command_prefix='!', case_insensitive=True)




@client.event
async def on_ready():
    print('Hello my fellow Americans')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name = ('my fellow Americans')))


@client.command()
async def obama(ctx):
  file_there = os.path.isfile("obama.mp4")
  voice = get(client.voice_clients, guild=ctx.guild)
  message = ctx.message 
  ogmsg = message.content
  size = len(ogmsg)
  if size > 280:
    size2 = size - 280
    mod_string = ogmsg[:size-size2]
  else:
    mod_string = ogmsg
  channel = message.author.voice.channel
  msg = mod_string.replace("!obama", "")
  text_area = driver.find_element_by_id('input_text')
  text_area.clear()
  text_area.send_keys(msg)
  talkbtn = driver.find_element_by_id('talk_button')
  talkbtn.click()
  url1 = driver.current_url
  url2 = url1.split('=') 
  del url2[0]
  print(url2)
  url3 = "".join(url2)
  url4 = 'http://talkobamato.me/synth/output/' + url3 +'/obama.mp4'
  print(url4)
  name='obama.mp4'
  r=requests.get(url4)
  print("****Connected****")
  if file_there:
      os.remove('obama.mp4')
  f=open(name,'wb');
  print("Donloading.....")
  for chunk in r.iter_content(chunk_size=255): 
      if chunk: # filter out keep-alive new chunks
            f.write(chunk)
  print("Done")
  f.close()
  if not channel:
      await message.send("You are not connected to a voice channel.")
      return
  voice = get(client.voice_clients, guild=ctx.guild)
  if voice and voice.is_connected():
          await voice.move_to(channel)
  else:
      voice = await channel.connect()
  voice.play(discord.FFmpegOpusAudio("obama.mp4"))

client.run(TOKEN)




