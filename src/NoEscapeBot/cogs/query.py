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

# helper function for updating full status
# TODO: Modify code to take the Status object as input and add all fields as needed.
def statusUpdate(embed, location, status):
    if status:
        embed.add_field(name=location, value="✅", inline=True)
    else:
        embed.add_field(name=location, value="❌", inline=True)

# TODO: Modify code to take the Status object as input and return a string to be added.
def defaultStatusUpdate(embed, location, status):
    return None


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
        statusUpdate(embed, "University Lift", True)
        statusUpdate(embed, "Centre Escalator Up", True)
        statusUpdate(embed, "Centre Escalator Down", True)
        statusUpdate(embed, "Centre Lift", True)
        statusUpdate(embed, "Platform Escalator Up", True)
        statusUpdate(embed, "Platform Escalator Down", True)
        statusUpdate(embed, "Platform Lift", True)
        await ctx.respond(embed=embed) 

    @discord.command()
    @option("location", description="Location and direction of travel to be updated.", required=True, choices=['University Escalator Up', 'University Escalator Down', 'University Lift', 
                                                                                                                'Centre Escalator Up', 'Centre Escalator Down', 'Centre Lift', 
                                                                                                                'Platform Escalator Up', 'Platform Escalator Down', 'Platform Lift'])
    @option("status", description="Working/Broken", required=True, choices=['working', 'broken'])
    async def update(self, 
                     ctx: discord.ApplicationContext, location, status):
        is_working = True
        if status.lower() == 'broken':
            is_working = False
        await ctx.respond(f'Setting status of {location}.\n{location} working is {is_working} as of <t:{getCurrTime()}>.')
        

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Query(bot))