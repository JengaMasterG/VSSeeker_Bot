import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from discord import Client
import json
from utils.dataIO import dataIO
import os
from copy import deepcopy
import random
from datetime import datetime

bot = commands.Bot(command_prefix = "!")

print ("Discord Version " + discord.__version__)
bot_version = "0.1.9"
print ("Bot Version " + bot_version)


#global variables used for all commands
file_path_trainer = "data/player/players.json"
file_path_tournament = "data/tournament/tournaments.json"

#global variables used for event
emoji_check = '✔'
emoji_x = '❌'
react_challengee = None
react_challenger = None
react_mode = ""
counter = 1

#JSON File Methods
def check_trainer_directory():
    if not os.path.exists('data/player'):
        print("Player directory doesn't exist...creating directory")
        os.makedirs("data/player")

    elif os.path.exists("data/player"):
        print("Directory Exists...checking for log")
    
    else:
        print("Could not create directory!")

def check_tournament_directory():
    if not os.path.exists('data/tournament'):
        print("Tournament directory doesn't exist...creating directory")
        os.makedirs("data/tournament")

    elif os.path.exists("data/tournament"):
        print("Directory Exists...checking for log")
    
    else:
        print("Could not create directory!")
    

def check_trainer_log():
    system = server_default_trainer

    file = 'data/player/players.json'
    if not dataIO.is_valid_json(file):
        print("Log not found...creating log")
        with open(file, 'w') as f:
            json.dump(system, f, sort_keys= True)

    elif dataIO.is_valid_json(file):
        print("Log found!")

    else:
        print("Could not create log, but directory exists.")

def check_tournament_log():
    system = server_default_tournament

    file = 'data/tournament/tournaments.json'
    if not dataIO.is_valid_json(file):
        print("Log not found...creating log")
        with open(file, 'w') as f:
            json.dump(system, f, sort_keys= True)

    elif dataIO.is_valid_json(file):
        print("Log found!")

    else:
        print("Could not create log, but directory exists.")

def load_file(path):
    file = dataIO.load_json(path)
    return file

def update_data(path, file):
    dataIO.save_json(path, file)


#Boot Checks for Bot
@bot.event
async def on_ready():
    online = "VS. Seeker Online"
    print("Will operate as " + bot.user.name)
    print("With the ID of: " + bot.user.id)

    print("Checking for Trainer Log...")
    check_trainer_directory()
    check_trainer_log()
    print("Checking for Tournament Log...")
    check_tournament_directory()
    check_tournament_log()

    print(online)




def challenge_add(challenger, challengee):
#access number of times the challenger and challengee has been challenged
    trainer_data = load_file(file_path_trainer)
    
    chllgr = trainer_data["Trainers"][challenger]
    chllgee = trainer_data["Trainers"][challengee]
#add 1 to num of times challenged
    num_challenger = chllgr["Times Challenged"] +1
    num_challengee = chllgee["Times Challenged"] +1

#update number of times challenged for challenger and challengee
    chllgr["Times Challenged"] = num_challenger
    chllgee["Times Challenged"] = num_challengee
    update_data(file_path_trainer, trainer_data)

def reset_challengee(challengee):
    #resets the global variable react_challengee for the challenge cmd.
    global react_challengee
    challengee = None
    react_challengee = challengee

def reset_challenger(challenger):
    #resets the global variable react_challenger for the challenge cmd.
    global react_challenger
    challenger = None
    react_challenger = challenger

@bot.command(pass_context=True)
async def hi(ctx):
    await bot.say("hello!")

@bot.command(pass_context=True)
async def version(ctx):
    await bot.say("Current bot version: " + bot_version)

@bot.command(pass_context=True)
async def challenge(ctx, user: discord.Member = None, mode = None):
    #Challenge a player: !challenge vs (or domination) @playername .
    cancel_challenge = False

    challenger = ctx.message.author
    challengee = user

    if user is None: await bot.say("To use this command, please mention a challenge type (vs or domination) and a user (@playername)")
    elif mode is None: await bot.say("Please type a challenge in after the player's name!")
    else:
        if mode in ['vs', 'VS', "v.s.", "V.S.", "v.s", "V.S", "Vs", "versus", "Versus"]: mode = "Versus"
        elif mode in ['domination', 'dom', 'Dom' 'Domination']: mode = "Domination"
        else: cancel_challenge = True
        
        if cancel_challenge is True: await bot.say("I'm sorry, but that is not a recognized game mode. Here are the current game modes: \nVersus, Domination")            
        elif cancel_challenge is False:
            embed = discord.Embed(title = "Challenge Issued!", description = "A challenger approaches!", color = 0xffff00)
            embed.add_field(name = "Challenger", value = challenger.mention, inline = True)
            embed.add_field(name = "Challengee", value = challengee.mention, inline = True)
            embed.add_field(name = "Challenge Type", value = mode, inline = True)
            embed.add_field(name = "Accept or Deny", value = "Please accept or deny the challenge")
            react_message = await bot.say(embed=embed)
            global react_challengee
            react_challengee = challengee #"{}".format(challengee) #sends challengee to global variable
            print(react_challengee) #shows challengee's userID on console
            global react_challenger
            react_challenger = challenger #"{}".format(challenger) #sends challenger to global variable
            global react_mode
            react_mode = "{}".format(mode) #sends mode to global variable
            await bot.add_reaction(react_message, emoji_check)
            await bot.add_reaction(react_message, emoji_x)
    
    

@bot.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    global counter
    count = counter

    user = user
    print("{}".format(user)) #shows which userID is the current user reacting
        
    reaction = "{}".format(reaction.emoji)
    print(reaction) #used to see if reaction is recorded.
        
    global react_challengee
    #check to see if the challengee was sent to global variable
        
    global react_challenger
    #check to see if the challenger was sent to global variable

    global react_mode
    #check to see if the mode was sent to the global variable
    print("{} should be same as {}".format(user, react_challengee))

    #print(react_challengee) #shows challengee's userID on console
    challengee = react_challengee #sets the challengee's userID to a new variable
    print("{} is the challengee".format(challengee)) #verifies the user's userID on console (the curernt one who reacted)

    #print(react_challenger) #shows challenger's userID on console
    challenger = react_challenger #sets the challenger's userID to a new variable
    print("{} is the challenger".format(challenger)) #verifies the user's userID on console (the curernt one who reacted)

    #print(react_mode) #shows mode on console
    mode = react_mode #sets the mode to a new variable
    print(mode + " Game Mode") #verifies the mode on console

    print (count)

    if user == challengee and reaction == emoji_check or reaction == emoji_x: #if the user is the challengee
        bot_message = False #this stops the bot and any other players from accepting the challenge
    #elif user == bot:
    #    bot_message = True  #the bot message will appear
    elif user is not challengee and reaction == emoji_check or reaction == emoji_x: #if the challengee is not the user (another player or bot)
        bot_message = False #this stops the bot and any other players from accepting the challenge
    

    if bot_message is True and count == 1: 
        count = count +1
        #await bot.send_message(channel, "Please accept or deny the challenge") 
        counter = count
        print ("the counter has increased to {}".format(counter))

    elif bot_message is True and count > 1:
        count = count +1
        counter = count
        print ("the counter has increased to {}".format(counter))

    if user == challengee and reaction == emoji_x:
        embed = discord.Embed(title = "Challenge Denied!", description = "Try again another time!", color = 0xff0000)
        embed.add_field(name = "Challenger", value = challenger, inline = True)
        embed.add_field(name = "Challengee", value = challengee, inline = True)
        embed.add_field(name = "Challenge Type", value = mode, inline = True)
        await bot.send_message(channel, embed=embed)
        count = 1
        counter = count
        print("Challenge denied. Counter reset to {}".format(counter))
        reset_challengee(challengee)
        reset_challenger(challenger)
           
    elif user == challengee and reaction == emoji_check: 
        embed = discord.Embed(title = "Challenge Accepted!", description = "Prepare to Battle!", color = 0x00cc00)
        embed.add_field(name = "Challenger", value = challenger, inline = True)
        embed.add_field(name = "Challengee", value = challengee, inline = True)
        embed.add_field(name = "Challenge Type", value = mode, inline = True)
        await bot.send_message(channel, embed=embed)
        challenge_add(challenger.id, challengee.id)
        count = 1
        counter = count
        print("Challenge accepted. Counter reset to {}".format(counter))
        reset_challengee(challengee)
        reset_challenger(challenger)


#TRAINER JSON PARAMETERS
# -------------------------------------------------------------------------------------------------

# Default settings that is created when a server begin's using Player List
server_default_trainer = {
    #"Server":{             Add-in if the .json file will be used for multiple servers
    "Trainers": {}
    #}for Server
    }
#---------------------------------------------------------------------------------------------------

#Default settings for a new trainer.
trainer_new = {
    "ID": "",
    "Title": "Trainer",
    "Times Challenged" : 0,
    "Wins": 0,
}
#---------------------------------------------------------------------------------------------------

#----------------TRAINER LIST COMMANDS--------------------------------------
   
def new_trainer(user):
    #server = user.server              for self.check_server_settings
    path = file_path_trainer             #multi-server replacement: path = self.check_server_settings(server)
    file = load_file(path)
    
    if user.id not in file["Trainers"]: #multi-server replacement: if user.id not in file["Servers"]["Trainers"]
        input_trainer = deepcopy(trainer_new)
        
        open(path, 'a')
        
        file["Trainers"]["{}".format(user.id)] = input_trainer #multi-server replacement: file["Servers"]["Trainers"][user.id] = input_trainer
        file["Trainers"][user.id]["ID"] = user.name #multi-server replacement: file ["Servers"]["Trainers"][user.id]["ID"] = user.name
        
        update_data(path, file)
        return file
            
def remove_trainer(user):
    #server = user.server
    path = file_path_trainer
    file = load_file(path)
    
    if user.id in file["Trainers"]:
        open(path, 'w')

        del file["Trainers"][user.id]
        
        update_data(path, file)
        return file

def change_title(user, new_title):
    path = file_path_trainer
    file = load_file(path)
    
    file["Trainers"][user.id]["Title"] = new_title
    update_data(path, file)
    
#Deploy if bot will be used on other servers to help organize .json file

#def check_server_settings(self, server):
#    log = self.trainer_data
#    if server.id not in log["Servers"]:
#        self.trainer_data["Servers"][server.id] = server_default_trainer
#        self.update_data()
#        print(_("Creating default trainer list settings for Server: {}").format(server.name))
#        path = self.trainer_data["Servers"][server.id]
#        return path
#
#    else:
#        path = self.trainer_data["Servers"][server.id]
#        return path
    
@bot.group(pass_context=True)
async def create_log(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say("That doesn't seem to be a valid command at this time.")
    
@create_log.command(pass_context = True)
async def trainer():   
   """Used to create and check for your trainer data!"""
   #check if the path to the file exists
   if not os.path.exists("data/player"):
       await bot.say("data/player folder does not exist!")
       await bot.say("Creating data/player folder...")
       os.makedirs("data/player")
   else:
       await bot.say("Folder location exists...")
       await bot.say("Searching for Trainer Log...")

   system = server_default_trainer

   #check if the file exists

   f = file_path_trainer
   if not dataIO.is_valid_json(f):
       await bot.say("Creating Trainer Log...")
       open(f, 'w')
       dataIO.save_json(f, system)
   if dataIO.is_valid_json(f):
       await bot.say("Trainer Log created!")
   else:
       await bot.say("Could not create Trainer Log!")

@create_log.command(pass_context=True)
async def tournaments():   
    """Used to create and check for your tournament data!"""
    #check if the path to the file exists
    if not os.path.exists("data/tournament"):
        await bot.say("data/tournament folder does not exist!")
        await bot.say("Creating data/tournament folder...")
        os.makedirs("data/tournament")
    else:
        await bot.say("Folder location exists...")
        await bot.say("Searching for Trainer Log...")

    system = server_default_tournament

    #check if the file exists

    f = file_path_tournament
    if not dataIO.is_valid_json(f):
        await bot.say("Creating Tournament Log...")
        open(f, 'w')
        dataIO.save_json(f, system)
    if dataIO.is_valid_json(f):
        await bot.say("Tournament Log created!")
    else:
        await bot.say("Could not create Tournament Log!")
        
@bot.command(pass_context=True)
async def trainer_add(ctx, user: discord.User):
    """Adds a new trainer to the log"""

    trainer = "{}".format(user.id)  
    #await bot.say(trainer) tester to see if user ID -> string for trainer variable
    path = file_path_trainer
    file = load_file(path)

    if trainer not in file["Trainers"]:
        new_trainer(user)
        trainer_data = load_file(file_path_trainer)
        trainer_id = file["Trainers"][trainer]["ID"]
        dataIO.save_json(file_path_trainer, trainer_data)
        await bot.say(user.mention + " has been added as " + trainer_id)
    
    else: await bot.say("This user has already been added.")

@bot.command(pass_context = True)
async def trainer_rm(ctx, user: discord.User):
    """Removes a trainer from the log"""
    
    trainer_data = load_file(file_path_trainer)
    trainer = user.id   
    #await bot.say(trainer) tester to see if user ID -> string for trainer variable
    if trainer not in trainer_data["Trainers"]:
        await bot.say("This trainer is not registered or has already been removed.")
    
    else:
        remove_trainer(user)
        await bot.say(user.mention + " has been removed.")
    
@bot.command(pass_context=True)
async def trainer_stats(ctx, user: discord.User):
    """Checks the Stats of a Trainer"""
    trainer_data = load_file(file_path_trainer)
    user_id = "{}".format(user.id)
    file = trainer_data["Trainers"][user_id]
    trainer = file["ID"]
    title = file["Title"]
    challenges = str(file["Times Challenged"])
    wins = str(file["Wins"])
    await bot.say("Trainer ID: " + trainer + "\nTitle: " + title + "\nTimes Challenged: " + challenges +" \nWins: " + wins)
    
@bot.command(pass_context=True)
async def trainer_won(ctx, user: discord.User):
    """Adds a Win to the player's log"""
    
    trainer_data = load_file(file_path_trainer)
    user_id = "{}".format(user.id)
    
    file = trainer_data["Trainers"][user_id]
    wins = file["Wins"] +1
    file["Wins"] = wins
    update_data(file_path_trainer, trainer_data)
    
    await bot.say(user.mention + "'s victory has been added to the trainer log.")

@bot.command(pass_context=True)
async def set_title(ctx, title = "", user: discord.Member = None ):
    """Changes the Title for a player"""
    
    trainer_data = load_file(file_path_trainer)
    
    if user is None:
        user = ctx.message.author
        
        if user.id not in trainer_data["Trainers"]:
            await bot.say("You're currently not in the trainer log. You can run `!trainer_add @username` to add yourself!")
        
        else:
            print("{} requested a title change".format(user))
            
            new_title = title
            change_title(user, new_title)
            await bot.say("Your Title has been changed to: " + new_title)
        

    else:
        if user.id not in trainer_data["Trainers"]:
            await bot.say("I'm sorry, but that user currenlty isn't listed as a Trainer. You can add them by running `!trainer_add @username` first!")
        
        else:
            print("{} requested a title change for {}".format(ctx.message.author, user))
            new_title = title
            change_title(user, new_title)
            await bot.say(user.mention + "'s title has been changed to: " + new_title)


#TOURNAMENT JSON PARAMETERS
# ------------------------------------------------------------------------------------

# Default settings that is created when a server begin's using Player List
server_default_tournament = {
    #"Server":{             Add-in if the .json file will be used for multiple servers
    "Tournaments": {}
    #}for Server
    }
#---------------------------------------------------------------------------------------------------

#Default settings for a new tournament.
tournament_new = {
    "Access Code": "",
    "Title": "",
    "Tournament Type" : "",
    "Host": "",
    "Signup": "",
}
#---------------------------------------------------------------------------------------------------

#----------------TOURNAMENT LIST COMMANDS--------------------------------------
#SERVICES SUPPORTED:
#   Silph Arena

#------------------------------------------------------------------------------

def new_tournament(file, path, tournament_type, tournament_signup, host, access_code):
    #server = user.server              for self.check_server_settings
    #path = file_path_tournament             #multi-server replacement: path = self.check_server_settings(server)
    ID = access_code

    if ID not in file["Tournaments"]: #multi-server replacement: if user.id not in file["Servers"]["Tournaments"]
        input_tournament = deepcopy(tournament_new)
        
        open(path, 'a')
        
        file["Tournaments"]["{}".format(ID)] = input_tournament #multi-server replacement: file["Servers"]["Tournaments"][ID] = input_tournament
        file["Tournaments"]["{}".format(ID)]["Tournament Type"] = tournament_type
        file["Tournaments"]["{}".format(ID)]["Signup"] = tournament_signup
        file["Tournaments"]["{}".format(ID)]["Host"] = host
        file["Tournaments"]["{}".format(ID)]["Access Code"] = ID

        update_data(path, file)
        
    return file
            
def remove_tournament(ID):
    #server = user.server
    path = file_path_tournament
    file = load_file(path)
    
    if ID in file["Tournaments"]:
        open(path, 'w')

        del file["Tournaments"][ID]
        
        update_data(path, file)
        return file

#def change_title(user, new_title):
#    path = file_path_tournament
#    file = load_file(path)
#    
#    file["Trainers"][user.id]["Title"] = new_title
#    update_data(path, file)

def create_access_code(create_ID):
    random.seed(datetime.now())
    
    code = random.randint(1000, 9999)

    create_ID = code
    return create_ID

@bot.group(pass_context = True)
async def tournament(ctx):
   if ctx.invoked_subcommand is None:
       await bot.say("That doesn't seem to be a valid command at this time.")

#@tournament.command(pass_context = True)
#async def list(ctx):
#    """Lists the current tournaments taking place"""

@tournament.command(pass_context = True)
async def create(ctx, tournament_type = None, tournament_signup = None, host: discord.Member = None, access_code = ""):
    #value corrections
    if tournament_type in ['swiss', 'Swiss', 'swis', 'Swis', 'sw', 'Sw', 'swi', 'Swi']: tournament_type = "Swiss"
    
    else:
        if tournament_type is None:
            await bot.say("The tournament type wasn't specified, so the tournament could not be created!")

    if tournament_signup in ['silph', 'Silph', 's', 'S', 'sil', 'Sil', 'silp', 'silph']: 
        tournament_signup = "The Silph Arena"
        service_support = True
    
    else:
        service_support = False
        
        if tournament_signup is None:
            await bot.say("The tournament signup location wasn't specified, so the tournament could not be created!")
    
    if host is None:
        await bot.say("The tournament host wasn't specified, so the tournament could not be created!")
    
    else:
        #creates ID for tournament if access_code is none
        if access_code is None:
            create_ID = 0
            ID = "{}".format(create_access_code(create_ID))
            await bot.say("Creating tournament...")
            await bot.say("This is your access code to manage the tournament here: \n {}".format(ID))
            await bot.say("If you were given an access code by the sign up provider, please use ```tournament set_access_code [Current ID] [new access code]``` to update it.")
        
        else:
            ID = access_code
            await bot.say("Creating tournament...")

        #ID check for existing tournament
        path = file_path_tournament
        file = load_file(path)
        
        if ID not in file["Tournaments"]:
            new_tournament(file, path, tournament_type, tournament_signup, host.name, ID)
            
            #prints the ID to the console
            print(file["Tournaments"][ID])
            
            #prints the tournament details to discord
            #Adds website link to the Signup location if it is The Silph Arena
            if service_support is False:
                tournament_created = discord.Embed(title = "A Tournament Has Been Created!", color = 0x00cc00)
                tournament_created.add_field(name = "Tournament Type", value = file["Tournaments"]["{}".format(ID)]["Tournament Type"], inline = True)
                tournament_created.add_field(name = "Tournament Host", value = file["Tournaments"][ID]["Host"], inline = True)
                tournament_created.add_field(name = "Where to Signup", value = file["Tournaments"][ID]["Signup"], inline = False)
                tournament_created.add_field(name = "Access Code", value = file["Tournaments"][ID]["Access Code"])
                await bot.say(embed=tournament_created)
                await bot.say("Please use your Access Code to manage this tournament.")
                
            else:
                tournament_created = discord.Embed(title = "A Tournament Has Been Created!", color = 0x00cc00)
                tournament_created.add_field(name = "Tournament Type", value = tournament_type, inline = True)
                tournament_created.add_field(name = "Tournament Host", value = host, inline = True)
                tournament_created.add_field(name = "Where to Signup", value = "[{}](https://silph.gg/tournaments/join)".format(tournament_signup), inline = False)
                tournament_created.add_field(name = "Access Code", value = file["Tournaments"][ID]["Access Code"])
                await bot.say(embed=tournament_created)
                
        else:
            await bot.say("It appears that there is already an active tournament with that ID. \nYou can run ```!tournament update``` to update the existing tournament.")

@tournament.command(pass_context=True)
async def clear(ctx, access_code = None):
    """Clears a tournament from the log"""

    ID = access_code
    path = file_path_tournament
    file = load_file(path)

    if ID is None:
        await bot.say("To clear a tournament, please input an access code.")
    
    elif len(ID) < 4:
        await bot.say("This ID doesn't have enough digits. Please input a 4-digit access code.")
    
    elif len(ID) > 4:
        await bot.say("This ID has too many digits. Please input a 4-digit access code.")
    
    else:
        ID = access_code
        if ID in file["Tournaments"]:
            remove_tournament(ID)
            await bot.say("The tournament has been cleared from the log.")

        else:
            await bot.say("It appears that ID is not registered in the tournament log.")          
            
        
@tournament.command(pass_context = True)
async def set_access_code(ctx, access_code_old = "", access_code = ""):
    """Updates the ID and Access Code for a tournament"""
    
    path = file_path_tournament
    file = load_file(path)

    old_ID = access_code_old
    new_ID = access_code
    
    update_access_code(path, file, new_ID, old_ID)


    if len(new_ID) < 4:
        await bot.say("The access code doesn't have enough digits. Please use a 4-digit access code.")

    elif len(new_ID) > 4:
        await bot.say("The access code has too many digits. Please use a 4-digit access code.")

    else:
        print(old_ID)
        if old_ID in file["Tournaments"]:
            file["Tournaments"][old_ID]["Access Code"] = new_ID
            file["Tournaments"][new_ID] = file["Tournaments"][old_ID]
            update_data(path, file)
            remove_tournament(old_ID)
            await bot.say("Access Code changed. Please use your new access code, **" + new_ID + "**, to manage this tournament")
            

        elif new_ID in file["Tournaments"]:
            await bot.say("It appears that ID has already been registered in the tournament log.")        
        
        else:
            await bot.say("It appears that ID isn't registered in the tournament log.")


bot.run("NDA5Njk5MDg4MzA5OTQ0MzIx.DhLRxg.6CtuxRl1SZ-tgmwkJCOCc0IkQr4")