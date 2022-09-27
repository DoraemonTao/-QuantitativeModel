from Alarm import Alarm
from AlarmStore import AlarmStore


class AlarmManager:
    # 使用alarmstore作为我们的存储队列
    mAlarmStore = AlarmStore()
    def __init__(self):
        return

    # 新加入一个alarm
    def set(self,type,when,whenElapsed,windowLength,
                      interval):
        alarm = Alarm(type,when,whenElapsed,windowLength,interval)
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
        # 将rtc时间转化成开机时间
        nominalTrigger = convertToElapsed(triggerAtTime , type)
        minTigger = no
        triggerElapsed = max(minTrigger,monialTrigger)


    def convertToElapsed(self,when,type):
        if (isRtc(type)):
            when -=
        return when

    def isRtc(self,type):
        return (type == Constant.RTC | type == Constant.RTC_WAKEUP)




# 测试用
if __name__ == '__main__':
    print(Constant.FLAG_IDLE_UNTIL)