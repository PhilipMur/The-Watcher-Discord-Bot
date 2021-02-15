import inspect
import os.path
import watcherLogging


def read_cofig():

    myDic = {}

    try:
        from configparser import ConfigParser
    except ImportError:
        from ConfigParser import ConfigParser  # ver. < 3.0

    # instantiate
    config = ConfigParser()

    try:
        filename = inspect.getframeinfo(inspect.currentframe()).filename
        path = os.path.dirname(os.path.abspath(
            filename)) + "/Setup/the_watcher_config.ini"
        print("Config Path :" + path)

        # parse existing file
        config.read(path)

        # read values from a section
        battlemetrics_url = config.get('section_a', 'battlemetrics_url')
        myDic['battlemetrics_url'] = battlemetrics_url

        server_ip = config.get('section_a', 'server_ip')
        myDic['server_ip'] = server_ip

        server_port = config.get('section_a', 'server_port')
        myDic['server_port'] = server_port

        bot_id = config.get('section_b', 'bot_id')
        myDic['bot_id'] = bot_id

        bot_channel_player_joined = config.getint(
            'section_b', 'bot_channel_player_joined')
        myDic['bot_channel_player_joined'] = bot_channel_player_joined

        bot_channel_commands = config.getint(
            'section_b', 'bot_channel_commands')
        myDic['bot_channel_commands'] = bot_channel_commands

        bot_player_name_changes = config.getint(
            'section_b', 'bot_player_name_changes')
        myDic['bot_player_name_changes'] = bot_player_name_changes

        bot_enable_name_changes = config.getboolean(
            'section_b', 'bot_enable_name_changes')
        myDic['bot_enable_name_changes'] = bot_enable_name_changes

        return myDic

    except Exception as e:
        print("Error reading config ::" + str(e))
        watcherLogging.error_logs(
            'Error has occured in read_cofig ::' + str(e))
