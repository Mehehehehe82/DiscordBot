"""A discord bot. Not much to see here"""
# bot.py
#  region Imports
import os
import sys
import re
import random
from datetime import datetime
from time import time
import pprint

from termcolor import colored
import discord
from discord.ext import commands
from dotenv import load_dotenv
import yaml
import conv
#import asyncio
#  endregion
#  region Constants


settings = {}
with open('config.yml') as f:
    settings = yaml.load(f, Loader=yaml.FullLoader)
load_dotenv()

TOKEN = ""
STATUS = os.getenv('DISCORD_BOT_STATUS')
prefixes = [
	"/onl ",			"/ONL ",
	".onl ",			".ONL ",
	"/tmy ",			"/TMY",
	".tmy ",			".TMY",
	"/tt ",				"/TT",
	".tt ",				".TT ",
	"/tommytrusty ",	"/TOMMYTRUSTY"
	"/tommy "			"/TOMMY"
]
# If your ID is in this array, you have access to dev commands such as /tt restart
# No, silly. Not your IP.
devs = settings['Authentication']['Authorized users']
bot = commands.Bot(command_prefix = prefixes)
#  endregion
#  region Functions
with open('badwords.txt','r') as f:
	bad_words = '|'.join(s for l in f for s in l.split(', '))
	bad_word_checker = re.compile(bad_words).search
async def prettymsg(ctx,
	msg: str = "Sample text be like bruh",
	Header: str = "Hey!",
	RawText: str = "", # Good for mentioning people
	ThumbnailURI: str = "https://i.imgur.com/VGJMhX6.jpg",
	colorHex: int = 0xb86767
):
	'''A quick embed creator with customizable defaults,'''
	embed=discord.Embed(title=Header, description=msg, color=colorHex)
	embed.set_thumbnail(url=ThumbnailURI)
	if conv.is_modified: # Set this to false if you modify the code for your own use
		embed.set_footer(text=f"Discord bot created by hyperboid. {conv.postmessage}")
	else:
		embed.set_footer(text=f"Based on the Discord bot created by hyperboid. {conv.postmessage}")
	await ctx.send(RawText, embed=embed)
def Log(Message: str, MessageType: str="INFO"):
	'''Logs stuff. What else can I say?'''
	timestamp = round(time())
	dt_object = datetime.fromtimestamp(timestamp)
	logtext = f"{dt_object} [{MessageType}] {Message}"
	print(logtext)
	file1 = open("bot.log", "a")
	file1.write(f'{logtext}\n')
	file1.close()
#  endregion
#  region Commands
@bot.command(
	name="test",
	brief="Hello World!",
	help="Makes the bot say \"Hello World!\" followed by a pseudo-random number."
)

async def test(ctx):
	'''Hello world command'''
	await prettymsg(ctx, f"Hello World! {random.randint(0,5) } ")
@bot.command(
	name="echo",
	brief="Makes the bot say something.",
	help="Makes the bot say something. Note that your name will be attached to the message."
)
async def command_echo(ctx,*args):
	'''See help.'''
	if not isinstance(ctx.channel, discord.channel.DMChannel):
		await ctx.message.delete()
	embed=discord.Embed(title=" ".join(args))
	embed.set_author(name=f"As {ctx.author.name} once said...")
	await ctx.send(embed=embed)
@bot.command(name='id', brief="Shows your discord ID.")
async def command_id(ctx):
	'''See help.'''
	await prettymsg(ctx, f'''Your ID is {str(ctx.message.author.id)}''')
@bot.command(name="restart", aliases=['reload', 'rl', 'reboot'], brief="Restarts the bot")
async def command_reboot(ctx):
	'''See help.'''
	if ctx.message.author.id in devs:
		await ctx.send("Restarting!")
		Log("-------------------------------------------------------------", "WARN")
		Log("Any error messages beyond this point are completely normal.  ", "WARN")
		Log("  I don't know how to fix them. DO NOT REPORT THEM TO ME.    ", "WARN")
		Log("-------------------------------------------------------------", "WARN")
		quit()
	else:
		await prettymsg(ctx, "You are not authorized to reboot the bot.")
@bot.command(
	name="weirdchamp",
	brief="Says that someone is WeirdChamp.",
	help="Accuses someone (not sure who) of being \"WeirdChamp\". Not sure why I added this."
)
async def command_weirdchamp(ctx):
	'''See help.'''
	await prettymsg(ctx, "that's kinda Weird champ <:WeirdChamp:799371267849453581> of you", "Bro")

@bot.command(name="emoji", brief="Shows a bunch of emojis")
async def command_emoji(ctx):
	'''See help.'''
	await prettymsg(ctx,
'''Emoji test
<:WeirderChamp:799375703387668541>
<:WeirdChamp:799375581984456724>
<:SadChampo:799375703387930654>
<:PauseChamp:799375703933845535>
<:E:799375750095437855><:E:799375788016533504><:E:799375829863366658><:E:799375864856576092>'''
	)

@bot.command(name="swears", brief="Lists swears")
async def command_swears(ctx, confirm: bool=False):
	'''See help.'''
	if confirm:
		await prettymsg(ctx, "Not yet implemented")
	else:
		await prettymsg(ctx, "Do you really want to see the swear list? Do `/tt swears True` to confirm.")
@bot.command(
	name="clean",
	brief="Cleans the channel",
	help="Deletes a bunch of messages at once."
)
async def command_clean(ctx, limit: int):
	'''See help.'''
	try:
		await ctx.channel.purge(limit=limit, bulk=False)
		await ctx.send(f'Cleared by {ctx.author.mention}')
		await ctx.message.delete()
	except discord.Forbidden:
		await prettymsg(ctx, "No permission.", "Error")
	except AttributeError:
		await prettymsg(ctx, "Some sort of AttributeError was thrown. wat", "Error")

#  endregion
#  region Events


@bot.event
async def on_ready():
	'''Runs when the bot gets online.'''
	Log("Connected!")
	await bot.change_presence(
		activity=discord.Activity(
			type=discord.ActivityType.watching,
			name=STATUS
		)
	)

@bot.event
async def on_message(message):
	'''Swear filter and message logging.'''
	if settings["Logging"]["Log messages to terminal"]:
		Log(f'''User {message.author.name} sent message "{message.content}"''', "VERB")
	if message.channel.name != "announcements" and settings['Swear filter']['Enabled']:
		if bad_word_checker(message.content):
			if settings["Logging"]["Log messages to terminal"]:
				Log("The message above was filtered for swearing.", "VERB")
			await message.delete()
			await prettymsg(message.channel, "\n".join(settings["Swear filter"]["Message"]),
			RawText=message.author.mention)
	else:
		await bot.process_commands(message)
#  endregion
Log("--- STARTING UP... ---")

try:
	f = open(settings["Authentication"]["Bot token file"])
	Log(pprint.pformat(f.read()))
	bot.run(f.read())
	f.close()
		# TOKEN = f
except:
	e = sys.exc_info()[0]
	Log("An error has occurred.", "CRITICAL")
	Log(pprint.pformat(e), "CRITICAL")
	raise
