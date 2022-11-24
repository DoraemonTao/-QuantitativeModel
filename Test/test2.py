from util import SystemTime

def minus():
    SystemTime.setCurrentTime(SystemTime.getCurrentTime()-1)

def gettime():
    print(str(SystemTime.getCurrentTime()))