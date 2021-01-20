# bot.py
#  region Imports
import os
import re
import asyncio
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
#  endregion
#  region Constants
settings = {
	"verbose": True
}
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
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
devs = [
	453204873346023424, # Hyperboid, me
	676572364460392498 # another person
]
bot = commands.Bot(command_prefix = prefixes)
#  endregion
#  region Convenience functions
async def prettymsg(ctx,
	msg: str = "Sample text be like bruh",
	Header: str = "Hey!",
	RawText: str = "", # Good for mentioning people
	ThumbnailURI: str = "https://cdn.discordapp.com/avatars/783773656227512331/e6db612b2f469225fda5522f3e915d7a.webp",
	colorHex: int = 0xb86767
):
	'''A quick embed creator with customizable defaults,'''
	embed=discord.Embed(title=Header, description=msg, color=colorHex)
	embed.set_thumbnail(url=ThumbnailURI)
	if True: # Set this to false if you modify the code for your own use
		embed.set_footer(text="Discord bot created by hyperboid. It's open source, check it out on github! https://github.com/Mehehehehe82/BotInnit")
	else:
		embed.set_footer(text="Based on the Discord bot created by hyperboid. It's open source, check it out on github! https://github.com/Mehehehehe82/BotInnit")
	await ctx.send(RawText, embed=embed)
#  endregion
#  region Commands
@bot.command(
	name="test",
	brief="Hello World!",
	help="Makes the bot say \"Hello World!\" followed by a pseudo-random number."
)
async def test(ctx):
	await prettymsg(ctx, f"Hello World! {random.randint(0,5) } ")
@bot.command(
	name="echo",
	brief="Makes the bot say something.",
	help="Makes the bot say something. Note that your name will be attached to the message."
)
async def command_echo(ctx,*args):
	if not isinstance(ctx.channel, discord.channel.DMChannel):
		await ctx.message.delete()
	embed=discord.Embed(title=" ".join(args))
	embed.set_author(name=f"As {ctx.author.name} once said...")
	await ctx.send(embed=embed)
@bot.command(name='id')
async def command_id(ctx):
	await prettymsg(ctx, f'''Your ID is {str(ctx.message.author.id)}''')
@bot.command(name="restart", aliases=['reload', 'rl', 'reboot'])
async def command_reboot(ctx):
	if (ctx.message.author.id in devs):
		await ctx.send("Restarting!")
		quit()
	else:
		await prettymsg(ctx, "You are not authorized to reboot the bot.")
@bot.command(
	name="weirdchamp",
	brief="Says that someone is WeirdChamp.",
	help="Accuses someone (not sure who) of being \"WeirdChamp\". Not sure why I added this."
)
async def command_weirdchamp(ctx):
	await prettymsg(ctx, "that's kinda Weird champ <:WeirdChamp:799371267849453581> of you", "Bro")

@bot.command(name="emoji", brief="Shows a bunch of emojis")
async def command_emoji(ctx):
	await prettymsg(ctx, "Emoji test\n<:WeirderChamp:799375703387668541> <:WeirdChamp:799375581984456724> <:SadChampo:799375703387930654> <:PauseChamp:799375703933845535> <:Champ_0_0:799375750095437855><:Champ_1_0:799375788016533504><:Champ_2_0:799375829863366658><:Champ_3_0:799375864856576092>")

@bot.command(name="swears")
async def command_swears(ctx, confirm: bool=False):
	if (confirm):
		await prettymsg(ctx, "Not yet implemented")
	else:
		await prettymsg(ctx, "Do you really want to see the swear list? Do `/tt swears True` to confirm.")
@bot.command(
	name="clean",
	brief="Cleans the channel",
	help="Makes the bot say something. Note that your name will be attached to the message."
)
async def command_clean(ctx, limit: int):
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
with open('badwords.txt','r') as f:
	bad_words = '|'.join(s for l in f for s in l.split(', '))
	bad_word_checker = re.compile(bad_words).search

@bot.event
async def on_ready():
	print("---   CONNECTED.   ---")
	print("Connected!")
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=STATUS))

@bot.event 
async def on_message(message):
	if settings["verbose"]:
		print(f'''[VB] User {message.author.name} sent message "{message.content}"''')
	else:
		print('Someone sent a message but verbose is off.')
	if bad_word_checker(message.content):
		await message.delete()
		await prettymsg(message.channel, "Only I'm allowed to `fricking` swear! <:WC:799371267849453581>.")
	else:
		await bot.process_commands(message)
#  endregion
print("--- STARTING UP... ---")
bot.run(TOKEN)
