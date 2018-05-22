from . import JobTagger
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
    TEST_JOB = ""

    tagger = JobTagger(logLevel=-1)

    def test_tagText(self):
        tags = [""]
        assert (self.tagger.tagText(self.TEST_TEXT)) == tags

    def test_tagJob(self):
        tags = [""]
        assert (self.tagger.tagJob(TEST_JOB)) == tags

    def test_tagJobs(self):
        tags = [""]
        assert self.tagger.tagJob(TEST_JOB) == tags

    def test_dumpLog(self):
        self.tagger.log.logTodos()
        print(self.tagger.log.dump())
        pass