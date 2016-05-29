import smtplib

## Config vars
GOOGLE_SMTP_ADDRESS = 'smtp.gmail.com'
GOOGLE_SMTP_PORT = 587

## Send mail from Gmail account
def sendGoogleMail(fromDir, fromPassword, toDir, msg):
    server = smtplib.SMTP(GOOGLE_SMTP_ADDRESS, GOOGLE_SMTP_PORT)
    server.starttls()

    server.login(fromDir, fromPassword)

    server.sendmail(fromDir, toDir, msg)

    server.quit()