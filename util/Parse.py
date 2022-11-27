import re

from alarm import Alarm
from job import JobStatus


class Parse:
    """
        解析产生的Result文件

        Args:
            lines: the context of Result.txt
    """
    def __init__(self,lines):
        self.lines = lines

        # jobPropertiesAndRegex
        # jobStatus
        self.jobStatusPropertiesRegex = {
            "callingUid"                    : ["uid=(\\d+)",None],
            "sourcePackageName"             : ["pkg=(.+)",None],
            "sourceUserId"                  : ["uid=(\\d+)",None],
            "standbyBucket"                 : ["Standby bucket: (\\w+)",None],
            "tag"                           : ["tag=(.+)",None],
            "earliestRunTimeElapsedMillis"  : ["earliest=(.+), latest",None],
            "latestRunTimeElapsedMillis"    : ["latest=(.+), original",None],
            "lastSuccessfulRunTime"         : ["Last successful run: (.+)",None],
            "lastFailedRunTime"             : ["Last failed run: (.+)",None],
        }
        # jobInfo
        self.jobInfoPropertiesRegex = {
            "service"        :   ["Service: (.+)",None],
            "isPersisted"    :   ["(PERSISTED)",None],
            "isPeriodic"     :   ["(PERIODIC:)",None],
            "intervalMills"  :   ["interval=(.+) flex",None],
            "flexMills"      :   ["flex=(.+)",None]
        }

        # ALarmPropertiesAndRegex
        # Alarm
        self.alarmPropertiesRegex = {
            "type"          :    [".*((RTC_WAKEUP)|(RTC)|(ELAPSED_REALTIME_WAKEUP)|(ELAPSED_REALTIME)).*",None],
            "origWhen"      :    ["origWhen=(.+) window",None],
            "mWhenElapsed"  :    ["whenElapsed=(.+) maxWhen",None],
            "windowLength"  :    ["window=(\\d+) ",None],
            "repeatInterval":    ["repeatInterval=(\\d+) ",None],
            "flag"          :    ["flags=(0x\\d+)",None],
            "mPackageName"  :    ["Alarm{.*\\d+ ([a-zA-Z\\.]+)}",None],
            "mMaxWhenElapsed":   ["maxWhenElapsed=(\\d+)",None],
            "requester"     :    ["requester=(\\d+) ",None],
            "app_standby"   :    ["app_standby=(\\d+) ",None]
        }

        self.mAlarmStore = []
        self.mJobStore = []



    # 清空job的属性
    def initJobProperties(self):
        # Initialize jobStatus
        for key,value in self.jobInfoPropertiesRegex.items():
            value[1] = None
        for key,value in self.jobStatusPropertiesRegex.items():
            value[1] = None
        # self.j = None
        # self.callingUid = None
        # self.sourcePackageName = None
        # self.sourceUserId = None
        # self.standbyBucket = None
        # self.tag = None
        # self.earliestRunTimeElapsedMillis = None
        # self.latestRunTimeElapsedMillis = None
        # self.lastSuccessfulRunTime = None
        # self.lastFailedRunTime = None
        #
        # # Initialize jobInfo
        # self.service = None
        # self.isPersisted = None
        # self.isPeriodic = None
        # self.intervalMills = None
        # self.flexMills = None



    # 清空alarm的属性
    def initAlarmProperties(self):
        # Initialize Alarm
        for key,value in self.alarmPropertiesRegex.items():
            value[1] = None
        # self.type = None
        # self.origWhen = None
        # self.mWhenElapsed = None
        # self.windowLength = None
        # self.repeatInterval = None
        # self.mPackageName = None

    def parseLines(self):

        # 相应段的Flag标志位
        alarmContentFlag = False
        jobContentFlag = False

        # 逐行分析
        for line in self.lines:
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
                    if(self.jobInfoPropertiesRegex['service'] is not None):
                        jobinfo = JobInfo(self.jobInfoPropertiesRegex['service'][1],self.jobInfoPropertiesRegex['isPersisted'][1],
                                      self.jobInfoPropertiesRegex['isPeriodic'][1],self.jobInfoPropertiesRegex['intervalMills'][1],
                                      self.jobInfoPropertiesRegex['flexMills'][1])
                        mJob = JobStatus(jobinfo,
                                         self.jobStatusPropertiesRegex['callingUid'][1],self.jobStatusPropertiesRegex['sourcePackageName'][1],
                                         self.jobStatusPropertiesRegex['sourceUserId'][1],self.jobStatusPropertiesRegex['standbyBucket'][1],
                                         self.jobStatusPropertiesRegex['tag'][1],self.jobStatusPropertiesRegex['earliestRunTimeElapsedMillis'][1],
                                         self.jobStatusPropertiesRegex['latestRunTimeElapsedMillis'][1],self.jobStatusPropertiesRegex['lastSuccessfulRunTime'][1],
                                         self.jobStatusPropertiesRegex['lastFailedRunTime'][1])
                        self.mJobStore.append(mJob)
                        self.initJobProperties()

                # 获取属性
                self.getJobStatusProperties(line)

            # 到达alarm段
            if alarmContentFlag:
                # 新的alarm时，将旧的job信息存储成jobStatus，随后清空属性
                if(re.match(".*((RTC_WAKEUP)|(RTC)|(ELAPSED)|(ELAPSED_WAKEUP)).*",line)):
                    if(self.alarmPropertiesRegex['origWhen'][1] is not None):
                        mAlarm = Alarm(self.alarmPropertiesRegex['type'][1],self.alarmPropertiesRegex['origWhen'][1],
                                       int(self.alarmPropertiesRegex['mWhenElapsed'][1]),self.alarmPropertiesRegex["windowLength"][1],
                                       self.alarmPropertiesRegex['repeatInterval'][1],self.alarmPropertiesRegex['flag'][1],
                                       self.alarmPropertiesRegex['mPackageName'][1],int(self.alarmPropertiesRegex['mMaxWhenElapsed'][1]),
                                       self.alarmPropertiesRegex['requester'][1],self.alarmPropertiesRegex['app_standby'][1])
                        self.mAlarmStore.append(mAlarm)
                        self.initAlarmProperties()
                # 获取属性
                self.getAlarmProperties(line)


    # 采集jobStatus的信息
    def getJobStatusProperties(self,line):
        for key,value in self.jobStatusPropertiesRegex.items():
            jobSearch = re.search(value[0],line)
            if(jobSearch):
                value[1] = jobSearch.group(1)

        for key,value in self.jobInfoPropertiesRegex.items():
            jobSearch = re.search(value[0], line)
            if (key == "isPersisted" or key == "isPeriodic"):
                if (jobSearch):
                    value[1] = True
                else:
                    value[1] = False
            else:
                if (jobSearch):
                    value[1] = jobSearch.group(1)

    # 采集alarm的信息
    def getAlarmProperties(self,line):
        for key,value in self.alarmPropertiesRegex.items():
            alarmSearch = re.search(value[0],line)
            if (alarmSearch):
                value[1] = alarmSearch.group(1)


    def getAlarmStore(self):
        return self.mAlarmStore

    def getJobStore(self):
        return self.mJobStore



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


