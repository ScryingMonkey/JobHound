from . import JobTagger
from app.models.job_opportunity import JobOpportunity
import timeit

class TestJobTagger(object):
    TEST_TEXT = '''
The titular threat of The Blob has always struck me as the ultimate movie
monster: an insatiably hungry, amoeba-like mass able to penetrate
virtually any safeguard, capable of--as a doomed doctor chillingly
describes it--"assimilating flesh on contact.
Snide comparisons to gelatin be damned, it's a concept with the most
devastating of potential consequences, not unlike the grey goo scenario
proposed by technological theorists fearful of
artificial intelligence run rampant.
'''
    TEST_TAGS = ['titular', 'threat', 'Blob', 'has', 'always', 'struck', 
    'me', 'ultimate', 'movie', 'monster', 'insatiably', 'hungry', 
    'amoeba-like', 'mass', 'able', 'penetrate', 'virtually', 'safeguard', 
    'capable', 'doomed', 'doctor', 'chillingly', 'describes', 'it', 
    'assimilating', 'flesh', 'contact', 'Snide', 'comparisons', 'gelatin', 
    'be', 'damned', 'it', "'s", 'concept', 'most', 'devastating', 'potential', 
    'consequences', 'not', 'grey', 'goo', 'scenario', 'proposed', 
    'technological', 'theorists', 'fearful', 'artificial', 'intelligence', 
    'run', 'rampant']
    
    TEST_JOB_CONFIG = {
        "title": "Full Time", 
        "url": "https://nh.craigslist.org/lab/d/full-time/6572575525.html", 
        "timestamp": 1526959125.392, 
        "timeToCrawl": 0.43599987030029297, 
        "prettyTimeStamp": "May212018_23:18:45", 
        "email": None, 
        "desc": "We are taking applications for a full time, year round, custodial position, in a school setting."
        }
    TEST_JOB = JobOpportunity(TEST_JOB_CONFIG)
    TEST_JOB_TAGS = ['Full', 'TimeWe', 'are', 'taking', 'applications', 'full', 
    'time', 'year', 'round', 'custodial', 'position', 'school', 'setting']

    tagger = JobTagger(logLevel=-1)

    def test_tagText(self):
        assert (self.tagger.tagText(self.TEST_TEXT)) == self.TEST_TAGS

    def test_tagJob(self):
        assert (self.tagger.tagJob(self.TEST_JOB.title + self.TEST_JOB.desc).tags) == self.TEST_JOB_TAGS
    
    def test_tagsFromJobOpportunity(self):
        assert self.TEST_JOB.tags == self.TEST_JOB_TAGS

    def test_dumpLog(self):
        self.tagger.log.logTodos()
        print(self.tagger.log.dump())
        pass