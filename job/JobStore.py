class JobStore():
    def __init__(self):
        self.mJobSet = JobSet()

    def add(self,job):
        self.mJobSet.add(job)

    def remove(self,job):
        self.mJobSet.remove(job)

class JobSet():
    def __init__(self):
        self.mJobs = {}
        self.mJobsPerSourceUid = {}

    def add(self,job):
        uid = job.callingUid
        sourceUid = job.sourceUserId
        jobs = self.mJobs.get(str(uid))
        if jobs is None:
            jobs = []
            self.mJobs[str(uid)] = jobs
        jobsForSourceUid = self.mJobsPerSourceUid.get(str(sourceUid))
        if jobsForSourceUid is None:
            jobsForSourceUid = []
            self.mJobsPerSourceUid[str(sourceUid)] = jobsForSourceUid

        added = jobs.append(job)
        added = jobsForSourceUid.append(job)

    def size(self):
        return len(self.mJobs)

    def remove(self,job):
        uid = job.callingUid
        jobs = self.mJobs.get(str(uid))
        sourceId = job.sourceUserId
        jobsForSourceUid = self.mJobsPerSourceUid.get(str(sourceId))
        didRemove = jobs != None and jobs.remove(job)
        sourRemove = jobsForSourceUid != None and jobsForSourceUid.remove(job)
        if didRemove or sourRemove:
            if(jobs != None and len(jobs) == 0):
                del self.mJobs[str(uid)]
                self.mJobs.pop(str(uid))
            if(jobsForSourceUid != None and len(jobsForSourceUid) == 0):
                self.mJobsPerSourceUid.pop(str(sourceId))
            return True
        return False

    def getAllJobs(self):
        allJobs = []
        for uid,jobs in self.mJobs.items():
            if jobs != None:
                for j in range(len(jobs)):
                    allJobs.append(jobs[j])
        return allJobs