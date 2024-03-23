import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord import option
from datetime import datetime


locations = {
    'mquni-escalator-up': {'name': 'University Escalator Up', 'message': None},
    'mquni-escalator-down': {'name': 'University Escalator Down', 'message': None},
    'mquni-lift': {'name': 'University Lift', 'message': None},
    'mqcentre-escalator-up': {'name': 'Centre Escalator Up', 'message': None},
    'mqcentre-escalator-down': {'name': 'Centre Escalator Down', 'message': None},
    'mqcentre-lift': {'name': 'Centre Lift', 'message': None},
    'concourse-escalator-up': {'name': 'Platform Escalator Up', 'message': None},
    'concourse-escalator-down': {'name': 'Platform Escalator Down', 'message': None},
    'concourse-lift': {'name': 'Platform Lift', 'message': None}
}
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
        statusUpdate(embed, locations['mquni-escalator-up']['name'], False)
        statusUpdate(embed, locations['mquni-escalator-down']['name'], True)
        statusUpdate(embed, locations['mquni-lift']['name'], True)
        statusUpdate(embed, locations['mqcentre-escalator-up']['name'], True)
        statusUpdate(embed, locations['mqcentre-escalator-down']['name'], True)
        statusUpdate(embed, locations['mqcentre-lift']['name'], True)
        statusUpdate(embed, locations['concourse-escalator-up']['name'], True)
        statusUpdate(embed, locations['concourse-escalator-down']['name'], True)
        statusUpdate(embed, locations['concourse-lift']['name'], True)
        await ctx.respond(embed=embed) 

    # send command, respond, delete after five seconds and add new message with status update with reaction
    @discord.command()
    @option("location", description="Location and direction of travel to be updated.", required=True, choices=[locations['mquni-escalator-up']['name'], locations['mquni-escalator-down']['name'], locations['mquni-lift']['name'], 
                                                                                                                locations['mqcentre-escalator-up']['name'], locations['mqcentre-escalator-down']['name'], locations['mqcentre-lift']['name'], 
                                                                                                                locations['concourse-escalator-up']['name'], locations['concourse-escalator-down']['name'], locations['concourse-lift']['name']])
    @option("status", description="Working/Broken", required=True, choices=['working', 'broken'])
    async def update(self, 
                     ctx: discord.ApplicationContext, location, status):
        try:
            is_working = True
            if status.lower() == 'broken':
                is_working = False
            embed = discord.Embed(
                title=f'Status update for {location}',
                description=f"{status.capitalize()} as of <t:{getCurrTime()}>",
                color=discord.Colour.red() # Pycord provides a class with default colors you can choose from
            )
            await ctx.respond(f'Report received!', delete_after=2)
            message = await ctx.channel.send(embed=embed)
            await message.add_reaction('✅')
        except ValueError:
            await ctx.respond(f'This location already has been reported!', delete_after=2)
        

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Query(bot))