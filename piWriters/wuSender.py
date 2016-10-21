## Send data to WU PWS
## RapidFire Server does a GET
## 
## usage
## action [action = updateraw]
## ID [ID as registered by wunderground.com]
## PASSWORD [PASSWORD registered with this ID]
## dateutc - [YYYY-MM-DD HH:MM:SS (mysql format)]
## winddir - [0-360]
## windspeedmph - [mph]
## windgustmph - [windgustmph ]
## humidity - [%]
## tempf - [temperature F]
## rainin - [rain in]
## dailyrainin - [daily rain in accumulated]
## baromin - [barom in]
## dewptf- [dewpoint F]
## weather - [text] -- metar style (+RA) 
## clouds - [text] -- SKC, FEW, SCT, BKN, OVC
## softwaretype - [text] ie: vws or weatherdisplay

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
