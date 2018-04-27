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
        'jobDetailsFile': "CListJobDetails.txt",
        'jobQuery': '//a[@class="result-title hdrlnk"]'
    }
    
    def buildCraigsListJobResults(self,titleDict):
        """Takes in an HTMLELement of a Craig's List Job Listing and returns a dictionary"""
        start = time.time()
        CRAIGS_LIST_DESC_QUERY = '//section[@id="postingbody"]/text()'
        title= titleDict['title']
        url = titleDict['url']
        xml = self.crawl(url)['tree']
        desc = xml.xpath(CRAIGS_LIST_DESC_QUERY)[1].replace("\n","").strip()
        elapsed = self.timeElapsed("buildCraigsListJobResults(jobElement)", start)
        return {
            'title':title,'url':url,'xml':xml,'desc':desc
            }

    def crawlCList(self, config=TEST_CLIST_CONFIG, searchTerms=['.']):
        """Takes in a list of search terms and returns a list of job results from Craig's List"""
        results = []
        start = time.time()
        self.todo("Set up git hub vc.",True)
        # if we should crawl...
        if False:
            # Crawl clist url for titles.
            self.todo("Date stamp crawl jsons.")
            self.todo("Crawl only if file older than a specified date.")
            jobData = self.crawl(
                self.config['baseUrl'])['tree'].xpath(self.config['jobQuery'])
            self.addLog('...crawl() yielded (%s) links.' % len(jobData))
            # Convert crawl data to lod.
            titles = [{'title':el.text_content(),'url':el.get('href')} for el in jobData] 
            self.addLog('titles length (%s).' % len(titles))
            # Write to json file.
            self.saveToJsonFile(self.config['jobTitlesFile'], titles)
            titles = []
        else:
            # Read json from file.
            titles = self.readFromJsonFile(self.config['jobTitlesFile'])['data']
            self.addLog("retrieved %s titles from file." % len(titles))
            self.showLod("titles retrieved from file",titles, 5)

        self.addLog("searching with searchTerms %s" % (searchTerms))
        # Search data for matches to searchTerms.
        matches = self.search([t['title'] for t in titles],searchTerms)
        self.addLog('found %s matches from %s potential.' % (len(matches),len(titles)))
        self.showList("...matches resulting from search",matches, 5)

        self.todo("crawl urls of matching filtered matches and build job results.")
        self.todo("write job results to file.")
        self.todo("Code deep search method.")
        # Crawl urls of matching filtered matches and build job results
        if True:

            self.saveToJsonFile(self.config['jobTitlesFile'], titles)
        # results = []
        # for i,t in enumerate(titles):
        #     if t['title'] in matches:
        #         results.append(self.buildCraigsListJobResults(t['url']))
        # self.addLog('crawlCraigsList() yielded (%s) results.' % len(results)) 
        elapsed = self.timeElapsed("crawlCraigsList(%s)" % (searchTerms), start)    
        self.logTodos()
        return results    