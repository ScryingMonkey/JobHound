from . import CListJobCrawler
from lxml import html
import timeit

class TestCListCrawler(object):
    TEST_SEARCH_TERMS = ["Developer", "Coder", "Roofing"]
    TEST_CLIST_CONFIG = {
        'baseUrl': "https://nh.craigslist.org/d/jobs/search/jjj",
        'jobTitlesFile': "CListJobTitles.txt",
        'jobFile': "CListJobDetails.txt",
        'jobQuery': '//a[@class="result-title hdrlnk"]'
        }

    cljc = CListJobCrawler(TEST_CLIST_CONFIG, -1)
    results = cljc.crawlCList(TEST_SEARCH_TERMS)

    def test_crawlCraigsList(self):     
        assert isinstance(self.results,list)
        assert isinstance(self.results[0],dict)
        assert len(self.results[0]) == 7

    def test_allDictKeysHaveValues(self):
        keys = self.results[0].keys()
        assert False not in [
            [True for k in keys if d[k] is not None] 
                for d in self.results]
    
    def test_jobTitlesFile(self):
        jfile = self.cljc.config['jobTitlesFile']
        data = self.cljc.readFromJsonFile(jfile)['data']
        assert len(data) > 0
    
    def test_jobDetailsFile(self):
        jfile = self.cljc.config['jobFile']
        data = self.cljc.readFromJsonFile(jfile)['data']
        assert len(data) > 0

    def test_resultDictsContainCorrectTypes(self):        
        # 'title':title,'url':url,'xml':xml,'desc':desc
        shouldBeType = {
            'title':unicode,
            'url':unicode,
            "timeStamp":float,
            "prettyTimeStamp":unicode,
            'email':unicode,
            'desc':unicode,
            }
        for k in shouldBeType.keys():
            assert k and False not in [isinstance(d[k],shouldBeType[k]) for d in self.results]

        assert False not in ["http" in d['url'] for d in self.results]
        assert False not in ["@" in d['email'] for d in self.results]
        assert len(self.results) == sum(["http" in d['url'] for d in self.results])
        assert len(self.results) == sum(["@" in d['email'] for d in self.results])
    
    # def test_dumpLog(self):
    #     self.cljc.log.logTodos()
    #     print(self.cljc.log.dump())