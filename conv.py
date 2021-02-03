"""Convenience functions go here"""
import discord
#  region Constants
is_modified = False # Set this to True if you modify the code for your own use.
GITHUB_URL = "https://github.com/Mehehehehe82/BotInnit"
postmessage = f"It's open source, check it out on github! {GITHUB_URL}"
#  endregion
#  region Functions
async def prettymsg(ctx,
	msg: str = "Sample text be like bruh",
	Header: str = "Hey!",
	RawText: str = "", # Good for mentioning people
	ThumbnailURI: str = "https://cdn.discordapp.com/avatars/783773656227512331/e6db612b2f469225fda5522f3e915d7a.webp",
	colorHex: int = 0xb86767
):
	'''A simple embed creator with customizable defaults,'''
	embed=discord.Embed(title=Header, description=msg, color=colorHex)
	embed.set_thumbnail(url=ThumbnailURI)
	if is_modified:
		embed.set_footer(text=f"Based on the Discord bot created by hyperboid. {postmessage}")
	else:
		embed.set_footer(text=f"Discord bot created by hyperboid. {postmessage}")
	await ctx.send(RawText, embed=embed)
#  endregion
