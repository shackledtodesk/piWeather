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
import math
import requests
import re

class piSender:
    uri = "https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php"
    station = None
    password = None
    wuSoftware = "piPWS0.1"
    maxRetry = 3

    def __init__(self, config):
        self.station = config.get('wunderground','station')
        self.password = config.get('wunderground','password')
        if config.has_option('wunderground','uri'):
            self.uri = config.get('wunderground','uri')
        if config.has_option('wunderground', 'retry'):
            self.maxRetry = config.get('wunderground','retry')
            
    def wuTime(self, inTime):
        wuT = re.match("(\d{4}-\d{2}-\d{2})T(\d{2}):(\d{2}):(\d{2}).(\d{3,6})Z", inTime)
        (tDate, tHr, tMn, tSec, tMS) = wuT.group(1, 2, 3, 4, 5)
        tMMS = "%d.%s" % (int(tSec), tMS)
        tMMS = int(round(float(tMMS)))

        return "%s+%s%%3A%s%%3A%02d" % (tDate, tHr, tMn, tMMS)

    def genReq(self, inTime, data):
        req = "ID=%s&PASSWORD=%s&dateutc=%s&action=updateraw&softwaretype=%s" % \
              (self.station, self.password , self.wuTime(inTime), self.wuSoftware)
        for desc, val in data.items():
            req = "%s&%s=%s" % (req, desc, val)
        return req

    def sendReq(self, req):
        for i in range(0,self.maxRetry):
            try:
                f = requests.get("%s?%s" % (self.uri, req))
                if f.status_code == requests.codes.ok:
                    return "ok: %d" % f.status_code
                else:
                    sleep(10)
            except (KeyboardInterrupt, SystemExit):
                return
            except Exception:
                e = sys.exc_info()[0]
                traceback.print_exc(file=sys.stdout)                
            else:
                sleep(10)
        return "error: %d - %s" % (f.status_code, f.text)

