from util import SystemTime


def add():
    SystemTime.setCurrentTime(SystemTime.getCurrentTime()+1)

def gettime():
    print(str(SystemTime.getCurrentTime()))