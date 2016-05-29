import json
import notification_filter
import time
from models.delegate_info import DelegateInfoStatus

## No previous log and not forging
def test1():
    current_time = time.time()
    result = notification_filter.checkTelegramNotification(current_time, "genesis_1", DelegateInfoStatus.STATUS_NOT_FORGING, None)
    print ("Test1 = " + str(result is True))


## No previous log and forging
def test2():
    current_time = time.time()
    result = notification_filter.checkTelegramNotification(current_time, "genesis_1", DelegateInfoStatus.STATUS_FORGING, None)
    print ("Test2 = " + str(result is True))

## Previous log time < 30 and forging DelegateInfoStatus.STATUS_FORGING
def test3():
    previousLog = {}
    previousLog['genesis_1'] = DelegateInfoStatus.STATUS_FORGING
    previousLog['lastTime'] = time.time() - (1000*60)

    current_time = time.time()

    result = notification_filter.checkTelegramNotification(current_time, "genesis_1", DelegateInfoStatus.STATUS_FORGING, previousLog)
    print ("Test3 = " + str(result is False))

## Previous log time < 30 and forging DelegateInfoStatus.STATUS_FORGING
def test4():
    previousLog = {}
    previousLog['genesis_1'] = DelegateInfoStatus.STATUS_FORGING
    previousLog['lastTime'] = time.time() - (31*1000*60)

    current_time = time.time()

    result = notification_filter.checkTelegramNotification(current_time, "genesis_1", DelegateInfoStatus.STATUS_FORGING, previousLog)
    print ("Test3 = " + str(result is True))

## Bateria de test
#test1()
#test2()
#test3()
#test4()

### TEST DE MAIL
def mailTest1():
    current_time = time.time()
    result = notification_filter.checkEmailNotification(current_time, "genesis_1", DelegateInfoStatus.STATUS_NOT_FORGING, None)
    print ("TestMail1 = " + str(result is True))

def mailTest2():
    current_time = time.time()
    result = notification_filter.checkEmailNotification(current_time, "genesis_1", DelegateInfoStatus.STATUS_FORGING, None)
    print ("TestMail2 = " + str(result is True))

## Previous log time < 30 and forging DelegateInfoStatus.STATUS_FORGING
def mailTest3():
    previousLog = {}
    previousLog['genesis_1'] = DelegateInfoStatus.STATUS_FORGING
    previousLog['lastTime'] = time.time() - (1000*60)

    current_time = time.time()

    result = notification_filter.checkEmailNotification(current_time, "genesis_1", DelegateInfoStatus.STATUS_FORGING, previousLog)
    print ("Test3 = " + str(result is False))

## Previous log time > 60 and forging DelegateInfoStatus.STATUS_FORGING
def mailTest4():
    previousLog = {}
    previousLog['genesis_1'] = DelegateInfoStatus.STATUS_NOT_FORGING
    previousLog['lastTime'] = time.time() - (62*1000*60)

    current_time = time.time()

    result = notification_filter.checkEmailNotification(current_time, "genesis_1", DelegateInfoStatus.STATUS_NOT_FORGING, previousLog)
    print ("Test4 = " + str(result is True))

## Previous log time < 60 and forging DelegateInfoStatus.STATUS_FORGING
def mailTest4():
    previousLog = {}
    previousLog['genesis_1'] = DelegateInfoStatus.STATUS_NOT_FORGING
    previousLog['lastTime'] = time.time() - (50*1000*60)

    current_time = time.time()

    result = notification_filter.checkEmailNotification(current_time, "genesis_1", DelegateInfoStatus.STATUS_NOT_FORGING, previousLog)
    print ("Test4 = " + str(result is False))
## Bateria de test
mailTest1()
mailTest2()
mailTest3()
mailTest4()