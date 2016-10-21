## Send data to WU PWS
from time import sleep
import requests
import re

wuSoftware = "piPWS0.1"
maxRetry = 3

def wuTime(inTime):
    wuT = re.match("(\d{4}-\d{2}-\d{2})T(\d{2}):(\d{2}):(\d{2}).000Z", inTime)
    return "%s+%s%%3A%s%%3A%s" % (wuT.group(1, 2, 3, 4))


def genReq(wuID, wuPass, inTime, wuTemp, wuPress):
    global wuSoftware
    req = "ID=%s&PASSWORD=%s&dateutc=%s&tempf=%s&baromin=%s&action=updateraw&softwaretype=%s" % \
          (wuID, wuPass, wuTime(inTime), wuTemp, wuPress, wuSoftware)    
    return req

def sendReq(URI, req):
    global maxRetry
    for i in range(1,maxRetry):
        try:
            f = requests.get("%s?%s" % (URI, req))
            if f.status_code == requests.codes.ok:
                return "ok: %d" % f.status_code
            else:
                sleep(10)
        except:
            e = sys.exc_info()[0]
            logger.debug(e)
        else:
            sleep(10)
    return "error: %d - %s" % (f.status_code, f.text)
