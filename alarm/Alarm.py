class Alarm:
    # 应用的策略，我们模块暂只引入idle状态
    NUM_POLICIES = 1

    # 策略的索引
    # idle状态下的索引
    DEVICE_IDLE_POLICY_INDEX = 0

    mWhenElapsed = None
    triggerAtMillis = None
    repeatinterval = None
    # 只有wakeup类型才会唤醒设备，我们只考虑wakeup类型的alarm
    wakeup = None
    mPackageName = None
    windowMills = None
    mMaxWhenElapsed = None
    # 在策略下需要保证的执行时间
    mPolicyWhenElapsed = []
    def __init__(self,type,when,requestedWhenElapsed,windowLength,interval
        ,uid,pkgName):
        self.type = type
        self.origWhen = when
        self.mWhenElapsed = requestedWhenElapsed
        self.windowLength = windowLength
        self.repeaIinterval = interval
        self.uid = uid
        self.mPackageName = pkgName
        self.wakeup = type == "RTC_WAKEUP" or type == "ELAPSED_REALTIME_WAKEUP"


    def getWhenElapsed(self):
        return self.mWhenElapsed

    def getMaxWhenElapsed(self):
        return self.mMaxWhenElapsed

    #
    def updateWhenElapsed(self):
        oldWhenElapsed = self.mWhenElapsed
        self.mWhenElapsed = 0
        for i in self.NUM_POLICIES:
            self.mWhenElapsed = max(self.mWhenElapsed,self.mPolicyWhenElapsed[i])

        return oldWhenElapsed != self.mWhenElapsed



