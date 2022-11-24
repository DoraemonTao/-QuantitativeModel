from util.Parse import Parse
from alarm.AlarmManagerService import *
from job.JobSchedulerService import *
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
        if nextAlarm.enqueueTime < nextJob.earliestRunTimeElapsedMillis:
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


def delivery_tasks(tasks, alarmManagerService):
    for task in tasks:
        if isinstance(task, Alarm):
            alarmManagerService.set(task)


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

    # TODO:将alarm和job按照enqueueTime排序
    mAlarm.sort(key=lambda alarm: alarm.enqueueTime)
    mJob.sort(key=lambda job: job.earliestRunTimeElapsedMillis)
    mTask = sort_alarm_job(mAlarm, mJob)
    delivery_tasks(mTask,alarmService)
    print("Total tasks num: " + str(len(mTask)) + "\n")
    print("Total delivery num: "+str(alarmService.getDeliveryNum())+"\n")

