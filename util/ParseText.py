import re
from alarm.Alarm import *
from job.JobStatus import *


class ParseText:
    def __init__(self, lines):
        self.lines = lines
        self.mAlarmStore = []
        self.mJobStore = []

    def parse(self):
        # 相应段的Flag标志位
        alarmContentFlag = False
        jobContentFlag = False

        for line in self.lines:
            if line == "\n":
                alarmContentFlag = False
                jobContentFlag = False
            # judge arrive alarm paragraph
            line = line.lstrip()
            if not alarmContentFlag and not jobContentFlag:
                alarmContentFlag = re.search("Delivery alarm :.*",line)
                continue
            # judge arrive job paragraph
            if not jobContentFlag:
                jobContentFlag = re.search("Recently delivery jobs:.*", line)
                if (jobContentFlag):
                    alarmContentFlag = False
                    continue

            # parse alarm info
            # alarm paragraph
            if alarmContentFlag:
                policyWhenElapsed = []
                attribute = line.strip().split(',')
                type = int(attribute[0])
                when = int(attribute[1])
                requestedWhenElapsed = int(attribute[2])
                maxWhenElapsed = int(attribute[3])
                elapsedRealtime = int(attribute[4])
                enqueueTime = int(attribute[5])
                windowLength = int(attribute[6])
                # repeatInterval = int(attribute[7])
                # flags = int(attribute[8])
                # TODO: bug
                repeatInterval = int(attribute[7][:-1])
                flags = int(attribute[7][-1])
                pkg = attribute[9]
                policyWhenElapsed.append(None if attribute[11] == '/' else int(attribute[11]))
                policyWhenElapsed.append(None if attribute[12] == '/' else int(attribute[10]))
                policyWhenElapsed.append(None if attribute[13] == '/' else int(attribute[13]))
                mAlarm = Alarm(type, when, requestedWhenElapsed, maxWhenElapsed, enqueueTime, elapsedRealtime,
                               windowLength, repeatInterval, flags, pkg,
                               policyWhenElapsed[0], policyWhenElapsed[1])
                self.mAlarmStore.append(mAlarm)
            # parse job info
            # job paragraph
            if jobContentFlag:
                attribute = line.strip().split(',')
                callingUid = int(attribute[0])
                sourcePackageName = attribute[1]
                sourceUserId = int(attribute[2])
                standbyBucket = int(attribute[3])
                tag = attribute[4]
                earliestRunTimeElapsedMillis = int(attribute[5])
                latestRunTimeElapsedMills = int(attribute[6])
                lastSuccessfulRunTime = int(attribute[7])
                lastFailedRunTime = int(attribute[8])
                isPeriodic = bool(attribute[9])
                isPersisted = bool(attribute[10])
                intervalMills = int(attribute[11])
                flexMills = int(attribute[12])
                mJob = JobStatus(callingUid, sourcePackageName, sourceUserId, standbyBucket,
                                 tag, earliestRunTimeElapsedMillis, latestRunTimeElapsedMills,
                                 lastSuccessfulRunTime, lastFailedRunTime, isPersisted,
                                 isPersisted, intervalMills, flexMills)
                self.mJobStore.append(mJob)

    def get_alarm_store(self):
        return self.mAlarmStore

    def get_job_store(self):
        return self.mJobStore
