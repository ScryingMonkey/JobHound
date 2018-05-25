from app.doers import CListJobCrawler
from lxml import html
import timeit

class TestCListCrawler(object):
    TEST_SEARCH_TERMS = ["Developer", "Coder", "Roofing"]
    TEST_CLIST_CONFIG = {
        'baseUrl': "https://nh.craigslist.org/d/jobs/search/jjj",
        'jobTitlesFile': "CListJobTitles_NH.txt",
        'jobFile': "CListJobDetails_NH.txt",
        'jobQuery': '//a[@class="result-title hdrlnk"]',
        'logPath': "c:/push/log_testing_TestCListCrawler.txt",
        'logLevel':2
        }

    cljc = CListJobCrawler(TEST_CLIST_CONFIG)
    results = cljc.convertLoJobOppsToLod(cljc.crawlCList(TEST_SEARCH_TERMS))

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

    def test_resultJobOppContainCorrectTypes(self):        
        # 'title':title,'url':url,'xml':xml,'desc':desc
        shouldBeType = {
            'title':unicode,
            'url':unicode,
            "timestamp":float,
            "prettyTimeStamp":str,
            'email':unicode,
            'desc':unicode,
            'tags':list
            }
        # print(self.results[0])
        # for l in self.results[0].keys():
        #     print("[%s] %s" % (l,self.results[0][l]))
        for d in self.results:
            for k in shouldBeType.keys():
                b = isinstance(d[k],shouldBeType[k])
                assert k and b
        assert False not in ["http" in d['url'] for d in self.results]
        assert len(self.results) == sum(["http" in d['url'] for d in self.results])
        # assert False not in ["@" in d['email'] for d in self.results]        
        # assert len(self.results) == sum(["@" in d['email'] for d in self.results])
    
    def test_dumpLog(self):
        self.cljc.log.dump()