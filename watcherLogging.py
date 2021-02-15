import datetime
import inspect
import os.path


def error_logs(textString):
    try:
        filename = inspect.getframeinfo(inspect.currentframe()).filename
        path = os.path.dirname(os.path.abspath(filename))
        print("Log Path :" + path)
        #dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(path + "/the_watcher_logs.txt", 'a') as myFile:
            myFile.write(datetime.datetime.now().ctime() +
                         " :: " + textString + "\n")
            myFile.close()
    except Exception as e:
        print("Error writing logs ::" + str(e))


error_logs("Logging Started")
