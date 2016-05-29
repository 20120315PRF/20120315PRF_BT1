__author__ = 'Usuario'

import os.path
import json
from models.delegate_info import DelegateInfoStatus
##
# Notification filter. Filter delegates for notifications
##
DELEGATE_STATUS_LOG_FILE = "delegateinfo.log"
## 30 minutes on telegram notifications
TIME_TELEGRAM_NOTIFICATION = (1000*60)*30
## Every 1 hour on mail notifications
TIME_MAIL_NOTIFICATION = (1000*60)*60


## Return the last config file stored
def readLastLog():
    if os.path.exists(DELEGATE_STATUS_LOG_FILE):
        logFile = open(DELEGATE_STATUS_LOG_FILE, 'r')
        fileContent = logFile.read()
        logFile.close()
        return json.loads(fileContent)

    else:
        return None

## Write the file
def writeLastLog(delegateList, currentTime):
    logFileJson = {}
    logFileJson['lastTime'] = currentTime

    for delegate in delegateList:
        logFileJson[delegateList[delegate]['name']] = 'Forging'

    logFile = open(DELEGATE_STATUS_LOG_FILE, 'w')
    logFile.write(json.dumps(logFileJson))
    logFile.close()

## Check if mails has to be sent
def checkEmailNotification(timestamp, delegateName, currentStatus, lastLog):

    ## If there is no log, return true ever
    if lastLog is None:
        return True
    ## Check the possibilities
    else:
        ## Delegate not in log before
        if not delegateName in lastLog:
            return True
        ## Delegate exists on log before
        else:
            ##Current status is green or not found
            if not (currentStatus is DelegateInfoStatus.STATUS_NOT_FORGING or currentStatus is DelegateInfoStatus.STATUS_CYCLE_LOST):
                return False

            ## Current status if not foging or lost
            else:

                ## Last state != current OR elapsed > 60m -> sned notif
                if (currentStatus is not lastLog[delegateName]) or (timestamp > ( int(lastLog['lastTime']) + TIME_MAIL_NOTIFICATION ) ):
                    return True
                else:
                    return False


def checkTelegramNotification (timestamp, delegateName, currentStatus, lastLog):
    ## If there is no log, return true
    if lastLog is None:
        return True
    ## Log exists
    else:
        ## Status red or orange -> notify
        if currentStatus is DelegateInfoStatus.STATUS_NOT_FORGING or currentStatus is DelegateInfoStatus.STATUS_CYCLE_LOST:
            return True
        ## If 30 min elapsed after the last notification and the status is forging or not found, send another notification
        if (currentStatus is DelegateInfoStatus.STATUS_FORGING or currentStatus is DelegateInfoStatus.STATUS_NOT_FOUND) and timestamp > (lastLog['lastTime'] + TIME_TELEGRAM_NOTIFICATION):
            return True
        ## time elapsed < 30 min and status is forging or not found -> not notify again
        else:
            return False
