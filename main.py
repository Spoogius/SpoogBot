import discord
import json
from commands.wordleScoreboard import *


def __main__( ):
  # Open discord bot config file
  with open( 'config.json', 'r' ) as cfgIn:
    cfg = json.load( cfgIn );
    cfgIn.close( );


  client = discord.Client( );

  @client.event
  async def on_ready( ):
    print( "Bot Connected\n" );

  @client.event
  async def on_message( message ):
    # Is DM
    if(  message.channel.type  == discord.ChannelType.private ): 
      await message.add_reaction( '💦' );
      return;

    #If message not sent by bot
    if( message.author != client.user ):
      
      # Starts with CMD_PREFIX
      if( message.content.startswith( cfg["CMD_PREFIX"] ) ):
        #Wordle Scoreboard command
        if( "scoreboard" in message.content.lower( ) ):        
          await wordleScoreboard( message );

  client.run( cfg['BOT_TOKEN'] );

__main__( );
