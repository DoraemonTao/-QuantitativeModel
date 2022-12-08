from job.JobStore import JobStore
from util import SystemTime
from util.bs_csv import get_uid_hardware


class JobSchedulerService:
    def __init__(self):
        self.mDeliveryNum = 0
        self.mHardwareUsage = 0
        self.mJobs = JobStore()

    # job加入时的调度函数
    def schedule(self,j):
        self.deliveryJob()
        self.startTackingJobLocked(j)
        # TODO: alarm and job aglin


    # 交付满足约束条件的alarm
    def deliveryJob(self):
        mDeliveryNum,mHardwareUsage= self.isReadyToBeExecutedLocked(SystemTime.getCurrentTime())
        self.mDeliveryNum += mDeliveryNum
        self.mHardwareUsage += mHardwareUsage

    # job任务跟踪
    def startTackingJobLocked(self,jobStatus):
        update = self.mJobs.add(jobStatus)

    # 将满足条件的job触发
    def isReadyToBeExecutedLocked(self,time):
        delivery_num = 0
        hardware_usage = 0
        alljobs = self.mJobs.mJobSet.getAllJobs()
        for job in alljobs:
            # 满足时间约束
            if job.completedJobTimeElapsd <= time:
                hardware_usage += len(get_uid_hardware().get(job.callingUid,[]))
                self.mJobs.remove(job)
                delivery_num += 1
        return delivery_num,hardware_usage

     # 得到总交付数
    def getDeliveryNum(self):
        return self.mDeliveryNum