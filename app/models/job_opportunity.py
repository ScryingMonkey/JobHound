        # potential job oppotunity states = [
        #   "new", 
        #   "ready to apply", 
        #   "waiting first response", 
        #   "in correspondance", 
        #   "ready to schedule interview", 
        #   "waiting for interview", 
        #   "closed"
        # ]

import time
from textblob import TextBlob
# from app.doers.job_tagger import JobTagger

class JobOpportunity():
    """Represents an individual job position and it's relevant details.  
      
    .title: Title of job posting.  
    .url: Url where job was collected.  
    .timestamp: Time that job was collected in seconds from epoch.  
    .prettyTimeStamp: Formatted timestamp. 'May222018_19:59:38'   
    .email: Email to respond to job opportunity.  
    .desc: Description of job.  
    .tags: Meta tags generated from job data.      
    """
    def __init__(self):
        self.title = ""
        self.url = ""
        self.timestamp = ""
        self.prettyTimeStamp = ""
        self.email = ""
        self.desc = ""
        self.tags = []

    def config(self,d):
        """Takes a dict and sets fields on JobOpportunity.
        Config should have at least the following 
        fields: [url, title, timestamp, and desc]
        If you have them, you can include [email,
        tags,timeToCrawl], otherwise they will be 
        generated from the required fields.
        """
        keys = d.keys()
        self.url = d['url']
        self.title = d['title']
        self.timestamp = d['timestamp']
        self.prettyTimeStamp = str(
            time.strftime("%b%d%Y_%H:%M:%S", time.localtime(d['timestamp'])))        
        self.desc = d['desc']
        if('email' in keys):
            self.email = d['email']
        else:
            self.email = self.scanTextForEmail(d['desc'])
        if('tags' in keys):
            self.tags = d['tags']
        else:
            self.tags = self.createTags(d['title']+d['desc'])
        if('timeToCrawl' in keys):
            self.timeToCrawl = d['timeToCrawl']
        else:
            self.timeToCrawl = None
    def scanTextForEmail(self,text):
        # DOM_FILE = "topLevelDomains.txt"
        # doms = self.readFromJsonFile(DOM_FILE)['data']
             
        # Pull email from description or fetch the anonymous email if needed.
        syms = ["@","."]
        cons = [
            (lambda x: all(c in x for c in syms)),
            (lambda x: "." in x and len(x)-(1+x.index("."))<4)
        ]
        res = [w for w in text.split(" ") if all(c(w) for c in cons)]
        return ", ".join(res)
    # def scanForEmail(self,txt):
    #     DOM_FILE = "./apps/doers/job_crawlers/topLevelDomains.txt"
    #     doms = self.readFromJsonFile(DOM_FILE)['data']
    #     nonalpha = ["<",">"]
    #     res = []
    #     buffer = ""
    #     for c in txt:
    #         if "@" in buffer and bool([True for c in doms if c in txt]):
    #             res.append(buffer)
    #             buffer = ""
    #         elif c in nonalpha:
    #             buffer = ""
    #         else:
    #             buffer += c
    #     return res
    def createTags(self,text):
        blob = TextBlob(text)
        POSkeepers = ["NN","NNS","NNP", "NNPS", ""]
        trash = ["TO","DT","IN","CC"]
        tags = [t[0] for t in blob.tags if t[1] not in trash]     
        return tags
    def __iter__(self):
        yield 'title', self.title
        yield 'url', self.url
        yield 'timestamp', self.timestamp
        yield 'prettyTimeStamp', self.prettyTimeStamp
        yield 'email', self.email
        yield 'desc', self.desc
        yield 'tags', self.tags
    def toDict(self):
        return {
            'title': self.title,
            'url': self.url,
            'timestamp': self.timestamp,
            'prettyTimeStamp': self.prettyTimeStamp,
            'email': self.email,
            'desc': self.desc,
            'tags': self.tags
        }