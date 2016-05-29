##
## Core.py
## This file executes the workflow for the scrap bot
##

from readConfig import Configuration
from readConfig import readConfigFile
from scrap_delegates import readDelegatesStatus
from generate_mails import sendMails
from generate_telegrams import sendTelegramNotifications
from notification_filter import readLastLog
from notification_filter import writeLastLog
import time

# 1. Read the config file
configuration = readConfigFile('botconfig.json')
delegatesList = configuration.getCandidateList()

# 2. Process the delegates one by one
delegateStatusList = readDelegatesStatus(delegatesList)

# 3. Send telegram alarms
##Current time to compute notifications
currentTime = time.time()
history = readLastLog()

# 3.1. Send telegram alerts
sendTelegramNotifications(configuration._telegramToken, configuration._listTelegram, delegateStatusList, currentTime, history)
# 3.2. Send mails
sendMails(configuration._fromMail, configuration._fromPassword, configuration._listMails, delegateStatusList)

# 4.Write log of history
writeLastLog(delegateStatusList, currentTime)

print(delegateStatusList)