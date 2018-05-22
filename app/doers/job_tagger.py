from textblob import TextBlob

from app.models import JobProfile
from app.models import JobOpportunity
from app.services import LogService

class JobTagger:

    def __init__(self, logLevel=2):
        self.logLevel = logLevel
        self.log = LogService("c:/push/log_testing_JobTagger.txt",logLevel)
        self.log.startLog()

        self.log.todo("Take in sample text and return tags", False)
        self.log.todo("Take in a job object and add tags to it.", False)
        self.log.todo("Reinsert job object into database with tags.", False)

    def getBlob(self,txt):
        return TextBlob(txt)
    def tagText(self,txt):
        blob = TextBlob(txt)
        tags = blob.tags
        self.log.log("tags:\n %s" % tags)
        return tags
    def tagJob(self,job):
        '''take in a JobOpportunity and return a
        JobOpportunities with tags attached.
        '''
        njob = JobOpportunity()
        return njob
    def tagJobs(self,path):
        '''take in a database of JobOpportunities and return
        a lod of JobOpportunities
        '''
        njobs = []
        return njobs
    def showBlob(self,blob):
        self.log.log("tags: ", blob.tags)
        self.log.log("noun phrases", printblob.noun_phrases)
        for sentence in blob.sentences:
            self.log.log(sentiment.sentiment.polarity)
        self.log.log(blob.translate(to="es"))