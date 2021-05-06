import discord
import os

client = discord.Client()

mod = None
modname = None
players = []
phase = -1
votes = []
users = [[],[],[],[],[]]
outcomes = []
confirmed = False
names = []


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    msg = message.content
    global mod
    global players
    global phase
    global users
    global outcomes
    global confirmed
    global names
    global modname
    
    if message.author == client.user:
        return

    if msg.startswith('mb>join '):
        if(phase != 0):
            await message.channel.send('Are you really dumb enough to think you could join right now?')
        else:
            if(message.author in players or message.author == mod):
                await message.channel.send('You\'re already in the game, you idiot!')
            elif(msg[8:] in names):
                await message.channel.send('No duplicate names. Stop trying to confuse me!')    
            else:
                names.append(msg[8:])
                await message.channel.send(msg[8:] + ' has joined the Town.')
                players.append(message.author)    
                
    if msg.startswith('mb>leave'):
        if(phase != 0):
            await message.channel.send('You can\'t leave the game right now. Stop trying to gamethrow!')
        else:
            if(message.author not in players and message.author != mod):
                await message.channel.send('You can\'t leave a game you haven\'t joined!') 
            else:
                if(message.author == mod):
                    mod = None
                    modname = None
                    await message.channel.send('The king has abdicated the throne!')  
                else:
                    num = players.index(message.author)
                    name = names[num]
                    players.pop(num)
                    names.pop(num)   
                    await message.channel.send(name + ' has left the Town. Probably a smart decision.')    
        
    if msg.startswith('mb>mod '):
        if(phase != 0):
            await message.channel.send('Are you really dumb enough to think you could mod right now?')
        else:
            if(mod == None):
                if(message.author in players):
                    await message.channel.send('You\'re already in the game, you idiot!')
                else:
                    modname = msg[7:]
                    mod = message.author
                    await message.channel.send(modname + ' is the king of the morons!')
            else:
                await message.channel.send('There\'s already a mod, you idiot!')
            
    if msg.startswith('mb>signups'):
        if(phase > 0 and mod != message.author):
            await message.channel.send('Do you really think you could restart the signups right now?')
        else:
            phase = 0
            players = []
            outcomes = []
            names = []
            modname = None
            mod = None
            confirmed = False
            await message.channel.send('Starting signups. Come on and join the Town of Morons!')
    
    if msg.startswith('mb>roles'):
        if(phase != 0 or mod != message.author):
            await message.channel.send('You can\'t start the game right now, moron!')
        elif(len(players) < 2 or mod == None):
            await message.channel.send('Don\'t you realize that you need actual players to play a game?')
        else:
            phase = 1
            plist = 'Players:'
            for i in names:
                plist += ' ' + i
            await message.channel.send(plist)
            await message.channel.send('Mod: ' + modname)
            await message.channel.send('You may now send your roles to the mod.')
            
    if msg.startswith('mb>start'):
        if(phase != 1 or mod != message.author):
            await message.channel.send('You can\'t start the game right now, moron!')
        else:
            for i in players:
                outcomes.append(0)
            phase = 2
            await message.channel.send("The game starts now. I'm too dumb to run the game, so let's let the mod take over.")
            if(mod in users[0]):
                users[1][users[0].index(mod)] += 1
            else:
                users[0].append(mod)
                users[1].append(1)
                users[2].append(0)
                users[3].append(0)
                users[4].append(0)
            
    if msg.startswith('mb>end'):
        if(phase != 2 or mod != message.author):
            await message.channel.send('You can\'t end the game right now, moron!')
        else:
            phase = 3
            await message.channel.send("The game is now over. The mod should record the results.")
    
    if msg.startswith('mb>givewin '):
        if(phase != 3 or mod != message.author):
            await message.channel.send('The game hasn\'t ended, it never existed, or you\'re not the mod. Either way, I don\'t want to know')
        else:
            found = False
            confirmed = False
            for i in range(len(names)):
                if(names[i] == msg[11:]):
                    found = True
                    outcomes[i] = 2
            if(found == False):
                await message.channel.send("That's not even a player!")
                
    if msg.startswith('mb>givedraw '):
        if(phase != 3 or mod != message.author):
            await message.channel.send('The game hasn\'t ended, it never existed, or you\'re not the mod. Either way, I don\'t want to know')
        else:
            found = False
            confirmed = False
            for i in range(len(names)):
                if(names[i] == msg[12:]):
                    found = True
                    outcomes[i] = 1
            if(found == False):
                await message.channel.send("That's not even a player!")
                
    if msg.startswith('mb>giveloss '):
        if(phase != 3 or mod != message.author):
            await message.channel.send('The game hasn\'t ended, it never existed, or you\'re not the mod. Either way, I don\'t want to know')
        else:
            found = False
            confirmed = False
            for i in range(len(names)):
                if(names[i] == msg[12:]):
                    found = True
                    outcomes[i] = 0
            if(found == False):
                await message.channel.send("That's not even a player!")      
                
    if msg.startswith('mb>confirm'):
        if(phase != 3 or mod != message.author):
            await message.channel.send('The game hasn\'t ended, it never existed, or you\'re not the mod. Either way, I don\'t want to know')
        else:
            confirmed = True
            await message.channel.send("If the following outcomes are correct, type mb>lock. Otherwise, fix the results.")  
            labels = ["loss", "draw", "win"]
            for i in range(len(players)):
                await message.channel.send(names[i] + ": " + labels[outcomes[i]])
                
    if msg.startswith('mb>lock'):
        if(confirmed == False or mod != message.author):
            await message.channel.send('You obviously can\'t lock the game results right now!')
        else:
            phase = -1
            nums = [4, 3, 2]
            for i in range(len(players)):
                if(players[i] in users[0]):
                    users[nums[outcomes[i]]][users[0].index(players[i])] += 1
                else:                
                    users[0].append(players[i])
                    users[1].append(0)
                    users[2].append(0)
                    users[3].append(0)
                    users[4].append(0)
                    users[nums[outcomes[i]]][len(users[0])-1] = 1
                    
    if msg.startswith('mb>stats'):
        if(message.author in users[0]):
            num = users[0].index(message.author)
            await message.channel.send('Games modded: ' + users[1][num])
            await message.channel.send('Wins: ' + users[2][num])
            await message.channel.send('Losses: ' + users[3][num])
            await message.channel.send('Draws: ' + users[4][num])
        else:
            await message.channel.send('You have\'t played any games yet. Play a game to become a true moron!') 
            
    if msg.startswith('mb>help'):
        await message.channel.send('mb>stats: view your winloss statistics')
        await message.channel.send('mb>signups: start signups for a new game')
        await message.channel.send('mb>join [name]: join a game')
        await message.channel.send('mb>mod [name]: mod a game')
        await message.channel.send('mb>leave: leave the game')
        await message.channel.send('mb>roles: start the roles phase')
        await message.channel.send('mb>start: start the game')
        await message.channel.send('mb>end: end the game')
        await message.channel.send('mb>givewin [nickname]: assign a win to a player')
        await message.channel.send('mb>giveloss [nickname]: assign a loss to a player')
        await message.channel.send('mb>givedraw [nickname]: assign a draw to a player')
        await message.channel.send('mb>confirm: confirm that you are done entering game results')
        await message.channel.send('mb>lock: confirm that game results are correct')
            
client.run('ODM5MzAwNzY4NDY4MzAzODg0.YJHpwA.Xlg2-WbYpgmNQJ3b6Bcvg-ZcAo8')
