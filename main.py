from util.Parse import Parse
from alarm.AlarmManagerService import *
from job.JobSchedulerService import *
from util.strategy import *
from util.ParseText import *

def parse_txt(BatteryState):
    f = open(BatteryState, encoding="utf-8")
    fileContent = f.readlines()
    f.close()
    return fileContent


# 将job和alarm按时间统一排序
def sort_alarm_job(alarms, jobs):
    tasks = []
    if len(alarms) == 0:
        tasks.append(jobs)
        return tasks
    else:
        nextAlarm = alarms.pop(0)
    if len(jobs) == 0:
        tasks.append(nextAlarm)
        for alarm in alarms:
            tasks.append(alarm)
        return tasks
    else:
        nextJob = jobs.pop(0)
    while len(alarms) != 0 or len(jobs) != 0:
        if nextAlarm.enqueueTime < nextJob.completedJobTimeElapsd:
            tasks.append(nextAlarm)
            if len(alarms) == 0:
                for job in jobs:
                    tasks.append(job)
                return tasks
            else:
                nextAlarm = alarms.pop(0)
        else:
            tasks.append(nextJob)
            if len(jobs) == 0:
                for alarm in alarms:
                    tasks.append(alarm)
                return tasks
            else:
                nextJob = jobs.pop(0)
    return tasks


def delivery_tasks(tasks, alarmManagerService,jobSchedulerService):
    for task in tasks:
        if isinstance(task, Alarm):
            # 系统时间移至当前task进入时间
            SystemTime.setCurrentTime(task.enqueueTime)
            alarmManagerService.set(task)
            # jobSchedulerService.deliveryJob()
        else:
            pass
            # 系统时间移至当前task进入时间
            # SystemTime.setCurrentTime(task.completedJobTimeElapsd)
            # alarmManagerService.deliveryAlarm()
            # jobSchedulerService.schedule(task)

# 打印输出alarm的基本信息
def dump_alarm_situation(alarms):
    alarms_num = len(alarms)
    flex_num = 0
    repeat_num = 0
    wakeup_num = 0
    flex_wakeup_num = 0
    for alarm in alarms:
        # is Wakeup?
        if alarm.wakeup:
            wakeup_num += 1
        if alarm.windowLength != 0:
            flex_num += 1
            if alarm.wakeup:
                flex_wakeup_num += 1
        if alarm.repeatInterval != 0:
            repeat_num += 1
    print("可延长alarm占比："+str(flex_num/alarms_num)+"\n")
    print("周期性alarm占比：" + str(repeat_num/alarms_num) + "\n")
    print("wakeup型alarm占比：" + str(wakeup_num / alarms_num) + "\n")
    print("wakeup&可延长型alarm占比：" + str(flex_wakeup_num/ alarms_num) + "\n")

def dump_job_situation(jobs):
    pass

# 打印输出指标的信息
def dump_task_delivery_situation(alarm_service,job_service):
    print("-------------Alarm-------------")
    print("Total tasks num: " + str(alarm_service.mAlarmStore.mNum) + "\n")
    print("Total delivery num: " + str(alarm_service.getDeliveryNum()) + "\n")
    print("Wakeup num: "+ str(alarm_service.getWakeupNum()))
    print("-------------Job-------------")
    print("Total delivery num: " + str(job_service.mDeliveryNum) + "\n")
    print("------------Tasks------------")

def get_task(path):
    fileContent = parse_txt(path)
    mParseText = ParseText(fileContent)
    mParseText.parse()
    mAlarm = mParseText.get_alarm_store()
    mJob = mParseText.get_job_store()
    return mAlarm, mJob

if __name__ == '__main__':
    mAlarm = []
    mJob = []
    mTask = []
    log_path = 'data/result.log'
    alarmService = AlarmManagerService()
    jobService = JobSchedulerService()
    mAlarm , mJob = get_task(log_path)

    # 将alarm和job按照enqueueTime排序
    mAlarm.sort(key=lambda alarm: alarm.enqueueTime)
    mJob.sort(key=lambda job: job.completedJobTimeElapsd)
    # 将delivery time延长至repeatInterval
    if WINDOW_LENGTH_ENLARGE:
        delivery_time_delay(mAlarm)
    dump_alarm_situation(mAlarm)
    mTask = sort_alarm_job(mAlarm, mJob)
    delivery_tasks(mTask,alarmService,jobService)
    dump_task_delivery_situation(alarmService,jobService)


