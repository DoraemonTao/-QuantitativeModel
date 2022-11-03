from alarm.Alarm import Alarm
import Constant
from AlarmStore import AlarmStore
from AlarmManager import *


class AlarmManagerService:
    mALarmStore = None

    def __init__(self,alarmStore):
        self.mAlarmStore = alarmStore

    # TODO:更新idlePolicy下的Elapsed
    def adjustDeliveryTimeBasedOnDeviceIdle(self, alarm):
        nowElapsed = alarm.mWhenElapsed
        if alarm.flags & (FLAG_ALLOW_WHILE_IDLE | FLAG_WAKE_FROM_IDLE) != 0:
            deviceIdlePolicyTime = nowElapsed
        # 在idle中被限制的alarm
        elif (self.isAllowedWhileIdleRestricted(alarm)):
            # TODO: 原生使用配额机制，1小时72次才会被限制，实际可能达不到72，因此暂不引入
            deviceIdlePolicyTime = nowElapsed
        elif ((alarm.flags & FLAG_PRIORITIZE) != 0) :

    # 指定的alamr有compat标识
    def isAllowedWhileIdleRestricted(self,alarm):
        return alarm.flags & (FLAG_ALLOW_WHILE_IDLE | FLAG_ALLOW_WHILE_IDLE_COMPAT) !=0

    # def set(self,callingPackage , type, triggerAtTime, windowLength, interval, flags,):
    #     if(flags & Constant.FLAG_IDLE_UNTIL !=0):
    #         windowLength = 0
    #     exact = (windowLength == 0)
    #     if(exact):
    #         flags |= Constant.FLAG_STAND_ALONE
    #
    #     # interval合法性检查
    #     minInterval = Constant.MIN_INTERVAL
    #     if (interval >0 & interval < minInterval):
    #         interval = minInterval
    #     elif (interval > Constant.MAX_INTERVAL):
    #         interval = Constant.MAX_INTERVAL
    #
    #     if (triggerAtTime < 0):
    #         triggerAtTime = 0
    #     # 将rtc时间转化成开机时间
    #     nominalTrigger = convertToElapsed(triggerAtTime , type)
    #     minTigger = no
    #     triggerElapsed = max(minTrigger,monialTrigger)


    # def convertToElapsed(self,when,type):
    #     if (isRtc(type)):
    #         when -=
    #     return when

    # def isRtc(self,type):
    #     return (type == Constant.RTC | type == Constant.RTC_WAKEUP)




# 测试用
if __name__ == '__main__':
    print(Constant.FLAG_IDLE_UNTIL)