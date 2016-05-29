import json
import os.path

## Class that mantains the configuration
class Configuration:

    ## Config parameters parsed here
    _fromMail = None
    _fromPassword = None
    _listMails = None
    _telegramToken = None
    _listTelegram = None

    def __init__(self):
        self._fromMail = ""
        self._fromPassword = ""
        self._listMails = []
        self._telegramToken = ""
        self._listTelegram = []

    def getCandidateList(self):
        delegates = []
        #process mails
        for mail in self._listMails.keys():
            for delegate in self._listMails[mail]:
                if delegate not in delegates:
                    delegates.append(delegate)
        #process telegrams
        for telegram in self._listTelegram.keys():
            for delegate in self._listTelegram[telegram]:
                if delegate not in delegates:
                    delegates.append(delegate)

        return delegates

##Function that return a configuration object
def readConfigFile(filename):

    if not os.path.exists(filename):
        raise Exception("config.json file does not exists")

    configFile = open(filename, 'r')
    fileContent = configFile.read()
    configFile.close()

    objectJson = json.loads(fileContent)

    configuration = Configuration()

    #extract the from file
    configuration._fromMail = objectJson['mails']['from']
    objectJson['mails'].pop('from', None)
    configuration._fromPassword = objectJson['mails']['password']
    objectJson['mails'].pop('password', None)
    configuration._listMails = objectJson['mails']
    configuration._telegramToken = objectJson['telegram']['token']
    objectJson['telegram'].pop('token', None)
    configuration._listTelegram = objectJson['telegram']

    return configuration

