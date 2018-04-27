from app.doers import JobCrawler
from lxml import html
import timeit

class TestCrawler(object):
    TEST_SEARCH_TERMS = ["Developer","Coder"]
    TEST_CONFIG= {
            'baseUrl': "https://nh.craigslist.org/d/jobs/search/jjj",
            'jobTitlesFile': "CListJobTitles.txt",
            'jobDetailsFile': "CListJobDetails.txt",
            'jobQuery': '//a[@class="result-title hdrlnk"]'
        }

    jc = JobCrawler(TEST_CONFIG)
    # jc = JobCrawler(config=TEST_CONFIG)
    data = jc.crawl(jc.config['baseUrl'])

    def test_saveToJsonFile(self):
        TEST_FILE_FROM_CODE = "./test_file_from_code.txt"
        TEST_LOD = [
            {"name": "l1", "l": [1,2,3,4]},
            {"name": "l2", "l": [5,6,7,8]},
            {"name": "l3", "l": [9,10,11,12]}
            ]
        self.jc.saveToJsonFile(TEST_FILE_FROM_CODE, TEST_LOD)
        dataFromFile = self.jc.readFromJsonFile(TEST_FILE_FROM_CODE)['data']
        assert type(dataFromFile) == list
        assert len(dataFromFile) == 3
        assert len(dataFromFile[2]) == 2
        assert dataFromFile[1]['name'] == 'l2'
        assert dataFromFile[0]['l'][0] == 1
        assert dataFromFile[2]['l'][2] == 11

    def test_readFromJsonFile(self):
        TEST_FILE = "./test_file.txt"   
        # {
        #   "test string": "test stringtest stringtest string", 
        #   "test list": [
        #       "(0) First line", 
        #       "(1) Second line", 
        #       "(2) Third line", 
        #       "(3) Second line"
        #       ]
        #   }     
        rawdata = self.jc.readFromJsonFile(TEST_FILE)
        dataFromFile = rawdata['data']
        assert type(rawdata) == dict
        assert type(dataFromFile) == dict
        assert len(dataFromFile.keys()) == 2
        assert dataFromFile['test string'] == "test stringtest stringtest string"
        assert dataFromFile['test list'][1] == "(1) Second line"

    def test_crawl(self):
        assert len(self.data) == 2
        assert isinstance(self.data['html'],str)
        assert isinstance(self.data['tree'],html.HtmlElement)

    def test_crawlData(self):
        links = self.data['tree'].xpath(self.jc.config['jobQuery'])
        assert len(links) > 0
        assert len([x.text_content() for x in links]) == len([x.get('href') for x in links])

    def test_crawlTime(self):
        t = "JobCrawler().crawl('%s')" % (self.jc.config['baseUrl'])
        timeForCrawl = timeit.timeit(t, setup="from app.doers import JobCrawler", number=1)
        assert timeForCrawl < 1

    def test_searchOnDummyData(self):
        dummyData = ['Paving Specialist', 'Health Services Specialist', 'Web Developer', 'Day Laborer', 'REalestate developer']
        dummySearchTerms = ['Developer', 'Coder']
        matches = self.jc.search(dummyData, dummySearchTerms)
        assert len(matches) == 2
        assert matches == ['Web Developer', 'REalestate developer']
    
    def test_searchTimeOnDummyData(self):
        dummyData = ['Paving Specialist', 'Health Services Specialist', 'Web Developer', 'Day Laborer', 'REalestate developer']
        dummySearchTerms = ['Developer', 'Coder']
        t = "JobCrawler().search(%s,%s)" % (dummyData,dummySearchTerms)
        timeElapsed = timeit.timeit(
            t, setup="from app.doers import JobCrawler", number=1)
        assert timeElapsed < 1
        
    def test_searchOnLiveData(self):
        pass


    
class TestCraigsListCrawler(object):
    TEST_SEARCH_TERMS = ["Developer", "Coder", "Roofing"]
    TEST_CONFIG= {
            'baseUrl': "https://nh.craigslist.org/d/jobs/search/jjj",
            'jobTitlesFile': "CListJobTitles.txt",
            'jobDetailsFile': "CListJobDetails.txt",
            'jobQuery': '//a[@class="result-title hdrlnk"]'
        }

    jc = JobCrawler(TEST_CONFIG)
    results = jc.crawlCList(TEST_SEARCH_TERMS)

    def test_crawlCraigsList(self):     
        assert isinstance(self.results,list)
        assert isinstance(self.results[0],dict)
        assert len(self.results[0]) == 4

    def test_allDictKeysHaveValues(self):
        for k in self.results[0].keys():
            assert [len(d[k]) > 0 for d in self.results]
    
    def test_jobTitlesFile(self):
        jfile = self.jc.config['jobTitlesFile']
        data = self.jc.readFromJsonFile(jfile)['data']
        assert len(data) > 0
    
    def test_jobDetailsFile(self):
        jfile = self.jc.config['jobDetailsFile']
        data = self.jc.readFromJsonFile(jfile)['data']
        assert len(data) > 0

    def test_resultDictsContainCorrectTypes(self):        
        # 'title':title,'url':url,'xml':xml,'desc':desc
        assert len(self.results) == sum([isinstance(d['title'],str) for d in self.results])
        assert len(self.results) == sum([isinstance(d['url'],str) for d in self.results])
        assert len(self.results) == sum(["http" in d['url'] for d in self.results])
        assert len(self.results) == sum([isinstance(d['xml'],html.HtmlElement) for d in self.results])
        assert len(self.results) == sum([isinstance(d['desc'],str) for d in self.results])
    
    def test_dumpLog(self):
        print(self.jc.getLog())


