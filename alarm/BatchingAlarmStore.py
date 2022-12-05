from alarm.AlarmManager import *
from util.Constant import *

# 对齐模块中alarm的数据结构
from util.bs_csv import get_uid_hardware


class BatchingAlarmStore:


    def __init__(self):
        self.mAlarmBatches = []
        self.mNum = 0
        self.deliveryBatchNum = 0

    def add(self, alarm):
        self.insertAndBatchAlarm(alarm)
        self.mNum = self.mNum + 1

    def addAll(self, alarms):
        if (alarms == None):
            return
        for a in alarms:
            self.add(a)

    # 模块暂不需要，后续根据情况编写
    def remove(self):
        return

    def removeBatch(self,index):
        self.mNum -= len(self.mAlarmBatches[index])
        self.mAlarmBatches.pop(index)


    def rebatchAllAlarms(self):
        oldBatched = self.mAlarmBatches
        self.mAlarmBatches = []
        for batch in oldBatched:
            for i in range(len(batch)):
                self.insertAndBatchAlarm(batch[i])

    def getSize(self):
        return self.mNum

    # 得到下次的交付时间
    def getNextDeliveryTime(self):
        if len(self.mAlarmBatches):
            return self.mAlarmBatches[0].mStart

    # 得到下次唤醒的时间
    def getNextWakeupDeliveryTime(self):
        for b in self.mAlarmBatches:
            if b.hasWakeups():
                return b.mStart

    def getNextWakeFromIdleAlarm(self):
        for batch in self.mAlarmBatches:
            if batch.mFlags & FLAG_WAKE_FROM_IDLE == 0:
                continue
            for i in range(len(batch)):
                a = batch.get(i)
                if a.flags & FLAG_WAKE_FROM_IDLE !=0:
                    return a
        return None

    # 将alarm插入至合适的batch中
    def insertAndBatchAlarm(self, alarm):
        whichBatch = -1 if (alarm.flags & FLAG_STANDALONE != 0) \
            else self.attemptCoalesce(alarm.getWhenElapsed(),alarm.getMaxWhenElapsed())
        if whichBatch < 0:
            self.addBatch(self.mAlarmBatches, Batch(alarm))
        else:
            batch = self.mAlarmBatches[whichBatch]
            if batch.add(alarm):
                self.mAlarmBatches.pop(whichBatch)
                self.addBatch(self.mAlarmBatches,batch)

    # 在alarmStore队列中加入新的Batch
    def addBatch(self, list, newBatch):
        if len(list) == 0:
            list.append(newBatch)
        else:
            # index = self.binarySearch(list, newBatch)
            index = self.binarySearch(list, newBatch,0,len(list)-1)
            list.insert(index, newBatch)

    # 二分查找
    def binarySearch(self, list, newBatch, l, r):
        if r >= l:
            mid = int(l + (r - l) / 2)
            if list[mid].mStart > newBatch.mStart:
                return self.binarySearch(list, newBatch, l, mid - 1, )
            else:
                return self.binarySearch(list, newBatch, mid + 1, r)
        else:
            return l
    # def binarySearch(self, list, newBatch):
    #     for i in range(len(list)):
    #         if newBatch.mStart < list[i].mStart:
    #             return i
    #     return len(list)

    # 返回对应的batch索引，-1表示未找到
    # def attemptCoalesce(self, whenElapsed, maxWhen):
    #     n = len(self.mAlarmBatches)
    #     for i in range(n):
    #         b = self.mAlarmBatches[i]
    #         if (b.mFlags & FLAG_STANDALONE == 0) and b.canHold(whenElapsed, maxWhen):
    #             return i
    #     return -1

    # 返回对应的batch索引，-1表示未找到
    def attemptCoalesce(self, whenElapsed, maxWhen):
        if TIME_OVERLAP_PRIORITY:
            n = len(self.mAlarmBatches)
            # 时间重复率
            batch_priority = []
            for i in range(n):
                priority = 0
                b = self.mAlarmBatches[i]
                if (b.mFlags & FLAG_STANDALONE == 0) and b.canHold(whenElapsed, maxWhen):
                    # 若窗口间隔等于0 则直接返回合适的batch
                    if whenElapsed  != maxWhen:
                        if whenElapsed < b.mStart:
                            if maxWhen < b.mEnd:
                                overlap = (maxWhen - b.mStart)/ (b.mEnd - b.mStart)
                            else:
                                overlap = (b.mEnd - b.mStart) / (b.mEnd - b.mStart)
                        else:
                            if maxWhen < b.mEnd:
                                overlap = (maxWhen - whenElapsed) / (b.mEnd - b.mStart)
                            else:
                                overlap = (b.mEnd - whenElapsed) / (b.mEnd - b.mStart)
                    else:
                        overlap = 0
                    if b.hasWakeups:
                        if overlap > 0.75:
                            priority = 1
                        elif overlap > 0.5:
                            priority = 2
                        elif overlap > 0.25:
                            priority = 3
                        else:
                            priority = 7
                    else:
                        if overlap > 0.75:
                            priority = 4
                        elif overlap > 0.5:
                            priority = 5
                        elif overlap > 0.25:
                            priority = 6
                        else:
                            priority = 8
                else:
                    priority = 9
                batch_priority.append(priority)
            min_priority = min(batch_priority)
            if min_priority == 9:
                return -1
            return batch_priority.index(min_priority)
        else:
            n = len(self.mAlarmBatches)
            for i in range(n):
                b = self.mAlarmBatches[i]
                if (b.mFlags & FLAG_STANDALONE == 0) and b.canHold(whenElapsed, maxWhen):
                    return i
            return -1

    # 去除当前时间触发的alarm
    def removePendingAlarms(self,nowElapsed):
        deliveryNum = 0
        wakeupNum = 0
        hardware_usages_num = 0
        while len(self.mAlarmBatches)>0:
            batch = self.mAlarmBatches[0]
            if batch.mStart > nowElapsed:
                break
            if batch.hasWakeups():
                wakeupNum += 1
            if batch.hardware_set is not None:
                hardware_usages_num += len(batch.hardware_set)
            self.mAlarmBatches.pop(0)
            deliveryNum += 1
        return deliveryNum , wakeupNum, hardware_usages_num

    def updateAlarmDeliveries(self,fun):
        changed = False
        for b in self.mAlarmBatches:
            for i in range(len(b)):
                # 匿名函数，由调用者定义函数方法
                changed |= fun(b[i])
        if changed:
            self.rebatchAllAlarms()
        return changed

    def rebatchAllAlarms(self):
        oldBatches = self.mAlarmBatches
        self.mAlarmBatches = None
        for batch in oldBatches:
            for i in range(len(batch)):
                self.insertAndBatchAlarm(batch[i])

    # 找到合适的batch，并将执行时间设置为jobTime
    def setSuitableBatch(self,job):
        whichBatch = self.attemptCoalesce(job.completedJobTimeElapsd, job.completedJobTimeElapsd)
        if whichBatch < 0:
            return False
        else:
            batch = self.mAlarmBatches[whichBatch]
            if batch.setExactTime(job.completedJobTimeElapsd):
                for hardware in get_uid_hardware().get(job.callingUid, []):
                    if hardware not in batch.hardware_set:
                        batch.hardware_set.append(hardware)
                self.mAlarmBatches.pop(whichBatch)
                self.addBatch(self.mAlarmBatches, batch)
                return True

class Batch:
    # 新加入一个alarm时调用
    def __init__(self, seed):
        self.mAlarms = []
        self.mStart = seed.getWhenElapsed()
        self.mEnd = seed.getMaxWhenElapsed()
        self.mFlags = seed.flags
        self.mAlarms.append(seed)

        # 非原生，用于计算硬件调用次数
        uid_hardware = get_uid_hardware()
        self.hardware_set = uid_hardware.get(seed.uid,[])

    def get(self, index):
        return self.mAlarms[index]

    def canHold(self, whenElapsed, maxWhen):
        return (self.mEnd >= whenElapsed) and (self.mStart <= maxWhen)

    def hasWakeups(self):
        for i in range(len(self.mAlarms)):
            a = self.mAlarms[i]
            if a.wakeup:
                return True
        return False

    def add(self, alarm):
        # 是否改变batch
        newStart = False
        index = self.binarySearch(self.mAlarms,alarm,0,len(self.mAlarms)-1)
        self.mAlarms.insert(index,alarm)
        # if alarm.getWhenElapsed() > self.mStart:
        if alarm.getWhenElapsed() > self.mStart:
            self.mStart = alarm.getWhenElapsed()
            newStart = True
        if alarm.getMaxWhenElapsed() < self.mEnd:
            self.mEnd = alarm.getMaxWhenElapsed()

        # 添加硬件组
        for hardware in get_uid_hardware().get(alarm.uid,[]):
            if hardware not in self.hardware_set:
                self.hardware_set.append(hardware)

        return newStart

    def binarySearch(self, mAlarms, alarm, l, r):
        if r >= l:
            mid = int(l + (r - l) / 2)
            if mAlarms[mid].getWhenElapsed() > alarm.getWhenElapsed():
                return self.binarySearch(mAlarms, alarm, l, mid - 1, )
            else:
                return self.binarySearch(mAlarms, alarm, mid + 1, r)
        else:
            return r

    # 设置精确时间，同job触发，只在taskAlign为1下有效
    def setExactTime(self,time):
        if self.mStart < time and self.mEnd > time:
            self.mStart = time
            self.mEnd = time
            return True
        return False


