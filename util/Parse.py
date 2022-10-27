import re

from alarm.Alarm import Alarm
from job.JobStatus import JobStatus


class Parse:
    """
        解析产生的Result文件

        Args:
            lines: the context of Result.txt
    """
    def __init__(self,lines):
        self.lines = lines

        # job属性  jobStatus以及jobInfo

        # jobStatus
        self.job = None
        self.callingUid = None
        self.sourcePackageName = None
        self.sourceUserId = None
        self.standbyBucket = None
        self.tag = None
        self.earliestRunTimeElapsedMillis = None
        self.latestRunTimeElapsedMillis = None
        self.lastSuccessfulRunTime = None
        self.lastFailedRunTime = None

        # jobInfo


        # jobPropertiesAndRegex
        # jobStatus
        self.jobStatusPropertiesRegex = {
            "job"                           : ["tag=(.*)" ,self.job],
            "callingUid"                    : ["uid=(\\d+)",self.callingUid],
            "sourcePackageName"             : ["pkg=(.*)",self.sourcePackageName],
            "sourceUserId"                  : ["uid=(\\d+)",self.sourceUserId],
            "standbyBucket"                 : ["Standby bucket: (\\w+)"],
            "tag"                           : ["tag=(.*)",self.tag],
            "earliestRunTimeElapsedMillis"  : ["earliest=(.*), latest",self.earliestRunTimeElapsedMillis],
            "latestRunTimeElapsedMillis"    : ["latest=(.*), original",self.latestRunTimeElapsedMillis],
            "lastSuccessfulRunTime"         : ["Last successful run: (.*)",self.lastSuccessfulRunTime],
            "lastFailedRunTime"             : ["Last failed run: (.*)",self.lastFailedRunTime],
        }
        # jobInfo
        self.jobInfoPropertiesRegex = {
            "service"        :   ["Service: (.*)",self.service],
            "isPersisted"    :   ["(PERSISTED)",self.isPersisted],
            "isPeriodic"     :   ["(PERIODIC:)",self.isPersisted],
            "intervalMills"  :   ["interval=(.*) flex",self.intervalMills],
            "flexMills"      :   ["flex=(.*)",self.flexMills]
        }



    # 清空job的属性
    def clearJobProperties(self):
        self.job = None
        self.callingUid = None
        self.sourcePackageName = None
        self.sourceUserId = None
        self.standbyBucket = None
        self.tag = None
        self.earliestRunTimeElapsedMillis = None
        self.latestRunTimeElapsedMillis = None
        self.lastSuccessfulRunTime = None
        self.lastFailedRunTime = None

    # 清空alarm的属性
    def clearAlarmProperties(self):
        self. = None

    def parseLines(self,lines):

        # 相应段的Flag标志位
        alarmContentFlag = False
        jobContentFlag = False

        # 逐行分析
        for line in lines:
            # 是否到达job段
            if not jobContentFlag:
                jobContentFlag = re.search("Job History:", line)

            # 是否到达alarm段
            if not alarmContentFlag:
                alarmContentFlag = re.search("Alarm History", line)
                if (alarmContentFlag):
                    jobContentFlag = False

            # 到达job段
            if (jobContentFlag):
                # 新的job时，将旧的job信息存储成jobStatus和jobInfo，随后清空属性
                if (re.match("  JOB #", line)):
                    if(self.job is not None):
                        mJob = JobStatus(self.job,self.callingUid,self.sourceUserId,self.standbyBucket,
                                     self.tag,self.earliestRunTimeElapsedMillis,self.latestRunTimeElapsedMillis,
                                     self.lastFailedRunTime,self.lastFailedRunTime)
                        self.clearJobProperties()

                # 查找属性
                self.getJobStatusProperties(line)

            # 到达alarm段
            if alarmContentFlag:
                # 新的alarm时，将旧的job信息存储成jobStatus，随后清空属性
                if(re.match(".*[(RTC_WAKEUP)(RTC)(ELAPSED_REALTIME_WAKEUP)(ELAPSED_REALTIME)].*",line)):
                    if(self.type is not None):
                        mAlarm = Alarm()


    # 采集jobStatus的信息
    def getJobStatusProperties(self,line):
        for key,value in self.jobStatusPropertiesRegex:
            jobSearch = re.search(value[0],line)
            if(jobSearch):
                value[1] = jobSearch.gruop(1)

        for key,value in self.jobInfoPropertiesRegex:
            jobSearch = re.search(value[0], line)
            if (key is "isPersisted" or "isPeriodic"):
                if (jobSearch):
                    value[1] = True
                else:
                    value[1] = False
            else:
                if (jobSearch):
                    value[1] = jobSearch.gruop(1)

    # 采集alarm的信息
    def getAlarmProperties(self,line):











# 提取屏幕状态
def extract_screen(lines):
    ScreenContentPattern = re.compile('(-screen )|( \+screen )')
    battery_histories = []
    flag = False
    for line in lines:

        if ('DUMP OF SERVICE batterystats:' in line):
            flag = True
        if (flag):
            content = None
            content = ScreenContentPattern.search(line)
            if (content):
                battery_histories.append(line)

    return battery_histories


# 根据内容提取出时间
def extract_time(screen_contents):
    OnScreenStatePattern = re.compile(' \+screen ')
    OffScreenStatePattern = re.compile(' \-screen ')
    TimePattern = re.compile(' \+\d+h\d+m\d+s\d+ms')

    # 记录着休眠时间段
    screen_state = []
    off_screen_time = 0

    #  取每行内容
    for content in screen_contents:
        screen_flag = None
        screen_flag = OnScreenStatePattern.search(content)
        if (screen_flag):
            # 第一次的是亮屏状态
            OnScreenTime = TimePattern.search(content).group(0)
        else:
            off_screen_time = TimePattern.search(content).group(0)

        if (screen_flag):
            screen_state.append([off_screen_time, OnScreenTime])



    return screen_state


# 提取出idle状态的
def extract_idle(lines):
    IdleContentPattern = re.compile('device_idle=')
    # 记录着idle时间段
    idle_histories = []
    flag = False
    for line in lines:

        if ('DUMP OF SERVICE batterystats:' in line):
            flag = True
        if (flag):
            content = None
            content = IdleContentPattern.search(line)
            if (content):
                idle_histories.append(line)

    return idle_histories

def extract_idle(idle_contents):
    OnIdleStatePattern = re.compile('device_idle=full')
    TimePattern = re.compile(' \+\d+h\d+m\d+s\d+ms')

    # 记录着休眠时间段
    idle_state = []
    off_idle_time = 0

    #  取每行内容
    for content in idle_contents:
        idle_flag = None
        idle_flag = OnIdleStatePattern.search(content)
        if (idle_flag):
            OnIdleTime = TimePattern.search(content).group(0)
        else:
            off_idle_time = TimePattern.search(content).group(0)

        if (idle_flag):
            idle_state.append([OnIdleTime,off_idle_time])

    return idle_state


def extra_alarm(lines):
