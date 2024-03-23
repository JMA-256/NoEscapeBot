import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord import option
from datetime import datetime

# Dictionary of locations comprising of location names and the last status update message ID.
# Key corresponds to location ID in backend.
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

# Helper functions for converting time into an integer Unix time for Discord messages.
def datetimeToDiscord(input_time):
    return int(input_time)

def getCurrTime():
    return int(datetime.timestamp(datetime.now()))

# TODO:
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

    # Placeholder command group /elevator
    test = SlashCommandGroup("elevator", "test")

    def __init__(self, bot):
        self.bot = bot

    # Test command which responds to user arguments, responds "none" if none provided.
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
        # Create the response message.
        embed = discord.Embed(
            title="MQ Station Status",
            description=f"Status as of <t:{getCurrTime()}>",
            color=discord.Colour.brand_green() # Pycord provides a class with default colors you can choose from
        )
        # Add fields corresponding to each location. Boolean values are placeholders.
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

    # Update command takes user arguments and updates the status of the location provided.
    @discord.command()
    @option("location", description="Location and direction of travel to be updated.", required=True, choices=[discord.OptionChoice(locations['mquni-escalator-up']['name'], value='mquni-escalator-up'), 
                                                                                                               discord.OptionChoice(locations['mquni-escalator-down']['name'], value='mquni-escalator-down'), 
                                                                                                               discord.OptionChoice(locations['mquni-lift']['name'], value='mquni-lift'), 
                                                                                                               discord.OptionChoice(locations['mqcentre-escalator-up']['name'], value='mqcentre-escalator-up'), 
                                                                                                               discord.OptionChoice(locations['mqcentre-escalator-down']['name'], value='mqcentre-escalator-down'), 
                                                                                                               discord.OptionChoice(locations['mqcentre-lift']['name'], value='mqcentre-lift'), 
                                                                                                               discord.OptionChoice(locations['concourse-escalator-up']['name'], value='concourse-escalator-up'), 
                                                                                                               discord.OptionChoice(locations['concourse-escalator-down']['name'], value='concourse-escalator-down'), 
                                                                                                               discord.OptionChoice(locations['concourse-lift']['name'], value='concourse-lift')])
    @option("status", description="Working/Broken", required=True, choices=['working', 'broken'])
    async def update(self, 
                     ctx: discord.ApplicationContext, location, status):
        try:
            # Convert the status from the status argument into boolean values.
            is_working = True
            if status.lower() == 'broken':
                is_working = False
            
            # Create the response message
            location_name = locations[location]['name']
            embed = discord.Embed(
                title=f'Status update for {location_name}',
                description=f"{status.capitalize()} as of <t:{getCurrTime()}>",
                color=discord.Colour.red() # Pycord provides a class with default colors you can choose from
            )
            # Give user acknowledgement, send the status update message, add the tick reaction and store the message ID in the locations dict.
            await ctx.respond(f'Report received!', delete_after=2)
            message = await ctx.channel.send(embed=embed)
            await message.add_reaction('✅')
            locations[location]['message'] = message.id

        except ValueError:
            await ctx.respond(f'This location already has been reported!', delete_after=2)
        

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Query(bot))