import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord import option

class Query(commands.Cog):

    # Slash commands in group (/elevator tester and /elevator pinguser)
    test = SlashCommandGroup("elevator", "test")

    def __init__(self, bot):
        self.bot = bot

    # responds to command with user arguments, responds "none" otherwise.
    @test.command()
    @option("content", description="Enter something", default='none')
    async def tester(self, ctx: discord.ApplicationContext, content):
        if content != None:
            await ctx.respond(content)
        else:
            await ctx.respond("none")

    # pings the user which sent the command
    @test.command()
    async def pinguser(self, ctx: discord.ApplicationContext):
        await ctx.respond(f'<@!{ctx.author.id}>') 

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Query(bot))