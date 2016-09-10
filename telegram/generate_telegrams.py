##
# Generate telegram messages and send to the user
##
import telebot
import notification_filter
from datetime import datetime, timedelta

#Singleton telegram bot
class TelegramBot:

    __telegramBot = None

    def __init__(self):
        self.__telegramBot = None

    def getBot(self, apiKey):
        if self.__telegramBot is None:
            self.__telegramBot = telebot.TeleBot(apiKey)
        return self.__telegramBot

    ## Return the bot with the api key given
    def setApiKey(self, apiKey):
        self.__telegramBot = None
        return self.getBot(apiKey)

#Instance for telegram bot
telegramBot = TelegramBot()

## Sends a message to the user
def __sendTelegramMessage(apiKey, user, msg):
     bot = telegramBot.getBot(apiKey)
     bot.send_message(int(user), str(msg) )

# Generate email message for a given delegate
def __generateMessageForTelegram( delegateStatus, user, delegateName, currentTime, history):

    ## TODO fix this filter
    #check filter. If is not valid notification, not send it
    #if not notification_filter.checkTelegramNotification(delegateName, delegateStatus, currentTime, history):
    #    return None

    #Notification ok. Check if is not present on list
    if delegateStatus[delegateName] is None:
        return "Delegate " + delegateName + " is not in the 101 top delegates list"

    # if is present on list
    msg = ""
    delegate = delegateStatus[delegateName]

    if delegate['status'] is None:
        delegate['status'] = 'Not found'

    msg = "\n\nDelegate " + delegateName + ": Status=" + delegate['status'] + "\n\t"
    msg = msg + "Position: " + delegate['position'] + "\tUptime: " + delegate['uptime'] + "\t" + "Approval: " + delegate['approval']

    return msg


## Generates a UTC Time
def generateUtcTime():
    now = datetime.utcnow()
    return str(now).split('.')[0]
## Generates GTM time with offset
def generateGtmTime(offset):
    now = datetime.utcnow() + timedelta(hours=offset)
    return str(now).split('.')[0]

## For each user of telegram, send message with notifications
def sendTelegramNotifications (apiKey, userList, delegateStatusList,currentTime, history, gtmOffset):
    for user in userList:
        msgList = list()
        ## Generate the msg for each related delegate
        for delegate in userList[user]:
            msg = __generateMessageForTelegram(delegateStatusList, user, delegate, currentTime, history)
            if msg is not None:
                msgList.append(msg)

        ## Send mail
        msgContent = ""
        for msg in msgList:
            msgContent = msgContent + msg
        ### Send notification only if msgContent is available
        if msgContent != "":
            msgContent = "[ (GTM+" + str(gtmOffset) + ") " + generateGtmTime(gtmOffset) + ' ]\n' + msgContent
            try:
                __sendTelegramMessage(apiKey, user, msgContent)
            except:
                print("Cant send message for the user " + str(user))


