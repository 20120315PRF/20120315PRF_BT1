from mail_google import sendGoogleMail

## Function that generates an emailModule
def generateMailMessage(fromDir, toDir,  msg):
    return "\r\n".join([
        "From:" + fromDir,
        "To:" + toDir,
        "Subject: Delegate Monitor",
        "",
        msg
    ])

## Generic function for sending a msg
def sendMail(fromMail, fromPassword, toMail, msg):
    #Generate the msg
    generatedMsg = generateMailMessage(fromMail, toMail, msg)

    ## TODO: condition para enviar segundo la extensio del mail
    sendGoogleMail(fromMail, fromPassword, toMail, generatedMsg)

