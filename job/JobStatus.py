class JobStatus:
    def __init__(self,
                 job,
                 callingUid,
                 sourcePackageName,
                 sourceUserId,
                 standbyBucket,
                 tag,
                 earliestRunTimeElapsedMillis,
                 latestRunTimeElapsedMillis,
                 lastSuccessfulRunTime,
                 lastFailedRunTime,
                 ):
        self.job = job
        self.calling = callingUid
        self.standbyBucket = standbyBucket

        self.sourceUserId = sourceUserId
        self.sourceTag = tag

        self.earliestRunTimeElapsedMillis = earliestRunTimeElapsedMillis
        self.latestRunTimeElapsedMillis = latestRunTimeElapsedMillis
        self.mOriginalLatestRunTimeElapsedMillis = latestRunTimeElapsedMillis
        self.sourcePackageName = sourcePackageName

        self.mLastSuccessfulRunTime = lastSuccessfulRunTime
        self.mLastFailedRunTime = lastFailedRunTime

