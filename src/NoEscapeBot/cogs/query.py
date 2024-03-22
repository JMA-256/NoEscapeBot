import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord import option
from datetime import datetime

def datetimeToDiscord(input_time):
    return int(input_time)

def getCurrTime():
    return int(datetime.timestamp(datetime.now()))

# Helper function to query data from the backend to assemble /status
# Query object will be a list of locations JSON with {Name: string, Status: bool, Verified: timestamp or null}
# Return string with list of broken locations and verified timestamp (if any)
def getStatus():
    return None

# helper function for updating status
def statusUpdate(embed, location, status):
    if status:
        embed.add_field(name=location, value="✅", inline=True)
    else:
        embed.add_field(name=location, value="❌", inline=True)

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

    # Status command with default behaviour.
    @discord.command()
    async def status(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="MQ Station Status",
            description=f"Status as of <t:{getCurrTime()}>",
            color=discord.Colour.brand_green() # Pycord provides a class with default colors you can choose from
        )   
        embed.add_field(name="The following elevators/escalators are broken:", value="None", inline=True)
        await ctx.respond(embed=embed) 

    # Status command displaying the status of all possible locations.
    @discord.command()
    async def fullstatus(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="MQ Station Status",
            description=f"Status as of <t:{getCurrTime()}>",
            color=discord.Colour.brand_green() # Pycord provides a class with default colors you can choose from
        )
        statusUpdate(embed, "University Escalator Up", False)
        statusUpdate(embed, "University Escalator Down", True)
        statusUpdate(embed, "University Elevator", True)
        statusUpdate(embed, "Centre Escalator Up", True)
        statusUpdate(embed, "Centre Escalator Down", True)
        statusUpdate(embed, "Centre Elevator", True)
        statusUpdate(embed, "Concourse Escalator Up", True)
        statusUpdate(embed, "Concourse Escalator Down", True)
        statusUpdate(embed, "Concourse Elevator", True)
        await ctx.respond(embed=embed) 

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Query(bot))