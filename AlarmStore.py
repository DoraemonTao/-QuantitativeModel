# 对齐模块中alarm的数据结构
class AlarmStore:
    mAlarmBatches = []
    mSize = None

    def __init__(self):
        self.mSize = 0

    def add(self, alarm):
        self.insertAndBatchAlarm(alarm)
        self.mSize = self.mSize + 1

    def addAll(self, alarms):
        if (alarms == None):
            return
        for a in alarms:
            self.add(a)

    # 模块暂不需要，后续根据情况编写
    def remove(self):
        return

    def rebatchAllAlarms(self):
        oldBatched = self.mAlarmBatches
        self.mAlarmBatches = []
        for batch in oldBatched:
            for i in range(len(batch)):
                self.insertAndBatchAlarm(batch[i])

    def getSize(self):
        return self.mSize

    # 得到下次的交付时间
    def getNextDeliveryTime(self):
        if len(self.mAlarmBatches):
            return self.mAlarmBatches[0].mStart

    # 将alarm插入至合适的batch中
    def insertAndBatchAlarm(self, alarm):
        whichBatch = self.attemptCoalesce(alarm.getElapsed())
        if (whichBatch < 0):
            self.addBatch(self.mAlarmBatches, self.Batch(alarm))

    # 在alarmStore队列中加入新的Batch
    def addBatch(self, list, newBatch):
        index = self.binarySearch(list, newBatch,0,len(list)-1)
        list.insert(index, newBatch)

    # 二分查找
    def binarySearch(self, list, newBatch, l, r):
        if r >= l:
            mid = int(1 + (r - 1) / 2)
            if list[mid].mStart > newBatch.mStart:
                return self.binarySearch(list, newBatch, l, mid - 1, )
            else:
                return self.binarySearch(list, newBatch, mid + 1, r)
        else:
            return r

    # 返回对应的batch索引，-1表示未找到
    def attemptCoalesce(self, whenElapsed, maxWhen):
        n = len(self.mAlarmBatches)
        for i in range(n):
            b = self.mAlarmBatches[i]
            if (b.canHold(whenElapsed, maxWhen)):
                return i

        return -1

    class Batch:
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



# 测试用
if __name__ == '__main__':
    alarmstores = AlarmStore()
    alarm = Alarm()
    alarmstores.add(alarm)
