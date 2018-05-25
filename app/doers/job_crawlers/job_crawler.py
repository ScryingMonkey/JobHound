from lxml import html, etree
import requests, json, sys, re, time, os.path
from clint.textui import colored

# from app.models import JobProfile
from app.models import JobOpportunity
from app.services import LogService

class JobCrawler:
    """Common class for holding methods useful for all crawlers.

    Utilizes lxml.xpath queries yielding HtmlElements.
    ref: https://www.w3schools.com/xml/xpath_examples.asp.
    """
    TEST_CONFIG = {
        'baseUrl': "https://nh.craigslist.org/d/jobs/search/jjj",
        'jobTitlesFile': "UnchristenedJobTitles.txt",
        'jobFile': "UnchristenedJobDetails.txt",
        'jobQuery': '//a[@class="result-title hdrlnk"]',
        'logPath': "c:/push/log_unchristened_JobCrawler.txt",
        'logLevel':1
    }
    def __init__(self, config=TEST_CONFIG):
        configKeys = ['baseUrl','jobTitlesFile','jobFile','jobQuery']
        for key in configKeys:
            if key not in config.keys():
                raise KeyError(
                    "Key [%s] is not in config keys [%s]" % (
                        key, config.keys()))
        self.config = config
        self.state = "new"
        self.content = None
        self.links = None 
        self.logLevel = config['logLevel']
        
        self.log = LogService(config['logPath'],config['logLevel'])
        self.log.startLog()

        self.log.todo("Separate out Crawler() class.", True)
        self.log.todo("Separate logging methods into the logging service.", True)
        self.log.todo("Set up Crawler() to build baseUrl to crawl multiple urls.", False)

    def crawl(self, url=""):  
        start = time.time()
        if len(url)<0: url = self.config['baseUrl']
        page = requests.get(url)
        tree = html.fromstring(page.content) 
        self.log.log(
            "...crawled [%s] in %s seconds." % (
                url, self.log.elapsed(start)), "white")
        return {"html":page.content,"tree":tree} 
    
    def searchList(self, listToSearch, searchTerms):
        start = time.time() 
        self.log.todo("Fix search().",True)        
        res = ""
        res += "...searching list of length [%s] for searchTerms [%s]. \n" % (
                len(listToSearch),searchTerms)
        # searchRegex = [re.compile(s) for s in searchTerms]
        matches = []
        for t in listToSearch:
            bools = []
            for r in searchTerms:
                b = r.lower() in t.lower()
                bools.append(b)  
            if any(bools):
                matches.append(t)  
        res += "...returning [%s] matches from a potential list of length [%s] in %s seconds. \n" % (
                len(matches),len(listToSearch),self.log.elapsed(start))
        if len(matches) < 1:
            matches = [{'oops':"No Results"}]
        self.log.log(res,"cyan")        
        return matches

    def saveTitles(self, lod):
        self.log.log(
            "...saving results of length %s."
             % len(lod),
             "cyan")
        self.saveToJsonFile(self.config['jobTitlesFile'], lod)

    def convertLoJobOppsToLod(self, LoJobbOpps):
        return [jo.toDict() for jo in LoJobbOpps]

    def saveJobs(self, lod):
        self.log.log(
            "...saving results of length %s to %s." % (
            len(lod),self.config['jobFile']),"cyan")
        self.saveToJsonFile(self.config['jobFile'], lod)

    def saveToJsonFile(self, fileName, lod):
        self.log.log(
            "...saving list of <%s> with length [%s] to file [%s]." % (
                type(lod[0]), len(lod),fileName),"cyan")
        with open(fileName,'w') as outfile:
            json.dump(lod, outfile)

    def addToJsonFile(self, outfile, lod):
        """Takes in a filename<string> and a lod.  Adds
        contents of lod to file in json format.
        """
        self.log.log(
            "...saving lod with length [%s] to file [%s]." % (
                len(lod),fileName), "white")
        outfile.append(json.dumps(lod))

    def readFromJsonFile(self, fileName):
        """Takes in a filename<string> for a json file and 
        returns a contents of file in a dict.

        returns {"data": <data from file>}
        """
        self.log.log("...reading json from file [%s]." % (fileName),"cyan")        
        try:
            with open(fileName,'r') as infile:
                data = json.load(infile)
        except IOError as e:
            try:
                filename = "./%s" % fileName
                with open(fileName,'r') as infile:
                    data = json.load(infile)
            except IOError as e:
                self.log.log("...unable to open file [%s]." % fileName, "red")
                data = {
                    "data":"...ERROR: unable to open file [%s]" % fileName, 
                    "E":"IOError"
                    }
        self.log.log("...retrieved data with length %s from [%s]." % (len(data),fileName),"cyan")                 
        return {"data":data}