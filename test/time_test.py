from datetime import datetime, timedelta


def generateUtcTime():
    now = datetime.utcnow()
    print(now)
    return str(now).split('.')[0]

def generateGtmTime(offset):
    now = datetime.utcnow() + timedelta(hours=offset)
    return str(now).split('.')[0]

print(generateUtcTime())
print(generateGtmTime(2))