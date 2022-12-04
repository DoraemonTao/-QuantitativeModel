import sys
import numpy as np
import matplotlib.pyplot as plt

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
    nextAlarm = alarms.pop(0)
    nextJob = jobs.pop(0)
    while len(alarms) != 0 or len(jobs) != 0:
        if nextAlarm.enqueueTime < nextJob.completedJobTimeElapsd:
            tasks.append(nextAlarm)
            if len(alarms) == 0:
                tasks.append(nextJob)
                for job in jobs:
                    tasks.append(job)
                return tasks
            else:
                nextAlarm = alarms.pop(0)
        else:
            tasks.append(nextJob)
            if len(jobs) == 0:
                tasks.append(nextAlarm)
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
            # 系统时间移至当前task进入时间
            SystemTime.setCurrentTime(task.completedJobTimeElapsd)
            alarmManagerService.deliveryAlarm()
            alarmManagerService.align(task)
            jobSchedulerService.schedule(task)
    SystemTime.setCurrentTime(sys.maxsize)
    alarmManagerService.deliveryAlarm()
    jobSchedulerService.deliveryJob()

# 打印输出alarm的基本信息
def dump_alarm_situation(alarms):
    alarms_num = len(alarms)
    flex_num = 0
    repeat_num = 0
    wakeup_num = 0
    flex_wakeup_num = 0
    exact_num = 0
    error_num = 0
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
        if alarm.flags & AlarmManager.FLAG_STANDALONE !=0:
            exact_num += 1
        if alarm.flags & AlarmManager.FLAG_STANDALONE == 0 and alarm.windowLength == 0:
            error_num += 1
    print("可延长alarm占比："+str(flex_num/alarms_num)+"\n")
    print("周期性alarm占比：" + str(repeat_num/alarms_num) + "\n")
    print("wakeup型alarm占比：" + str(wakeup_num / alarms_num) + "\n")
    print("wakeup&可延长型alarm占比：" + str(flex_wakeup_num/ alarms_num) + "\n")
    print("不可对齐的alarm占比：" + str(exact_num / alarms_num) + "\n")
    print("加入batch无法对齐的alarm占比：" + str(error_num / alarms_num) + "\n")


def dump_job_situation(jobs):
    pass

# 打印输出指标的信息
def dump_task_delivery_situation(tasks,alarm_service,job_service):
    print("-------------Alarm-------------")
    print("Total tasks num: " + str(alarm_service.mAlarmStore.mNum) + "\n")
    print("Total delivery num: " + str(alarm_service.getDeliveryNum()) + "\n")
    print("Wakeup num: "+ str(alarm_service.getWakeupNum()))
    print("-------------Job-------------")
    print("Total delivery num: " + str(job_service.mDeliveryNum) + "\n")
    print("------------Tasks------------")
    print("Tasks num: " + str(len(tasks)))
    print("Tasks delivery num: " + str(alarm_service.getDeliveryNum()+job_service.mDeliveryNum))
    print("Decrease ratio: " + str((len(tasks)-alarm_service.getDeliveryNum()-job_service.mDeliveryNum) /
                                (len(tasks)) * 100) + "%\n")
    print("Align num: " + str(alarm_service.alarm_job_align_num))
    print("Align ratio: " + str((alarm_service.alarm_job_align_num) /
                                   (alarm_service.getDeliveryNum()+job_service.mDeliveryNum) * 100) +"%")
    task_delivery_num = alarm_service.getDeliveryNum()+job_service.mDeliveryNum
    wakeup_num = alarm_service.getWakeupNum()
    return task_delivery_num,wakeup_num


def get_task(path):
    fileContent = parse_txt(path)
    mParseText = ParseText(fileContent)
    mParseText.parse()
    mAlarm = mParseText.get_alarm_store()
    mJob = mParseText.get_job_store()
    return mAlarm, mJob



# TODO: Test All Policy Target
def test_all_policy(mTask):
    CHANGE_POLICY = [False,True]
    DELAY_POLICY = [False,True]
    for delay in DELAY_POLICY:
        for change in CHANGE_POLICY:
            # Whether apply align policy
            alarmService = AlarmManagerService(DELIVERY_TIME_CHANGE=change)
            jobService = JobSchedulerService()
            # Whether enlarge alarm windowLength
            delivery_time_delay(mTask,ratio=2, WINDOW_LENGTH_ENLARGE=delay)
            delivery_tasks(mTask, alarmService, jobService)
            if delay:
                if change:
                    print("--------------------------- Apply align policy and Enlarge alarm windowLength. --------------------------- \n")
                else:
                    print("--------------------------- Enlarge alarm windowLength. --------------------------- \n")
            else:
                if change:
                    print("--------------------------- Apply align policy. ---------------------------\n")
                else:
                    print("--------------------------- Native policy. --------------------------- \n")
            dump_task_delivery_situation(mTask,alarmService, jobService)

def test_diff_enlarge_ratio(mTask):
    ratios = np.linspace(1, 3, 20)
    delivery_list = []
    wakeup_list = []
    align_delivery_list = []
    align_wakeup_list = []
    changes = [True,False]
    i = 0

    for ratio in ratios:
        for change in changes:
            alarmService = AlarmManagerService(DELIVERY_TIME_CHANGE=change)
            jobService = JobSchedulerService()
            # Whether enlarge alarm windowLength
            delivery_time_delay(mTask, ratio=ratio, WINDOW_LENGTH_ENLARGE=True)
            delivery_tasks(mTask, alarmService, jobService)
            print("--------------------------- %.1f ratio --------------------------- \n" %(ratio))
            task_delivery_num,wakeup_num=dump_task_delivery_situation(mTask, alarmService, jobService)
            if change:
                align_delivery_list.append(task_delivery_num)
                align_wakeup_list.append(wakeup_num)
            else:
                delivery_list.append(task_delivery_num)
                wakeup_list.append(wakeup_num)
    for i in range(len(wakeup_list)-1):
        wakeup_list[i+1] = wakeup_list[i+1] / wakeup_list[0]
        delivery_list[i + 1] = delivery_list[i + 1] / delivery_list[0]
        align_wakeup_list[i + 1] = align_wakeup_list[i + 1] / align_wakeup_list[0]
        align_delivery_list[i + 1] = align_delivery_list[i + 1] / align_delivery_list[0]
    wakeup_list[0] = 1
    delivery_list[0] = 1
    align_wakeup_list[0] = 1
    align_delivery_list[0] = 1

    # figure 1
    plt.title("Different enlarge ratio")
    plt.xlabel("Enlarge ratio")
    plt.ylabel("Decrease ratio")
    plt.plot(ratios,wakeup_list,label="Wakeup_ratio",marker = 'o')
    plt.plot(ratios,delivery_list,label="Delivery_ratio",marker = 'o')
    plt.legend()
    plt.show()

# 得到硬件的调用次数
def get_component_usage_num(mTask):


if __name__ == '__main__':
    mAlarm = []
    mJob = []
    mTask = []
    WINDOW_LENGTH_ENLARGE = DEFAULT_WINDOW_LENGTH_ENLARGE
    DELIVERY_TIME_CHANGE = DEFAULT_DELIVERY_TIME_CHANGE
    log_path = 'data/result.log'

    mAlarm , mJob = get_task(log_path)

    # 将alarm和job按照enqueueTime排序
    mAlarm.sort(key=lambda alarm: alarm.enqueueTime)
    mJob.sort(key=lambda job: job.completedJobTimeElapsd)
    dump_alarm_situation(mAlarm)
    mTask = sort_alarm_job(mAlarm, mJob)
    test_all_policy(mTask)
    # test_diff_enlarge_ratio(mTask)



