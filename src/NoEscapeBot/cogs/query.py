import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord import option
from datetime import datetime
import os
from dotenv import load_dotenv
import ap_statuses
load_dotenv()

# Location statuses
location_status = ap_statuses.Statuses()

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


# Helper function to query data from the backend to assemble /status
# Query object will be a dict of locations with {Name: string, Status: bool, Verified: timestamp or null}
# Return string with list of broken locations and verified timestamp (if any)
def getStatus():
    status = location_status.get_all_statuses()
    broken_locations = []
    for key, val in status.items():
        if val['is_working'] == False:
            broken_locations.append(key)
    return broken_locations

def defaultStatusUpdate():
    broken_locations = getStatus()
    message = ""
    for key in broken_locations:
        val = location_status.get_status(key)['verified']
        name = locations[key]['name']
        if val == None:
            message += f"- {name}\n"
        else:
            message += f"- {name} (Verified as of <t:{datetimeToDiscord(val)}>)\n"
    if (len(message) == 0):
        message += "All locations working!"
    return message

# helper function for updating full status
def statusUpdate(embed):
    status = location_status.get_all_statuses()
    for key, val in status.items():
        if val['is_working'] == True:
            if val['verified'] == None:
                embed.add_field(name=locations[key]['name'], value="✅", inline=True)
            else:
                time = datetimeToDiscord(val['verified'])
                embed.add_field(name=locations[key]['name'], value=f"✅\nVerified at <t:{datetimeToDiscord(time)}>", inline=True)
        else:
            if val['verified'] == None:
                embed.add_field(name=locations[key]['name'], value="❌", inline=True)
            else:
                time = datetimeToDiscord(val['verified'])
                embed.add_field(name=locations[key]['name'], value=f"❌\nVerified at <t:{datetimeToDiscord(time)}>", inline=True)


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
        embed.add_field(name="The following lifts/escalators are broken:", value=defaultStatusUpdate(), inline=True)
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
        statusUpdate(embed)
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

            location_status.set_status(location, is_working, ctx.author)
            
            # Create the response message
            location_name = locations[location]['name']
            embed = discord.Embed(
                title=f'Status update for {location_name}',
                description=f"{status.capitalize()} as of <t:{getCurrTime()}>",
                color=discord.Colour.red()
            )
            # Give user acknowledgement, send the status update message, add the tick reaction and store the message ID in the locations dict.
            await ctx.respond(f'Report received!', delete_after=2)
            message = await ctx.channel.send(embed=embed)
            await message.add_reaction('✅')
            locations[location]['message'] = message.id

        except ValueError:
            await ctx.respond(f'This location already has been reported!', delete_after=2)

    # Detect reaction and increment reaction count by 1
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # TODO: Bot should not count itself as a reaction using payload.user_id != os.getenv('BOT_ID') (Removed due to unexpected behaviour for now.)
        if (payload.emoji.name == '✅'):
            for key, value in locations.items():
                if payload.message_id == value['message']:
                    location_status.verify_status(key)
                    # print(location_status.get_status(key)['votes'])
                    # Test functionality- responds with reaction added and link to message. Final functionality will increment count in backend.
                    # message = await channel.send(f'Reaction added to https://discord.com/channels/{payload.guild_id}/{payload.channel_id}/{payload.message_id}.')
                    # await message.edit(suppress=True)

            
    # Detect removal of reaction and decrement counter by 1
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # env variable not needed as the bot should not remove its own reaction.
        if (payload.emoji.name == '✅'):
            for key, value in locations.items():
                channel = self.bot.get_channel(payload.channel_id)
                if payload.message_id == value['message']:
                    location_status.unverify_status(key)
                    # print(location_status.get_status(key)['votes'])
                    # Test functionality- responds with reaction added and link to message. Final functionality will decrement count in backend.
                    # message = await channel.send(f'Reaction removed from https://discord.com/channels/{payload.guild_id}/{payload.channel_id}/{payload.message_id}.')
                    # await message.edit(suppress=True)
        

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Query(bot))