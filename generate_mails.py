##
# Mail alerts from delegate list and list of mails
##
from emailModule import mail_alert

# Generate email message for a given delegate
def generateMessageForMail(delegateStatus, email, delegateName):
    #if is not present on list
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


## Function that generates an emailModule
def generateMail(myDir, to,  msg):
    return "\r\n".join([
        "From:" + myDir,
        "To:" + to,
        "Subject: Delegate Monitor",
        "",
        msg
    ])

## Sends an email
def sendMails(fromMail, fromPassword, listMails, delegateStatusList):
    for mail in listMails.keys():
        msgList = list()
        ## Generate the msg for each related delegate
        for delegate in listMails[mail]:
            msg = generateMessageForMail(delegateStatusList, mail, delegate)
            msgList.append(msg)

        print(mail + " --> ")
        print(msgList)

        ## Send mail
        msgContent = ""
        for msg in msgList:
            msgContent = msgContent + msg
        mail_alert.sendMail(fromMail, fromPassword, mail, msgContent)
