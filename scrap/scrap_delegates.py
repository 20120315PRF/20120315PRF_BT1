from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lxml import html
from pyvirtualdisplay import Display
import os
import logging


from models.delegate_info import DelegateInfoFactory
from models.delegate_info import DelegateInfoStatus

## Static Vars
DELEGATE_MONITOR_URL = "https://testnet-explorer.lisk.io/delegateMonitor"
CHROME_DRIVER_PATH = "C:/Program Files (x86)/Google/chromedriver_win32/chromedriver.exe"
os.environ["webdriver.chrome.driver"] = CHROME_DRIVER_PATH

delegateFactory = DelegateInfoFactory()

#Check if OS is Linux
def osIsLinux():
    return os.name == 'posix'

## Generates a DOM object with selenium that mantains the html core read
def readDOMDocument(url):
    driver = None
    display = None

    if osIsLinux():
        logging.debug('OS is posix')
        Display(visible=0, size=(800, 600))
        display.start()

    # use the firefox driver or chrome instead
    try:
        #driver = webdriver.Chrome(executable_path=r"C:/Program Files (x86)/Google/chromedriver_win32/chromedriver.exe")
        driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    except:
        logging.error('Cant open a browser! Please install Chrome Core')
        raise Exception("Cant open a browser! Please install Chrome Core")

    ##Read the doc and close the driver. Wait until the 101 delegates are loaded
    driver.get(url)
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//td[@class="ng-binding" and text() = "101"]')))
    except:
        logging.error('Timeout exceeded. Cannot open the webpage')
        raise Exception("Timeout exceeded. Cannot open the webpage")

    code = html.fromstring(driver.page_source)
    driver.close()
    driver.quit()
    if display is not None:
        logging.debug('Closing virtualenv for posix OS')
        display.stop()
    return code

## Read the delegate status from the DOM document with xpath
def getDelegateStatus(code, delegateName):

    ## Get the row which mantais the delegate info and get status + approval
    delegateParsed = code.xpath('//a[@class="ng-binding" and text() = "'+ delegateName +'"]')

    ## In case that the delegate is not found
    if(delegateParsed == None or len(delegateParsed) == 0):
        delegate = delegateFactory.generateDelegate(delegateName)
        return delegate

    ## Delegate is found
    rowParent = delegateParsed[0].getparent().getparent()
    rowDetails = rowParent.xpath('.//td')

    delegate = delegateFactory.generateDelegate(delegateName)
    delegate['position'] = rowDetails[0].text

    ## If delegate is on top 101
    if int(delegate['position']) < int(102):
        delegate['uptime'] = rowDetails[5].text
        delegate['approval'] = rowDetails[6].text

        ## Check the node status
        try:
            statusClass = rowDetails[4].xpath('.//i')[0].attrib['class']

            if(statusClass != None):
                if 'red' in statusClass:
                    status = DelegateInfoStatus.STATUS_NOT_FORGING
                elif 'orange' in statusClass:
                    status = DelegateInfoStatus.STATUS_CYCLE_LOST
                elif 'green' in statusClass:
                    status = DelegateInfoStatus.STATUS_FORGING
                # else: red by default
        except:
            status = DelegateInfoStatus.STATUS_NOT_FOUND

        delegate['status'] = status

    ## If delegate is not on top 101
    else:
        delegate['uptime'] = rowDetails[3].text
        delegate['approval'] = rowDetails[4].text

    return delegate

## Read the delegates status. Must provide a delegate list
def readDelegatesStatus(delegateList):
    #delagate status list as json
    delegates = {}

    code = readDOMDocument(DELEGATE_MONITOR_URL)

    #Check delegate, verify status and add to dict
    for delegate in delegateList:
        delegateStats = getDelegateStatus(code, delegate)
        delegates[delegate] = delegateStats

    return delegates


