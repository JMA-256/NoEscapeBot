import discord
from discord import option

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
  # Get token from token.txt file
  f = open("token.txt", 'r')
  token = f.readline().rstrip()
  try:
    client.run(token)
  except:
    print('Bot disconnected')