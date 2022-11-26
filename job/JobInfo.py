class JobInfo():
    def __init__(self,isPeriodic,isPersisted,intervalMills,flexMills,flags):

        self.isPeriodic = isPeriodic
        self.isPersisted = isPersisted
        self.intervalMills = intervalMills
        self.flexMills = flexMills
        self.flags = flags


    def isPeriodic(self):
        return self.service

    def isPersisteed(self):
        return self.isPersisted

    def getIntervalMills(self):
        return self.intervalMills

    def getFlexMill(self):
        return self.flexMills

    def setIntervalMills(self, newIntervalMills):
        self.intervalMills = newIntervalMills

    def extendInterval(self, ratio):
        self.intervalMills = self.intervalMills * ratio



