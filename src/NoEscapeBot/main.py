import os
from dotenv import load_dotenv
import discord

# load env variables from .env
load_dotenv()

client = discord.Bot()

# cogs
cogs_list = [
  'query'
]

# load cogs in cogs_list
for cog in cogs_list:
    client.load_extension(f'cogs.{cog}')

# placeholder commands
# responds to command with "placeholder"
@client.command(name="help")
async def help(ctx):
  await ctx.respond("placeholder")

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))

if __name__ == "__main__":
  try:
    client.run(os.getenv('TOKEN'))
  except:
    print('Bot disconnected')