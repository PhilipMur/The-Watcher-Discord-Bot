
import watcherLogging

# takes in a list and gives back list items in 1000 chars or less
# discord bot has a max value of 2000 so we will send in chunks below that


def get_chunked_data(yourList):

    totalChars = 0
    stringList = list()
    stringChunk = ""

    try:
        for val in yourList:
            stringChunk += val
            # print(myStr)
            #playerCount += 1
            totalChars += int(len(val))
            if totalChars >= 1000:
                stringList.append(str(stringChunk + "\n"))
                stringChunk = ''
                #print('Total Chars:' , totalChars)
                totalChars = 0
        if(len(stringChunk) > 0):
            stringList.append(str(stringChunk + '\n'))

    except Exception as e:
        print("Error get_chunked_data ERROR ::" + e)
        watcherLogging.error_logs('Error get_chunked_data ERROR ::' + str(e))

    return stringList
