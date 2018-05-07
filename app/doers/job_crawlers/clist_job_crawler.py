from . import JobCrawler
from lxml import html, etree
import requests, json, sys, re, time, os.path
from clint.textui import colored

from app.models import JobProfile
from app.models import JobOpportunity
from app.services import LogService

class CListJobCrawler(JobCrawler):
    """Takes a job profile, crawls known job sources and returns a list of qualified leads."""
    TEST_CLIST_CONFIG = {
        'baseUrl': "https://nh.craigslist.org/d/jobs/search/jjj",
        'jobTitlesFile': "CListJobTitles.txt",
        'jobFile': "CListJobDetails.txt",
        'jobQuery': '//a[@class="result-title hdrlnk"]'
        }
    
    def parseCListDesc(self, jobResponse):
        CRAIGS_LIST_DESC_QUERY = '//section[@id="postingbody"]/text()'
        try:
            data = jobResponse['tree'].xpath(CRAIGS_LIST_DESC_QUERY)
            desc = data[1].replace("\n","").strip()
            self.log.show("desc: \"%s\"" % desc, "cyan")
        except IndexError: 
            desc = ""
            self.log.log("...no results from xml. \n", "yellow")
            self.log.log(str(data))
        return desc

    def parseCListResponseEmail(self,jobResponse):
        #self.log.show("taking in xml %s and html %s" % (jobResponse['tree'],jobResponse['html']), "cyan")                
        desc = self.parseCListDesc(jobResponse)
        # self.log.show("retrieved desc: \"%s\"" % desc, "cyan")        
        # Pull email from description or fetch the anonymous email if needed
        if "@" in jobResponse['desc']:
            # split = desc.split(" ")
            # email = [w for w in split if "@" in w]
            email = self.scanForEmail(desc)
        if "@" in desc and bool([True for c in dots if c in jobResponse['html']]):
            # print("in html loop...")
            # expression = re.compile(r"(\S+)@(\S+)")
            # result = expression.findall(html)
            # print("result: %s" % result)
            
            # print("email from html: %s" % (res))
            email = self.scanForEmail(html)            
        else:
            print("in else loop...")
            email = None
        
            
        return email 
    
    def buildCraigsListJobResult(self,titleDict):
        """Takes in an dict with keys [title, url] of a 
        Craig's List Job Listing and returns a dictionary
        returns {
            'title':title of job listing, 
            'url':url for job listing, 
            'timeStamp':timeStamp, 
            'prettyTimeStamp':prettytimeStamp, 
            'email':email to respond to,
            'desc':description of job,
            }
        """
        title= titleDict['title']
        url = titleDict['url']
        timeStamp = time.time()
        prettyTimeStamp = self.log.now()
        desc = self.parseCListDesc(titleDict['response'])        
        email = self.parseCListResponseEmail(titleDict['response'])

        return {
            'title':title, 
            'url':url, 
            'timeStamp':timeStamp, 
            'prettyTimeStamp':prettyTimeStamp, 
            'email':email,
            'desc':desc,
            'timeToCrawl':None
            }


    def refreshTitlesData(self, config):
        """Takes in a config<dict>, recrawls and updates 
        data in titles database.
        """
        self.log.log("refreshing titles file", "cyan")
        self.log.todo("refreshData() crawls only results that are newer than newest saved timestamp.")
        crawlstart = time.time()
        # Crawl clist url for titles.
        jobData = self.crawl(
            self.config['baseUrl'])['tree'].xpath(self.config['jobQuery'])
        self.addLog('...crawl() yielded (%s) links.' % len(jobData),"cyan")
        # Convert crawl data to lod.
        titles = [{'title':el.text_content(),'url':el.get('href')} for el in jobData] 
        self.addLog('...saving %s titles.' % len(titles), "cyan")
        # Write to json file.
        # self.saveToJsonFile(self.config['jobTitlesFile'], titles)
        self.saveTitles(titles)
        self.log.log(
            "...time to crawl, process and save titles [%s]." % (
                self.log.elapsed(crawlstart)), "cyan")
    def refreshJobsData(self,titles,n=None):
        """Takes in a list of titles and url pairs<dict>, 
        crawls urls and updates data in jobs database.
        """
        self.log.log("refreshing jobs file", "cyan")        
        jobs = []
        for e,t in enumerate(titles):
            job = {}
            crawlstart = time.time()
            t['response'] = self.crawl(t['url'])
            job = self.buildCraigsListJobResult(t)       
            job['timeToCrawl'] = self.log.elapsed(crawlstart)
            self.log.log(
                "...time to crawl, process and save match %s [%s]" % (
                    e,self.log.elapsed(crawlstart)))
            jobs.append(job)
            if n:
                if e>n: break
        self.saveJobs(jobs)
    def crawlCList(self, config=TEST_CLIST_CONFIG, searchTerms=['.']):
        """Takes in a list of search terms and returns a 
        list of job results from Craig's List
        """
        results = []
        start = time.time()
        self.log.todo("Set up git hub vc.",True)
        # if we should crawl...
        if False:
            self.refreshTitlesData(config)
            self.log.todo("Date stamp crawl jsons.")
            self.log.todo("Crawl only if file older than a specified date.")
        # Read json from file.
        titles = self.readFromJsonFile(self.config['jobTitlesFile'])['data']
        self.log.log("retrieved %s titles from file." % len(titles), "white")
        self.log.showLod("titles retrieved from file",titles, 5)

        # Search data for matches to searchTerms.
        self.log.todo("Code deep search method.")
        self.log.log("searching with searchTerms %s" % (searchTerms), "white")        
        matches = self.search([t['title'] for t in titles],searchTerms)
        self.log.log('found %s matches from %s potential.' % (len(matches),len(titles)), "white")
        self.log.showList("...matches resulting from search",matches, 5)

        # Crawl urls of matching filtered matches and build job results
        self.log.todo("crawl urls of matching filtered matches and build job results.", True)
        self.log.todo("write job results to file.", True)
        self.log.todo("job results include the email to send response to.")        
        if True:
            self.refreshJobsData(titles,5)
        jobs = self.readFromJsonFile(self.config['jobFile'])['data']
        results = []
        for job in jobs:
            if job['title'] in matches:
                results.append(job)
        self.log.log(
            'crawlCraigsList() yielded [%s] results in %s seconds.' % (
                len(results), self.log.elapsed(start)), "white") 
        self.log.showLod("results of clist crawl",results, 5)        
        
        # for k in results[0].keys():
            # assert [len(d[k]) > 0 for d in self.results]
            # self.log.log(([assert d[k] is not None for d in results]),"yellow")

        # self.log.logTodos()
        # print(self.log.dump())        
        return results  # lod  