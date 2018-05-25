from lxml import html, etree
import requests, json, sys, re, time, os.path
from clint.textui import colored
from selenium import webdriver

from . import JobCrawler
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
            #self.log.show("desc: \"%s\"" % desc, "cyan")
        except IndexError: 
            desc = ""
            self.log.log("...no results from xml. \n", "yellow")
            self.log.log(str(data))
        return desc
    
    def parseCListResponseEmail(self, jobResponse):
        desc = self.parseCListDesc(jobResponse)
        email = JobOpportunity().scanTextForEmail(desc) 
        if (email):
            self.log.log("...returning email [%s]" % email, "cyan") 
        else:
            self.log.log("...did not find an email in desc.", "cyan")  
            email = "" 
        return email

    def buildCraigsListJobOpportunity(self,titleDict):
        """Takes in an dict with keys [title, url] of a 
        Craig's List Job Listing and returns a JobOpportunity object
        returns JobOpportunity

          .title: Title of job posting.  
          .url: Url where job was collected.  
          .timestamp: Time that job was collected in seconds from epoch.  
          .prettyTimeStamp: Formatted timestamp. 'May222018_19:59:38'   
          .email: Email to respond to job opportunity.  
          .desc: Description of job.  
          .tags: Meta tags generated from job data.            
        """
        self.log.log("...building job result.", "cyan")
        title= titleDict['title']
        url = titleDict['url']
        timeStamp = time.time()
        desc = self.parseCListDesc(titleDict['response'])       

        jobOpp = JobOpportunity()
        jobOpp.config({
            'title':title, 
            'url':url, 
            'timestamp':timeStamp,
            'desc':desc
            })
        return jobOpp


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
        self.log.log('...crawl() yielded (%s) links.' % len(jobData),"cyan")
        # Convert crawl data to lod.
        titles = [{'title':el.text_content(),'url':el.get('href')} for el in jobData] 
        self.log.log('...saving %s titles.' % len(titles), "cyan")
        # Write to json file.
        # self.saveToJsonFile(self.config['jobTitlesFile'], titles)
        self.saveTitles(titles)
        self.log.log(
            "...time to crawl, process and save titles [%s]." % (
                self.log.elapsed(crawlstart)), "cyan")
    def refreshJobsData(self, titles, n=None):
        """Takes in a list of titles and url pairs<dict>, 
        crawls urls and updates data in jobs database.
        """
        self.log.log("..refreshing jobs file", "cyan")        
        jobs = []
        for e,t in enumerate(titles):
            job = JobOpportunity()
            crawlstart = time.time()
            t['response'] = self.crawl(t['url'])
            job = self.buildCraigsListJobOpportunity(t)       
            job.timeToCrawl = self.log.elapsed(crawlstart)
            self.log.log(
                "...time to crawl, process and save match %s [%s]" % (
                    e,self.log.elapsed(crawlstart)),"cyan")
            jobs.append(job)
            if n:
                if e>n: break
        self.log.todo("Parse email from listing", False)
        jlod = self.convertLoJobOppsToLod(jobs)
        self.log.showLod("Jobs",jlod,10)
        self.saveJobs(jlod)

    def clickButton(self):
        driver = webdriver.Firefox()
        driver.get(url)
        driver.find_element_by_class_name("reply_button").click()
        driver.find_element_by_class_name("anonemail").text
        driver.close()


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
        self.log.log("Retrieved %s titles from file." % len(titles), "white")
        self.log.showLod("titles retrieved from file",titles, 5)

        # Search data for matches to searchTerms.
        self.log.todo("Code deep search method.")
        self.log.log("searching with searchTerms %s" % (searchTerms), "white")        
        matches = self.searchList([t['title'] for t in titles],searchTerms)
        self.log.log('Found %s matches from %s potential.' % (len(matches),len(titles)), "white")
        self.log.log("...matches: %s" % matches, "cyan")
        self.log.showList("...matches resulting from search",matches)

        # Crawl urls of matching filtered matches and build job results
        self.log.todo("crawl urls of matching filtered matches and build job results.", True)
        self.log.todo("write job results to file.", True)
        self.log.todo("job results include the email to send response to.")  
        # if we should crawl      
        if False:
            self.refreshJobsData(titles,10)
        self.log.log("Retrieving jobs from file.", "white")
        jobJsons = self.readFromJsonFile(self.config['jobFile'])['data']
        jobs = []
        for jobJson in jobJsons:
            j = JobOpportunity()
            j.config(jobJson)
            jobs.append(j)

        self.log.log("Retrieved %s jobs from file." % len(jobs), "white")    

        results = []
        self.log.log('Matching jobs against matches.', "white")
        self.log.showList("Matches",matches, len(matches))
        for job in jobs:
            if job.title in matches:
                self.log.log('"...(+)found for "%s" in matches.' % (job.title), "cyan")
                results.append(job)
            else:
                pass
                # self.log.log('...(-)did not find "%s" in matches.' % (job['title']), "cyan")                
        self.log.log('Matched %s jobs against matches.' % len(results), "white")
        
        self.log.log(
            'CListJobCrawler.crawlCraigsList() yielded [%s] results in %s seconds.' % (
                len(results), self.log.elapsed(start)), "white") 
        self.log.showLod("results of clist crawl",self.convertLoJobOppsToLod(results), 5)        
        
        # for k in results[0].keys():
            # assert [len(d[k]) > 0 for d in self.results]
            # self.log.log(([assert d[k] is not None for d in results]),"yellow")

        # self.log.logTodos()
        # print(self.log.dump())        
        return results  # lod  