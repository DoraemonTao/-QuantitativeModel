import Constant
from AlarmStore import AlarmStore


class AlarmManagerService:
    mALarmStore = None

    def __init__(self):
        self.mAlarmStore = AlarmStore()

    def set(self,callingPackage , type, triggerAtTime, windowLength, interval, flags,):
        if(flags & Constant.FLAG_IDLE_UNTIL !=0):
            windowLength = 0
        exact = (windowLength == 0)
        if(exact):
            flags |= Constant.FLAG_STAND_ALONE

        # interval合法性检查
        minInterval = Constant.MIN_INTERVAL
        if (interval >0 & interval < minInterval):
            interval = minInterval
        elif (interval > Constant.MAX_INTERVAL):
            interval = Constant.MAX_INTERVAL

        if (triggerAtTime < 0):
            triggerAtTime = 0
        nominalTrigger = convertToElapsed(triggerAtTime , type)







# 测试用
if __name__ == '__main__':
    print(Constant.FLAG_IDLE_UNTIL)