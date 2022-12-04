from alarm.BatchingAlarmStore import BatchingAlarmStore
from alarm.BatchingAlarmStore import Batch

# 应用不同策略下的alarm对齐次数
class OptiBatchedAlarmStore(BatchingAlarmStore):

    def getNextDeliveryTime(self):
        if len(self.mAlarmBatches):
            return self.mAlarmBatches[0].mEnd

    def getNextWakeupDeliveryTime(self):
        for b in self.mAlarmBatches:
            if b.hasWakeups():
                return b.mEnd

    def removePendingAlarms(self, nowElapsed):
        deliveryNum = 0
        wakeupNum = 0
        while len(self.mAlarmBatches) > 0:
            batch = self.mAlarmBatches[0]
            if batch.mEnd > nowElapsed:
                break
            if batch.hasWakeups():
                wakeupNum += 1
            self.mAlarmBatches.pop(0)
            deliveryNum += 1
        return deliveryNum, wakeupNum


