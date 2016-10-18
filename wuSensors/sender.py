## Send data to WU PWS
import urllib2
import re

wuSoftware = "piPWS0.1"

def wuTime(inTime):
    wuT = re.match("(\d{4}-\d{2}-\d{2})T(\d{2}):(\d{2}):(\d{2}).000Z", inTime)
    return "%s+%s%%3A%s%%3A%s" % (wuT.group(1, 2, 3, 4))


def genReq(wuID, wuPass, inTime, wuTemp, wuPress):
    req = "ID=%s&PASSWORD=%s&dateutc=%s&tempf=%s&baromin=%s&action=updateraw&softwaretype=%s" % \
          (wuID, wuPass, wuTime(inTime), wuTemp, wuPress, wuSoftware)
    
    return req

def sendReq(URI, req):
    f = urllib2.urlopen("%s?%s" % (URI, req))
    return f.read()

