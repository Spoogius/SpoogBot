import json
import requests

#https://stackoverflow.com/questions/4664850/how-to-find-all-occurrences-of-a-substring
def find_all(a_str, sub):
    rtn = list();
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return rtn
        rtn.append(start)
        start += len(sub) # use start += 1 to find overlapping matches
    

async def womBingoParser( message, config_file="commands/wom_config.json" ):
  with open(config_file, 'r') as cfg_fin:
    config = json.load(cfg_fin);

  print( config );

  r = requests.get(config['competition_homepage']);

  html_source = str(r.text);
  username_idx = find_all( html_source, "username")
  username_list = list();
  for idx in username_idx:
    username_source = html_source[idx+13:idx+13+32:1];
    username = username_source[0:username_source.find('\"')-1:1]
    username_list.append(username);

  u_usernames = set(username_list)
  print( u_usernames )

  # From Config
  #skill_list = ["Overall", "Woodcutting", "Fishing", "Mining", "Agility", "Slayer"]
  skill_list = config["skills"]

  user_totals = {};
  user_totals['total'] = {};
  # Init user totals
  for skill in skill_list:
    user_totals['total'][f"{skill}"] = int(0)

  for user in u_usernames:
    print(f"User: {user}")
    user_req = requests.get( f"{config['user_page_root']}{user}{config['user_page_tail']}")
    html_source_user = user_req.text;
    user_totals[f"{user}"] = {};
    for skill in skill_list:
      skill_idx = find_all( html_source_user, skill )
      idx = skill_idx[0]
      skill_source = html_source_user[idx:idx+256:1];
      val_start_idx = skill_source.find('<!-- -->') + 8;

      if( val_start_idx < 150 ): # Case Zero xp
        skill_val_str = "0";
      else: 
        skill_source = skill_source[val_start_idx::1]
        val_stop_idx = skill_source.find('</span>')
        skill_val_str = skill_source[0:val_stop_idx:1]

      skill_val_str = skill_val_str.replace(",", "")
      if( skill_val_str.find("k") != -1 ): 
        skill_val = float( skill_val_str[:-1:1]) * 1E3
      elif( skill_val_str.find("m") != -1 ):
        skill_val = float( skill_val_str[:-1:1]) * 1E6
      else: # Raw number
        skill_val = float( skill_val_str )
      #print( f"{skill}: {skill_val_str}")
      user_totals[f"{user}"][f"{skill}"] = int(skill_val)
      user_totals["total"][f"{skill}"] += int(skill_val) 
    print( f"Completed user: {user}")
    
  #print(user_totals)

  # Comput remaining
  user_totals['remaining'] = {};
  for tgt_idx in range(len(skill_list)):
    #print(f"{skill_list[tgt_idx]}: {user_totals['total'][skill_list[tgt_idx]]}/{config['target_xp'][tgt_idx]}", end = '')
    if( user_totals['total'][skill_list[tgt_idx]] > config['target_xp'][tgt_idx] ):
      #print(" Completed")
      user_totals['remaining'][skill_list[tgt_idx]] = int(0);
    else:
      #print( f" {config['target_xp'][tgt_idx] - user_totals['total'][skill_list[tgt_idx]]} Remaining")
       
      user_totals['remaining'][skill_list[tgt_idx]] = int( config['target_xp'][tgt_idx] - user_totals['total'][skill_list[tgt_idx]]);

  # Sort by 'Overall'
  u_usernames = list(u_usernames);
  xp_totals = [ user_totals[f"{user}"]['Overall'] for user in u_usernames ];
  sort_idx = sorted(range(len(xp_totals)), key=lambda k: xp_totals[k]) #https://stackoverflow.com/questions/7851077/how-to-return-index-of-a-sorted-list

  # Format discord String
  discord_string = f"```| {'Username':12} |";
  for skill in skill_list:
    skill_print_chars = max(len(skill),8);
    discord_string += f" {skill:{skill_print_chars}} |";
  discord_string += '\n';
  for user_idx in sort_idx:
    user = u_usernames[sort_idx[user_idx]]
    if( user == 'total' or user == 'remaining' ):
      continue

    discord_string += f"| {user:12} |";
    for skill in skill_list:
      skill_print_chars = max(len(skill),8);
      discord_string += f" {user_totals[user][skill]:{skill_print_chars}} |";
    discord_string += '\n';

  for user in ['total', 'remaining']:
    discord_string += f"| {user:12} |";
    for skill in skill_list:
      skill_print_chars = max(len(skill),8);
      discord_string += f" {user_totals[user][skill]:{skill_print_chars}} |"; 
    discord_string += '\n';
  discord_string += '```';
  print( discord_string )
  await message.channel.send( discord_string );
