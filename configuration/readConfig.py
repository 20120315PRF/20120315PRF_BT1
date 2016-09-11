import json
import os.path
import logging

## Class that mantains the configuration
class Configuration:

    ## Config parameters parsed here
    _telegramToken = None
    _listTelegram = None
    _mode = None
    _gtm = 0

    def __init__(self):
        self._telegramToken = ""
        self._listTelegram = []
        self._mode = ""
        self._gtm = 0

    def getCandidateList(self):
        delegates = []
        #process telegrams
        for telegram in self._listTelegram.keys():
            for delegate in self._listTelegram[telegram]:
                if delegate not in delegates:
                    delegates.append(delegate)

        return delegates

    def getMode(self):
        return self._mode

    def getGtm(self):
        if not self._gtm is None:
            return self._gtm
        else:
            return 0

##Function that return a configuration object
def readConfigFile(filename):

    if not os.path.exists(filename):
        logging.error("Configuration file %s does not exists", filename)
        raise Exception("config.json file does not exists")

    configFile = open(filename, 'r')
    fileContent = configFile.read()
    configFile.close()

    objectJson = json.loads(fileContent)

    configuration = Configuration()

    #extract the from file
    configuration._telegramToken = objectJson['telegram']['token']
    objectJson['telegram'].pop('token', None)
    configuration._listTelegram = objectJson['telegram']
    # Working mode
    configuration._mode = objectJson['mode']
    # GTM offset
    if 'GTM' in objectJson:
        configuration._gtm = objectJson['GTM']

    return configuration

