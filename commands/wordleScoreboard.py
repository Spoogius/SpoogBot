import re
from functools import cmp_to_key;

async def wordleScoreboard( message ):

  if( not( "wordle" in message.channel.name ) ):
    return

  messages = await message.channel.history( limit=None ).flatten( );

  sbMap = { };
  userArr = list( );
  userIdx = 0;
  maxNameLength = 0;

  for m in messages:
    if( re.search( 'wordle [0-9]{3} [1-6]/6', m.content.lower() ) ): 
      slashIdx = m.content.find('/');
      user = str( m.author)
      user = user[ 0:user.find('#') ];
      if( user in sbMap.keys( ) ):
        sbMap[ user ][ 'sum' ] += int( m.content[ slashIdx - 1 ] );
        sbMap[ user ][ 'trys' ] += 1; 
      else:
        sbMap[ user ] = { 'idx' : userIdx, 'sum' : int( m.content[ slashIdx - 1 ] ), "trys" : 1, "avg": 0 };       
        userArr.append( user );
        maxNameLength = max( len( user ), maxNameLength );
        userIdx += 1;


  for key in sbMap.keys( ):
    sbMap[ key ][ 'avg' ] = sbMap[ key ][ 'sum' ]/sbMap[ key ][ 'trys' ];

  def customSort( a, b ):
    if( sbMap[ a ][ 'avg' ] > sbMap[ b ][ 'avg' ] ):
      return 1;
    elif( sbMap[ a ][ 'avg' ] < sbMap[ b ][ 'avg' ] ):
      return -1;
    else: 
      if( sbMap[ a ][ 'trys' ] > sbMap[ b ][ 'trys' ] ):
        return -1;
      elif( sbMap[ a ][ 'trys' ] < sbMap[ b ][ 'trys' ] ):
        return 1;
      else:
        return 0;

  userArr = sorted( userArr, key=cmp_to_key( customSort ) );  

  scoreboardStr = "User, Average Score, Num Wordles\n";
  for user in userArr:
    scoreboardStr += "{:<{}}, {:.2f}, {:3.0f}\n".format( user, maxNameLength, sbMap[ user ][ 'avg' ], sbMap[ user ][ 'trys' ] );  

  await message.channel.send( scoreboardStr );
