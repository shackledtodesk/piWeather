## Send data to a Graphite/Carbon Server

import sys, time, socket
from datetime import datetime

class piSender:
    carbon_server = '127.0.0.1'
    carbon_port = 2003
    station = "pi2wu"
    
    def __init__(self, config):
        if config.has_option('graphite','server'):
            self.carbon_server = config.get('graphite','server')
        if config.has_option('graphite','port'):
            self.carbon_port = config.get('graphite','port')
        if config.has_option('general','station'):
            self.station = config.get('general','station')
            
        self.sock = socket.socket()
        try:
            self.sock.connect( (self.carbon_server, self.carbon_port) )
        except socket.error:
            raise SystemExit("Could not connect to carbon server.")


    def genReq(self, inTime, data):
        epoch_time = time.mktime(strptime(inTime, "%Y-%m-%d %H:%M:%s").timetuple())
        lines = []
        for name, value in data.items():
            lines.append("%s.%s %s %d" %
                         (self.station, name, value, epoch_time))
        message = '\n'.join(lines) + '\n'
        return message

    def sendReq(self, req):
        try:
            self.sock.sendall(message)
        except Exception:
            e = sys.exc_info()[0]
            return e
        else:
            return "ok"
            
