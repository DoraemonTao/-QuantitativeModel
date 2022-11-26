from util import SystemTime
class JobSchedulerService:
    def __init__(self):
        self.deliveryNum = 0

    def getDeliveryNum(self):
        return self.deliveryNum

    def setTime(self,job):
        SystemTime.setCurrentTime(job.)