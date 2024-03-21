import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord import option
import datetime
import time

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
    async def status(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="MQ Station Status",
            description=f"Status as of <t:{int(time.mktime((datetime.datetime.now()).timetuple()))}>",
            color=discord.Colour.brand_green() # Pycord provides a class with default colors you can choose from
        )
        embed.add_field(name="University Escalator Up", value="Status", inline=True)
        embed.add_field(name="University Escalator Down", value="Status", inline=True)
        embed.add_field(name="University Elevator", value="Status", inline=True)
        embed.add_field(name="Centre Escalator Up", value="Status", inline=True)
        embed.add_field(name="Centre Escalator Down", value="Status", inline=True)
        embed.add_field(name="Centre Elevator", value="Status", inline=True)
        embed.add_field(name="Concourse Escalator Up", value="Status", inline=True)
        embed.add_field(name="Concourse Escalator Down", value="Status", inline=True)
        embed.add_field(name="Concourse Elevator", value="Status", inline=True)
        await ctx.respond(embed=embed) 

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Query(bot))