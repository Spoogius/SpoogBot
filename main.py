import discord
import json
from commands.wordleScoreboard import *
from commands.wom_webscrape import *

def __main__( ):
  # Open discord bot config file
  with open( 'config.json', 'r' ) as cfgIn:
    cfg = json.load( cfgIn );
    cfgIn.close( );

  intents = discord.Intents.default()
  intents.message_content = True
  #client = discord.Client( );
  bot = discord.Client(command_prefix=cfg["CMD_PREFIX"], description="spoogbot", intents=intents);
  @bot.event
  async def on_ready( ):
    print( "Bot Connected\n" );

  @bot.event
  async def on_message( message ):
    # Is DM
    if(  message.channel.type  == discord.ChannelType.private ): 
      await message.add_reaction( '💦' );
      return;

    #If message not sent by bot
    if( message.author != bot.user ):
      print(f"{message}"); 
      # Starts with CMD_PREFIX
      if( message.content.startswith( cfg["CMD_PREFIX"] ) ):
        print(f"Command Recieved: {message.content}")
        #Wordle Scoreboard command
        if( "scoreboard" in message.content.lower( ) ):        
          await wordleScoreboard( message );
        elif( "bingo_xp" in message.content.lower( ) ):        
          await womBingoParser( message, "commands/wom_config.json");

  bot.run( cfg['BOT_TOKEN'] );

__main__( );
