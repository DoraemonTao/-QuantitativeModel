from alarm import *
from util import SystemTime
from util.Constant import *
from alarm.AlarmManager import *
from alarm.BatchingAlarmStore import BatchingAlarmStore
import random


class AlarmManagerService:
    def __init__(self):
        self.mAlarmStore = BatchingAlarmStore()
        self.currentTime = None
        self.mPendingIdleUntil = None
        self.mNextWakeFromIdle = None
        self.mDeliveryNum = 0

    # 获得当前时间
    def getCurrentTime(self):
        return self.currentTime

    def getDeliveryNum(self) -> int:
        """

        :rtype: int
        """
        return self.mDeliveryNum

    # 设置当前时间
    def setCurrentTime(self, time):
        self.currentTime = time

    # 将当前时间移至当前，删除store中执行的batch
    def setTime(self, alarm):
        SystemTime.setCurrentTime(alarm.enqueueTime)
        # 删除当前时间前的batch
        self.mDeliveryNum += self.mAlarmStore.removePendingAlarms(SystemTime.getCurrentTime())

    # 调度alarm
    def set(self, a):
        # 时间移至当前alarm进入时间
        self.setTime(a)
        if (a.flags & FLAG_IDLE_UNTIL) != 0:
            self.adjustIdleUntilTime(a)
            self.mPendingIdleUntil = a
            self.mAlarmStore.updateAlarmDeliveries(self.adjustDeliveryTimeBasedOnDeviceIdle)
        elif self.mPendingIdleUntil is not None:
            self.adjustIdleUntilTime(a)
        if a.flags & FLAG_WAKE_FROM_IDLE != 0:
            if self.mNextWakeFromIdle is None or self.mNextWakeFromIdle.getWhenElapsed() > a.getWhenElapsed():
                self.mNextWakeFromIdle = a
                # update the idle-until time when this wake earlier than previously scheduled
                if self.mPendingIdleUntil is not None:
                    update = self.mAlarmStore.AlarmStoreDeliveries(
                        lambda alarm: (alarm == self.mPendingIdleUntil) and self.adjustIdleUntilTime(alarm))
                    if update:
                        self.mAlarmStore.updateAlarmDeliveries(
                            lambda alarm: self.adjustDeliveryTimeBasedOnDeviceIdle(alarm))
        self.mAlarmStore.add(a)

    # 更新idlePolicy下的Elapsed
    def adjustDeliveryTimeBasedOnDeviceIdle(self, alarm):
        nowElapsed = self.getCurrentTime()

        if alarm.flags & (FLAG_ALLOW_WHILE_IDLE | FLAG_WAKE_FROM_IDLE) != 0:
            deviceIdlePolicyTime = nowElapsed
        # 在idle中被限制的alarm
        elif self.isAllowedWhileIdleRestricted(alarm):
            # 原生使用配额机制，1小时72次才会被限制，实际可能达不到72，因此暂不引入
            deviceIdlePolicyTime = nowElapsed
        else:
            deviceIdlePolicyTime = self.mPendingIdleUntil.getWhenElapsed()
        return alarm.setPolicyElapsed(DEVICE_IDLE_POLICY_INDEX, deviceIdlePolicyTime)

    # 指定的alarm有compat标识
    def isAllowedWhileIdleRestricted(self, alarm):
        return alarm.flags & (FLAG_ALLOW_WHILE_IDLE | FLAG_ALLOW_WHILE_IDLE_COMPAT) != 0

    # 只有能够置device为idle状态的才能够调用，同时判断是否有wakeup类型的alarm，提前唤醒device
    def adjustIdleUntilTime(self, alarm):
        if (alarm.flags & FLAG_IDLE_UNTIL) == 0:
            return False
        changedBeforeFuzz = False
        if self.mNextWakeFromIdle is None:
            return changedBeforeFuzz
        upcomingWakeFromIdle = self.mNextWakeFromIdle.getWhenElapsed()
        # 添加模糊时间，在这段模糊时间中，唤醒时间按照alarm
        if alarm.getWhenElapsed() < (upcomingWakeFromIdle - MIN_DEVICE_IDLE_FUZZ):
            return changedBeforeFuzz
        futurity = upcomingWakeFromIdle - alarm.enqueueTime
        if futurity <= MIN_DEVICE_IDLE_FUZZ:
            alarm.setPolicyElapsed(0, alarm.enqueuTime)
        else:
            upperBoundExcl = min(MAX_DEVICE_IDLE_FUZZ, futurity) + 1
            fuzz = random.randint(MIN_DEVICE_IDLE_FUZZ, upperBoundExcl)
            alarm.setPolicyElapsed(0, upcomingWakeFromIdle - fuzz)
        return True

    def deleteBatch(self, time):
        while self.mAlarmStore.getNextDeliveryTime() < time:
            self.mAlarmStore.mAlarmBatches.removeBatch(0)
            self.mNextWakeFromIdle = self.mAlarmStore.getNextWakeFromIdleAlarm()

# 测试用
if __name__ == '__main__':
    print(FLAG_IDLE_UNTIL)
