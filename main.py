import discord
from discord.ext import commands
import asyncio
import battleMetricsScraping
import playRustIO
import playerDatabase
import chunkedData
import readSetupFile
import watcherLogging

myBot = commands.Bot(command_prefix='>')


# these are the main setup found in the (the_watcher_config.ini) file
battlemetrics_url = ''
server_ip = ''
server_port = ''
bot_id = ''
bot_channel_player_joined = 0
bot_channel_commands = 0
bot_player_name_changes = 0
bot_enable_name_changes = False

loggedDictionCompare = dict()
myDiction = dict()
myLocalDic = dict()
myDictionOLD = dict()

isReady = False


def setReady():
    global isReady
    isReady = True


@myBot.event
async def on_ready():
    setReady()
    print('TheWatcher Bot is ready')


def read_config_file_now():

    global battlemetrics_url
    global server_ip
    global server_port
    global bot_id
    global bot_channel_player_joined
    global bot_channel_commands
    global bot_player_name_changes
    global bot_enable_name_changes

    # read the config file and assign the values
    setupDic = readSetupFile.read_cofig()

    for key in setupDic:
        if key == 'battlemetrics_url':
            battlemetrics_url = setupDic[key]
        elif key == 'server_ip':
            server_ip = setupDic[key]
        elif key == 'server_port':
            server_port = setupDic[key]
        elif key == 'bot_id':
            bot_id = setupDic[key]
        elif key == 'bot_channel_player_joined':
            bot_channel_player_joined = setupDic[key]
        elif key == 'bot_channel_commands':
            bot_channel_commands = setupDic[key]
        elif key == 'bot_player_name_changes':
            bot_player_name_changes = setupDic[key]
        elif key == 'bot_enable_name_changes':
            bot_enable_name_changes = setupDic[key]


# updates player joined logged every 5 mins if data is there
# updates player name changes every 30 mins if data is there
# @myBot.command()
async def update_players():
    await myBot.wait_until_ready()

    global battlemetrics_url
    global server_ip
    global server_port
    global bot_channel_player_joined

    print('Started....')
    thirtyMinCounter = 0
    # create the table if its not been created on launch
    playerDatabase.create_player_table()
    loggedDictionCompare = {}
    myDiction = {}

    while not myBot.is_closed():
        print('===========')
        try:
            if isReady:

                # myDiction = {}
                myDiction = battleMetricsScraping.get_Data_Now(
                    battlemetrics_url)
                global myLocalDic
                global myDictionOLD
                myLocalDic = myDiction

                # GET ALL CURRENT PLAYERS
                print('running all players call')
                myAllList = battleMetricsScraping.get_all_current_players(
                    myDiction)
                # for p in myAllList:
                # print(p)
                if len(myAllList) > 0:
                    print('running all players parse')
                    myChunkedList1 = chunkedData.get_chunked_data(
                        myAllList)
                    for allP in myChunkedList1:
                        print(allP)
                        # give the chunked data to the bot to send to the channel

                # GET JUST JOINED PLAYERS
                print('running player joined call')
                myPList = battleMetricsScraping.get_just_joined_players(
                    myDiction, myDictionOLD)

                if len(myPList) > 3:
                    print('running player joined bot parse')
                    myChunkedList2 = chunkedData.get_chunked_data(
                        myPList)
                    for pJoin in myChunkedList2:
                        # give the chunked list to the bot to send to the channel
                        print(pJoin)

                        # send to player-joined-logged channel with the channel id
                        channel = myBot.get_channel(
                            bot_channel_player_joined)
                        await channel.send(pJoin + '\n')
                    # last list of updated players if it contains the same players dont resend a minute later
                    myDictionOLD = myDiction
                else:
                    myDictionOLD = {}

                # GET PLAYERS LOGGED OFF
                print('running player logged call')
                if len(loggedDictionCompare) > 0:
                    myLoggedOutList = battleMetricsScraping.get_logged_off_players(
                        loggedDictionCompare, myDiction)
                    print(f"Player logged off debug ::{len(myLoggedOutList)}")
                    if len(myLoggedOutList) > 3:
                        print('running player logged parse')
                        # for item in myLoggedOutList:
                        # print(item)
                        myChunkedList3 = chunkedData.get_chunked_data(
                            myLoggedOutList)
                        # give the chunked list to the bot to send to the channel
                        for pLogged in myChunkedList3:
                            print(pLogged)
                            # send to player-joined-logged channel
                            channel = myBot.get_channel(
                                bot_channel_player_joined)
                            await channel.send(pLogged + '\n')

                # GET PLAYER NAME CHANGES
                if(thirtyMinCounter >= 30 and bot_enable_name_changes == True):
                    print('running player name changes not setup yet')
                    pNameChangeList = []
                    pNameChangeList = playRustIO.check_for_player_name_changes(
                        server_ip, server_port)
                    myChunkedList4 = chunkedData.get_chunked_data(
                        pNameChangeList)
                    # give to the discord bot to send to the channel
                    for pName in myChunkedList4:
                        print(pName)
                        # send to player-name-changes channel
                        channel = myBot.get_channel(bot_player_name_changes)
                        await channel.send(pName + '\n')

                    thirtyMinCounter = 0
                else:
                    thirtyMinCounter = 0

            thirtyMinCounter += 1
            loggedDictionCompare = myDiction
            # myLocalDic = myDiction
            print("Thirty Minute Counter Value :{}".format(thirtyMinCounter))
            print('Sleeping for 1 min')
            # sleep for 5 mins
            # await asyncio.sleep(30)
            # #send to player-joined-logged channel
            # channel = myBot.get_channel(1234567890)
            # await channel.send('This ia Test')
            # print('Msg sent')
        except Exception as e:
            print("Rust Bot Loop ERROR::" + str(e))
            watcherLogging.error_logs(
                "Rust Bot Loop ERROR::" + str(e))
            await asyncio.sleep(10)

        await asyncio.sleep(60)


@myBot.event
async def on_message(message):
    # id = client.get_guild(1234567890)
    # myLocalDic = myDiction
    # channels = ["the-watcher-commands"]
    global bot_channel_commands
    myAllList = []
    # cmdChannel = myBot.get_channel(1234567890)
    cmdChannel = myBot.get_channel(bot_channel_commands)
    if message.author == myBot.user:
        return
    # if str(message.channel) in channels:
    if message.channel.id == cmdChannel.id:
        myMessage = message.content.lower()
        if myMessage.startswith('>players'):
            print("Received players cmd")
            try:
                if myLocalDic is not None and len(myLocalDic) > 0:
                    # myDiction = battleMetricsScraping.get_Data_Now(mainUrl)
                    myAllList = battleMetricsScraping.get_all_current_players(
                        myLocalDic)
                    # for p in myAllList:
                    # print(p)
                    if len(myAllList) > 0:
                        print('running all players parse')
                        myChunkedList1 = chunkedData.get_chunked_data(
                            myAllList)
                        for allP in myChunkedList1:
                            print(allP)
                            await message.channel.send(allP)
                            # give the chunked data to the bot to send to the channel
                            # await message.channel.send("implement count players here")
                    else:
                        print('No player data Yet...')
                        await message.channel.send("No player data Yet...")
                        # await message.channel.send('No player data Yet...')
                else:
                    print('Bot not ready Yet...')
                    await message.channel.send("Bot not ready Yet...")
            except Exception as e:
                print('An error occured in on_message Discord Bot ::' + str(e))
                watcherLogging.error_logs(
                    'An error occured in on_message Discord Bot ::' + str(e))

        elif myMessage.startswith(">pinfo"):
            print("Received pinfo cmd")
            try:
                pInfoList = playerDatabase.get_DB_linked_player_Embed_List()
                for itmEmbed in pInfoList:
                    await message.channel.send(embed=itmEmbed)
            except Exception as e:
                print('An error occured in on_message Discord Bot ::' + str(e))
                watcherLogging.error_logs(
                    'An error occured in on_message Discord Bot ::' + str(e))

        elif myMessage.startswith(">help"):
            helpMsg = ">players :: All Online players \n"\
                ">pinfo :: All players saved from database \n"\
                ">help :: This help menu"
            await message.channel.send(helpMsg)

    # else:
        # await message.channel.send('Wrong command channel Noob XD')

# #read the config file and assign the values
# setupDic = readSetupFile.read_cofig()

# for key in setupDic:
#     if key == 'battlemetrics_url':
#         battlemetrics_url = setupDic[key]
#     elif key == 'server_ip':
#         server_ip = setupDic[key]
#     elif key == 'server_port':
#         server_port = setupDic[key]
#     elif key == 'bot_id':
#         bot_id  = setupDic[key]
#     elif key == 'bot_channel_player_joined':
#         bot_channel_player_joined  = setupDic[key]
#     elif key == 'bot_channel_commands':
#         bot_channel_commands  = setupDic[key]
#     elif key == 'bot_player_name_changes':
#         bot_player_name_changes  = setupDic[key]
#     elif key == 'bot_enable_name_changes':
#         bot_enable_name_changes = setupDic[key]


read_config_file_now()


myBot.loop.create_task(update_players())

# your bot key
myBot.run(bot_id)
