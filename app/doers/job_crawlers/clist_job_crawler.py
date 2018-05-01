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
    
    def buildCraigsListJobResult(self,titleDict):
        """Takes in an dict with keys [title, url] of a Craig's List Job Listing and returns a dictionary"""
        CRAIGS_LIST_DESC_QUERY = '//section[@id="postingbody"]/text()'
        title= titleDict['title']
        url = titleDict['url']
        xml = titleDict['xml']

        try:
            data = xml.xpath(CRAIGS_LIST_DESC_QUERY)
            body = data[1].replace("\n","").strip()
        except IndexError: 
            body = ""
            self.log.log("...no results from xml. \n", "yellow")
            self.log.log(str(data))
        
        desc = body        
        
        # print "..."
        # print body
        # print "..."

        return {
            'title':title,'url':url,'desc':desc
            }

    def refreshData(self, config):
        self.log.todo("refreshData() crawls only results that are newer than newest saved timestamp.")
        crawlstart = time.time()
        # Crawl clist url for titles.
        jobData = self.crawl(
            self.config['baseUrl'])['tree'].xpath(self.config['jobQuery'])
        self.addLog('...crawl() yielded (%s) links.' % len(jobData),"gray")
        # Convert crawl data to lod.
        titles = [{'title':el.text_content(),'url':el.get('href')} for el in jobData] 
        self.addLog('...saving %s titles.' % len(titles), "gray")
        # Write to json file.
        # self.saveToJsonFile(self.config['jobTitlesFile'], titles)
        self.saveTitles(titles)
        self.log.log(
            "...time to crawl, process and save titles [%s]." % (
                self.log.elapsed(crawlstart)), "gray")

    def crawlCList(self, config=TEST_CLIST_CONFIG, searchTerms=['.']):
        """Takes in a list of search terms and returns a list of job results from Craig's List"""
        results = []
        start = time.time()
        self.log.todo("Set up git hub vc.",True)
        # if we should crawl...
        if False:
            self.refreshData(config)
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
        self.log.todo("crawl urls of matching filtered matches and build job results.")
        self.log.todo("write job results to file.")
        if True:
            jobs = []
            for e,t in enumerate(titles):
                job = {}
                crawlstart = time.time()
                t['xml'] = self.crawl(t['url'])['tree']
                job = self.buildCraigsListJobResult(t)                
                timeToCrawl = self.log.elapsed(start)
                job['timeToCrawl'] = timeToCrawl
                self.log.log(
                    "...time to crawl, process and save match %s [%s]" % (
                        e,self.log.elapsed(crawlstart)))
                jobs.append(job)
                # if e>5: break
            self.saveJobs(jobs)
        jobs = self.readFromJsonFile(self.config['jobFile'])['data']
        results = []
        for job in jobs:
            if job['title'] in matches:
                results.append(job)
        self.log.log(
            'crawlCraigsList() yielded [%s] results in %s seconds.' % (
                len(results), self.log.elapsed(start)), "white") 
        self.log.showLod("results of clist crawl",results, 5)        
        
        self.log.logTodos()
        # print(self.log.dump())        
        return results    