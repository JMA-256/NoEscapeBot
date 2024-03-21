import os
from dotenv import load_dotenv
import discord
from discord import option

# load env variables from .env
load_dotenv()

client = discord.Bot()

# placeholder test group
test = client.create_group("elevator", "testing functions")

# placeholder commands

# responds to command with "placeholder"
@client.command(name="help")
async def help(ctx):
  await ctx.respond("placeholder")

# responds to command with user arguments, responds "none" otherwise.
@test.command()
@option("content", description="Enter something", default='none')
async def tester(ctx, content):
  if content != None:
    await ctx.respond(content)
  else:
    await ctx.respond("none")

# pings the user which sent the command
@test.command()
async def pinguser(ctx):
  await ctx.respond(f'<@!{ctx.author.id}>')

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))

if __name__ == "__main__":
  try:
    client.run(os.getenv('TOKEN'))
  except:
    print('Bot disconnected')