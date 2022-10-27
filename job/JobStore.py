class JobStore():
    def __init__(self):
        self.mJobSet = JobSet()

    def add(self,job):
        self.mJobSet.add(job)

class JobSet():
    def __init__(self):
        self.mJobs = []

    def add(self,job):
        self.mJobs.append(job)

    def size(self):
        return len(self.mJobs)

