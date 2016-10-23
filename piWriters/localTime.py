from datetime import datetime

class localTime:
  def __init__(self):
    None
    
  def getTime(self):
    now = datetime.utcnow()
    return datetime.strftime(now, "%Y-%m-%dT%H:%M:%S.000Z")

  def stop(self):
    None
  
if __name__ == '__main__':
  something = localTime()
  print something.getTime()
