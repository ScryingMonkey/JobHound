from textblob import TextBlob
#http://textblob.readthedocs.io/en/dev/quickstart.html

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
        tags = ""
        # self.log.log("tags:\n %s" % ([b[0] for b in blob.tags]), "white")
        # self.log.log("noun_phrases:\n %s" % (blob.noun_phrases), "white")
        # self.log.log("sentiment:\n %s" % (str(blob.sentiment)), "white")
        # self.log.log("sentiment.polarity: %s\n" % (blob.sentiment.polarity), "white")
        # self.log.log("sentiment.subjectivity: %s\n" % (blob.sentiment.subjectivity), "white")

        # self.log.log(".words:\n %s" % (blob.words))
        # self.log.log(".words.singularlize: %s\n" % blob.words.singularize(), "white")
        # self.log.log(".words.lemmatize: %s\n" % blob.words.lemmatize(), "white")
        
        # self.log.log("sentence (subjectivity(), polarity()):\n", "white")
        # for s in blob.sentences:
        #     self.log.log("%s (%s, %s)" % (
        #         s, s.sentiment.subjectivity, s.sentiment.polarity), 
        #         "white")
        POSkeepers = ["NN","NNS","NNP", "NNPS", ""]
        trash = ["TO","DT","IN","CC"]
        tags = [t[0] for t in blob.tags if t[1] not in trash]
        self.log.log("...returning tags:\n%s\n" % tags, "white")        
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