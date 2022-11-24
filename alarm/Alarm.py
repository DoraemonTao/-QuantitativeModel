class Alarm:
    # 应用的策略，我们模块暂只引入idle状态
    NUM_POLICIES = 2

    # TODO:增加idle状态下的情况

    # 策略的索引
    # 用户请求时间
    REQUESTER_POLICY_INDEX = 0
    APP_STANDBY_POLICY_INDEX = 1
    # idle状态下的索引
    DEVICE_IDLE_POLICY_INDEX = 2

    mPolicyWhenElapsed  = []

    mWhenElapsed = None
    triggerAtMillis = None
    repeatinterval = None
    # 只有wakeup类型才会唤醒设备，我们只考虑wakeup类型的alarm
    wakeup = None
    mPackageName = None
    windowMills = None
    mMaxWhenElapsed = None
    # 在策略下需要保证的执行时间
    mPolicyWhenElapsed = [0,0,0,0,0]
    def __init__(self,type,when,requestedWhenElapsed,maxWhenElapsed,enqueueTime,elapsedRealtime,windowLength,interval
        ,flags,pkgName,requester,app_standby):
        self.elapsedRealtime = elapsedRealtime;
        self.enqueueTime = enqueueTime
        self.type = type
        self.origWhen = when
        self.mWhenElapsed = requestedWhenElapsed
        self.windowLength = windowLength
        self.repeatInterval = interval
        self.flags = flags
        self.mPackageName = pkgName
        self.wakeup = type == "RTC_WAKEUP" or type == "ELAPSED_REALTIME_WAKEUP"
        self.mMaxWhenElapsed = maxWhenElapsed
        self.mPolicyWhenElapsed[self.REQUESTER_POLICY_INDEX] = requester
        self.mPolicyWhenElapsed[self.APP_STANDBY_POLICY_INDEX] = app_standby



    # 改变交付时间
    def setPolicyElapsed(self,policyIndex,policyElapsed):
        self.mPolicyWhenElapsed[policyIndex] = policyElapsed
        return self.updateWhenElapsed()

    # 返回是否改变交付时间
    def updateWhenElapsed(self):
        oldWhenElpased = self.mWhenElapsed
        mWhenElapsed = 0
        for i in range(1,self.NUM_POLICIES):
            mWhenElapsed = max(mWhenElapsed,self.mPolicyWhenElapsed[i])
        oldMaxWhenElapsed = self.mMaxWhenElapsed
        maxRequestedElapsed = self.mPolicyWhenElapsed[self.REQUESTER_POLICY_INDEX] + self.windowLength
        self.mMaxWhenElapsed = max(maxRequestedElapsed,mWhenElapsed)

        return (oldWhenElpased is not self.mWhenElapsed) or (oldMaxWhenElapsed is not self.mMaxWhenElapsed)



    def getWhenElapsed(self):
        return self.mWhenElapsed

    def getMaxWhenElapsed(self):
        return self.mMaxWhenElapsed

    def getFlag(self):
        return self.flags


