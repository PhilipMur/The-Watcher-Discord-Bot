import requests
import json
import playerDatabase
import watcherLogging

# This will be set in the config file so dont worry about it :-)
mainIpandPort = "192.168.1.1:28015"

# get all recent players with hyper links


def get_all_recent_player_info(serverIP, ServerPort):
    global mainIpandPort

    try:
        resp = requests.get("http://" + serverIP + ':' +
                            ServerPort + "/recent.json", allow_redirects=True)
        print("check for all player recent info Address" + str(mainIpandPort))
        myList = []
        playerCount = 0

        # print(resp.content)

        players = json.loads(resp.content)

        for p in players:
            myList.append('player=(' + p['name'] + ') id=(' + p['id'] + ')\n')
            playerCount += 1
        myList.append("Total recent players::{}" .format(playerCount) + '\n')

    except Exception as e:
        print("Error has occured in PlayRust.io request get_all_recent_player_info ::" + str(e))
        watcherLogging.error_logs(
            'Error has occured in PlayRust.io request get_all_recent_player_info ::' + str(e))

    return myList

# check thise dictinary against values stored in the database and returns a dictionary of name changes if any
# key = playerID and Value = player name


def check_for_player_name_changes(serverIP, ServerPort):
    global mainIpandPort
    playerDbList = []
    myReturnList = []
    try:
        resp = requests.get("http://" + serverIP + ':' +
                            ServerPort + "/recent.json", allow_redirects=True)
        print("check for player name changes Address" + str(mainIpandPort))
        #myDic = {}

        # print(resp.content)

        players = json.loads(resp.content)

        for p in players:
            playerDbList = playerDatabase.check_for_existing_player(p['id'])
            if len(playerDbList) > 0:
                for pData in playerDbList:
                    if pData[2] != p['name']:
                        # check if the name has changed
                        playerDatabase.update_player_name(p['id'], p['name'])
                        myReturnList.append(
                            "Player ::" + pData[1] + " Now Playing as ::" + p['name'] + '\n')
                        print("player changed name")
            else:
                # add new player to the database
                playerDatabase.add_player_data(p['id'], p['name'], p['name'])
                print("Added new player :: Id:" +
                      p['id'] + " Name:" + p['name'])

            # add or check player in the database

    except Exception as e:
        print("Error has occured in PlayRust.io request check_for_player_name_changes ::" + str(e))
        watcherLogging.error_logs(
            'Error has occured in PlayRust.io request check_for_player_name_changes ::' + str(e))

    return myReturnList
