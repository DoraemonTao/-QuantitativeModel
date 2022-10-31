
from alarm.BatchingAlarmStore import BatchingAlarmStore

# 应用不同策略下的alarm对齐次数
class OptiBatchedAlarmStore(BatchingAlarmStore):
    def insertAndBatchAlarm(self, alarm):
        whichBatch = self.attemptCoalesce(alarm.getWhenElapsed(), alarm.getMaxWhenElapsed())
        if (whichBatch < 0):
            self.addBatch(self.mAlarmBatches, OptiBatch(alarm))


# 优化Batch机制，将交付时间从mStart改为mEnd
class OptiBatch:
    mStart = None
    mEnd = None
    mAlarms = []

    # 新加入一个alarm时调用
    def __init__(self, seed):
        self.mStart = seed.getWhenElapsed()
        self.mEnd = seed.getMaxWhenElapsed()
        self.mAlarms.append(seed)

    def size(self):
        return len(self.mAlarms)

    def get(self, index):
        return self.mAlarms[index]

    def canHold(self, whenElapsed, maxWhen):
        return (self.mEnd >= whenElapsed) & (self.mStart <= maxWhen)

    def add(self, alarm):
        # 是否改变batch
        newStart = False
        index = self.binarySearch(self.mAlarms,alarm,0,len(self.mAlarms)-1)
        self.mAlarms.insert(index,alarm)
        if alarm.getWhenElapsed() > self.mStart:
            self.mStart = alarm.getWhenElapsed()
            newStart = True
        if alarm.getMaxWhenElapsed() < self.mEnd:
            self.mEnd = alarm.getMaxWhenElapsed()
        return newStart

    def binarySearch(self, mAlarms, alarm, l, r):
        if r >= l:
            mid = int(1 + (r - 1) / 2)
            if mAlarms[mid].mStart > alarm.mStart:
                return self.binarySearch(mAlarms, alarm, l, mid - 1, )
            else:
                return self.binarySearch(mAlarms, alarm, mid + 1, r)
        else:
            return r


