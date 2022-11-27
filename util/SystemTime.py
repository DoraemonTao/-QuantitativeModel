from util import *
from alarm.AlarmManagerService import AlarmManagerService
from job.JobSchedulerService import JobSchedulerService

def getCurrentTime():
    return Constant.SYSTEM_TIME

def setCurrentTime(time):
    Constant.SYSTEM_TIME = time
    AlarmManagerService.deliveryAlarm()
    JobSchedulerService.deliveryJob()

