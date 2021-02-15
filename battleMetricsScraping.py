import requests
from datetime import datetime
from bs4 import BeautifulSoup
from csv import writer
import watcherLogging
import sys

# server URL in Battlemetrics
# This is set in the config file at startup so dont worry about it :-)
mainUrl = "https://www.battlemetrics.com/servers/rust/123456"


def get_Data_Now(myUrl):

    myDic = {}

    mainUrl = myUrl

    # isGoodRequest = False

    # # Windows 10 with Google Chrome
    # user_agent_Windows = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '\
    #     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 '\
    #     'Safari/537.36'

    # # Windows 10 with Firefox Full headers
    # user_agent_Windows = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'

    # Windows 10 with Firefox
    user_agent_Windows = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
                          'Accept': 'text/html; charset=utf-8',
                          'Accept-Language': 'en-US,en;q=0.5'}

    session = requests.session()
    session.headers.update(user_agent_Windows)

    # non ascii charcters converter, normally used for IDLE
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

    try:

        response = session.get(mainUrl, allow_redirects=True,
                               timeout=(2, 5))  # Send request (tuple #1 = get request timeout #2 = read timeout)

        if response.history:
            print("Request was redirected")
            for resp in response.history:
                print(resp.status_code, resp.url)
                print("Final destination:")
                print(response.status_code, response.url)
        else:
            print("Request was not redirected")

        code = response.status_code  # HTTP response code

        if code == 200:
            print(f'Good Request From Battlemetrics: {code}')
            # isGoodRequest = True
        else:
            # isGoodRequest = False
            print(f'Error to load Battlemetrics: {code}')
            watcherLogging.error_logs(f'Error to load Battlemetrics: {code}')
            return myDic

        serverName = ''

        soup = BeautifulSoup(response.text, 'html.parser')

        # this spits out raw html as a string
        # print('PrintOut =' + str(soup.encode("utf-8")))

        myDic = {}

        if soup is None:
            return

        # findServerName = soup.find(id='serverPage').get_text()
        div = soup.find('div', id="main")
        if div is not None:
            # table = div.find_all('h2')
            # print('Found =' + div[0])
            print('List Count =' + str(len(div)))
        else:
            print('Not Found')
            return

        # temp = soup.get_text()
        temp = soup.find("h2").find_all(text=True, recursive=False)
        if temp != None and len(temp) >= 1:
            serverName = temp[0]
            # serverName = temp.get_text()
        else:
            return

        temp2 = soup.find(class_='css-1i1egz4').find_all('dd')[1]
        if temp2 != "":
            getPyCount = temp2.get_text()

        myDic = {"Server::": serverName, "Players Online::": getPyCount}

        i = 0

        playTime = soup.find_all('tbody')
        for pTime in playTime:
            py = pTime.find_all('a')
            pt = pTime.find_all('time')
            for p in py:
                # print('Player::('+ p.get_text() + ') PlayTime::('+ pt[i].get_text()+')')
                # myDic[p.get_text()] = pt[i].get_text()
                pNameUni = str(p.get_text()).translate(non_bmp_map)
                myDic[pNameUni] = pt[i].get_text()
                # print(pt[i].get_text())
                i = i+1

    except requests.exceptions.HTTPError as e:
        print('HTTP ERROR::' + str(e))
        watcherLogging.error_logs(
            'An error occured in hhtp Battlemetric web scraping ::' + str(e))
    except requests.exceptions.ConnectionError as e:
        print('CONNECTION ERROR::' + str(e))
        watcherLogging.error_logs(
            'An error occured in connection Battlemetric web scraping ::' + str(e))
    except Exception as e:
        print('An error occured in Battlemetric web scraping ::' + str(e))
        watcherLogging.error_logs(
            'An error occured in Battlemetric web scraping ::' + str(e))
        return myDic

    return myDic


def get_just_joined_players(dataDictionaryNew, dataDictionaryOld):

    myTime = datetime.strptime('12:12', '%H:%M')
    myCompareTime = datetime.strptime('00:01', '%H:%M')
    myList = []
    counter = 0

    try:
        if len(dataDictionaryNew) > 0:

            tme = datetime.now().strftime('%H:%M:%S')
            mssg = f":green_circle: Joined {tme}\n"
            myList.append(mssg)

            for key, value in dataDictionaryNew.items():

                # print('Player::('+ key + ') PlayTime::('+ value +')')
                # skip the first 2 as they are headers(servername/playercount)
                if counter > 1:
                    if key in dataDictionaryOld:
                        print("Key Found ::" + str(key))
                    else:
                        myTime = datetime.strptime(value, '%H:%M')
                        if myTime.time() <= myCompareTime.time():
                            # print('Player Joined::('+ key + ') PlayTime::('+ value +')')
                            myList.append(
                                ':white_check_mark: ::(' + key + ') PlayTime::(' + value + ')\n')
                else:
                    myList.append(key + " " + value + '\n')
                counter += 1
    except Exception as e:
        print('An error occured in Battlemetric get_just_joined_players ::' + str(e))
        watcherLogging.error_logs(
            'An error occured in Battlemetric get_just_joined_players ::' + str(e))

    return myList

# get players that have logged off /compare first scan to newest scan


def get_logged_off_players(originalDiction, newDiction):

    myList = []
    # skips the first 2 rows as its the sitename and player count
    counter = 0

    siteHeader = ""
    siteTotPlayer = ""
    headerCount = 0

    try:
        if len(newDiction) > 0:

            tme = datetime.now().strftime('%H:%M:%S')
            mssg = f":red_circle: Logged {tme}\n"
            myList.append(mssg)

            for nKey, nVal in newDiction.items():
                if headerCount == 0:
                    siteHeader = nKey + " " + nVal + "\n"
                    myList.append(siteHeader)
                elif headerCount == 1:
                    siteTotPlayer = nKey + " " + nVal + "\n"
                    myList.append(siteTotPlayer)
                headerCount += 1

            for orgKey, orgVal in originalDiction.items():
                if counter > 1:
                    if orgKey in newDiction.keys():
                        print('Still On :' + orgKey +
                              ' Playing For :' + orgVal)
                        # print('Still On :' + orgKey + ' Playing For :' + orgVal)
                        # print(' ')
                    else:
                        print(':x: :' + orgKey +
                              ' Played For :' + orgVal)
                        myList.append(
                            ':x: ::(' + orgKey + ') PlayTime::(' + orgVal + ")\n")
                # else:
                    # myList.append(orgKey + " " + orgVal + '\n')
                counter += 1

    except Exception as e:
        print('An error occured in Battlemetric get_logged_off_players ::' + str(e))
        watcherLogging.error_logs(
            'An error occured in Battlemetric get_logged_off_players ::' + str(e))

    return myList


# get all current players back in a list
def get_all_current_players(dataDictionary):

    counter = 0
    myList = []

    try:
        if len(dataDictionary) > 0:

            # tme = datetime.now().strftime('%H:%M:%S')
            # mssg = f"{tme}"
            # # mssg = f"""```css\n{tme}```"""
            # myList.append(mssg)

            for key, value in dataDictionary.items():
                if counter > 1:
                    myList.append(
                        'Player::(' + key + ') PlayTime::(' + value + ')\n')
                    # print('Player::('+ key + ') PlayTime::('+ value +')')
                else:
                    myList.append(key + " " + value + '\n')
                counter += 1
    except Exception as e:
        print('An error occured in Battlemetric get_just_joined_players ::' + str(e))
        watcherLogging.error_logs(
            'An error occured in Battlemetric get_just_joined_players ::' + str(e))

    return myList
