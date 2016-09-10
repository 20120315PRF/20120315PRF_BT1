##
## Core.py
## This file executes the workflow for the scrap bot
##

import time

from configuration.readConfig import readConfigFile
from scrap.scrap_delegates import readDelegatesStatus
from telegram.generate_telegrams import sendTelegramNotifications
from notification_filter import readLastLog
from notification_filter import writeLastLog


# 1. Read the config file
configuration = readConfigFile('configuration/botconfig.json')
delegatesList = configuration.getCandidateList()

# 2. Process the delegates one by one
delegateStatusList = readDelegatesStatus(delegatesList)

# 3. Send telegram alarms
##Current time to compute notifications
currentTime = time.time()
history = readLastLog()

# 3.1. Send telegram alerts
sendTelegramNotifications(configuration._telegramToken, configuration._listTelegram, delegateStatusList, currentTime, history, configuration.getGtm() )

# 4.Write log of history
writeLastLog(delegateStatusList, currentTime)

print(delegateStatusList)