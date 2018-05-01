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

    cljc = CListJobCrawler(TEST_CLIST_CONFIG)
    results = cljc.crawlCList(TEST_SEARCH_TERMS)

    def test_crawlCraigsList(self):     
        assert isinstance(self.results,list)
        assert isinstance(self.results[0],dict)
        assert len(self.results[0]) == 4

    def test_allDictKeysHaveValues(self):
        for k in self.results[0].keys():
            assert [len(d[k]) > 0 for d in self.results]
    
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
        assert len(self.results) == sum([isinstance(d['title'],str) for d in self.results])
        assert len(self.results) == sum([isinstance(d['url'],str) for d in self.results])
        assert len(self.results) == sum(["http" in d['url'] for d in self.results])
        assert len(self.results) == sum([isinstance(d['xml'],html.HtmlElement) for d in self.results])
        assert len(self.results) == sum([isinstance(d['desc'],str) for d in self.results])
    
    # def test_dumpLog(self):
    #    print(self.cljc.log.dump())