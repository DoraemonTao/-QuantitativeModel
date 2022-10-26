class JobStatus:
    def __init__(self,
                 job,
                 callingUid,
                 sourcePackageName,
                 sourceUserId,
                 standbyBucket,
                 tag,
                 numFailures,
                 earliestRunTimeElapsedMillis,
                 latestRunTimeElapsedMillis,
                 lastSuccessfulRunTime,
                 lastFailedRunTime,
                 internalFlags,
                 dynamicConstraints
                 ):
        self.job = job
        self.calling = callingUid
        self.standbyBucket = standbyBucket

        self.sourceUserId = sourceUserId
        self.sourceTag = tag

        self.earliestRunTimeElapsedMillis = earliestRunTimeElapsedMillis
        self.latestRunTimeElapsedMillis = latestRunTimeElapsedMillis
        self.mOriginalLatestRunTimeElapsedMillis = latestRunTimeElapsedMillis
        self.numFailures = numFailures
        self.sourcePackageName = sourcePackageName

        self.mLastSuccessfulRunTime = lastSuccessfulRunTime
        self.mLastFailedRunTime = lastFailedRunTime

        self.mInternalFlags = internalFlags

        self.dynamicConstraints = dynamicConstraints
        self.dynamicConstraints = dynamicConstraints