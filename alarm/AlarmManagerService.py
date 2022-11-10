from alarm.Alarm import Alarm
from AlarmStore import AlarmStore
from util.Constant import *
from AlarmManager import *
from alarm.BatchingAlarmStore import BatchingAlarmStore


class AlarmManagerService:

    def __init__(self):
        self.mAlarmStore = BatchingAlarmStore()

    # 将当前时间移至当前，删除store中执行的batch
    def setTime(self,alarm):
        # 删除当前时间前的batch
        deleteBatch(alarm.getWhenElapsed())



    # 调度alarm
    def set(self,a):
        # 时间移至当前alarm进入时间
        setTime(a)
        if (a.flags & FLAG_IDLE_UNTIL) != 0:
            self.adjustIdleUntilTime(a)

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


        return deviceIdlePolicyTime

    # 指定的alamr有compat标识
    def isAllowedWhileIdleRestricted(self,alarm):
        return alarm.flags & (FLAG_ALLOW_WHILE_IDLE | FLAG_ALLOW_WHILE_IDLE_COMPAT) !=0

    # 只有能够置device为idle状态的才能够调用，同时判断是否有wakeup类型的alarm，提前唤醒device
    def adjustIdleUntilTime(self,alarm):
        if(alarm.flags & FLAG_IDLE_UNTIL) == 0:
            return False
        changedBeforeFuzz = False
        if (self.mNextWakeFromIdle == None):
            return changedBeforeFuzz
        upcomingWakeFromIdle = self.mNextWakeFromIdle.getWhenElapsed()
        # 添加模糊时间，在这段模糊时间中，唤醒时间按照alarm
        if (alarm.getWhenElapsed() <(upcomingWakeFromIdle - MIN_DEVICE_IDLE_FUZZ)):
            return changedBeforeFuzz
        if (upcomingWakeFromIdle <= alarm.get)

    def deleteBatch(self,time):
        while(self.mAlarmStore.getNextDeliveryTime() < time):
            self.mAlarmStore.mAlarmBatches.removeBatch(0)
            self.mNextWakeFromIdle = self.mAlarmStore.getNextWakeFromIdleAlarm()




# 测试用
if __name__ == '__main__':
    print(Constant.FLAG_IDLE_UNTIL)