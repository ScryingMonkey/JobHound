from lxml import html, etree
import requests, json, sys, re, time, os.path
from clint.textui import colored

from app.models import JobProfile
from app.models import JobOpportunity
from app.services import LogService

class JobCrawler:
    """Common class for holding methods useful for all crawlers.

    Utilizes lxml.xpath queries yielding HtmlElements.
    ref: https://www.w3schools.com/xml/xpath_examples.asp.
    """
    TEST_CONFIG = {
        'baseUrl': "https://nh.craigslist.org/d/jobs/search/jjj",
        'jobTitlesFile': "CListJobTitles.txt",
        'jobDetailsFile': "CListJobDetails.txt",
        'jobQuery': '//a[@class="result-title hdrlnk"]'
    }
    def __init__(self, config=TEST_CONFIG, logLevel=-1 ):
        configKeys = ['baseUrl','jobTitlesFile','jobDetailsFile','jobQuery']
        for key in configKeys:
            if key not in config.keys():
                raise KeyError("config dictionary is missing key [%s]" % key)
        self.config = config
        self.state = "new"
        self.content = None
        self.links = None 
        self.logLevel = logLevel
        
        self.LOG = "\n\n[starting log : %s] \n" % time.strftime("%H:%M:%S")
        self.todos = []

        self.todos.append(colored.green("\n[X] Separate out Crawler() class."))
        self.todos.append(colored.yellow("\n[ ] Set up Crawler() to build baseUrl to crawl multiple urls.")  + "/n")

    def todo(self,s,b=False):
        if b:
            s = colored.green("\n[X] %s" % s)
        else:
            s = colored.yellow("\n[ ] %s" % s)
        self.todos.append(s)
    
    def logTodos(self):
        res = colored.yellow("\n\nTODOS: \n")
        for t in self.todos:
            res += t
        self.addLog(res)
    
    # def queryXpath(self, xpathO,query):
    #     return xpathO.xpath(query)

    def crawl(self, url=""):  
        start = time.time()
        if len(url)<0: url = self.url
        page = requests.get(url)
        tree = html.fromstring(page.content) 
        elapsed = self.timeElapsed("crawl(url)", start)
        self.addLog("...crawled [%s] in %s seconds." % (url,elapsed))
        return {"html":page.content,"tree":tree} 
    
    def search(self, listToSearch, searchTerms):
        start = time.time() 
        self.todo("Fix search().",True)        
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
        elapsed = self.timeElapsed("search(listToSearch,searchTerms)", start)    
        res += "...returning [%s] matches from a potential list of length [%s] in %s seconds. \n" % (
                len(matches),len(listToSearch),elapsed)
        if len(matches) < 1:
            matches = [{'oops':"No Results"}]
        self.addLog(res)        
        return matches
    
    def saveToJsonFile(self, fileName, lod):
        self.addLog(
            "...saving lod with length [%s] to file [%s]." % (
                len(lod),fileName))
        
        with open(fileName,'w') as outfile:
            json.dump(lod, outfile)

    def readFromJsonFile(self, fileName):
        self.addLog("...reading json from file [%s]." % (fileName))        
        try:
            with open(fileName,'r') as infile:
                data = json.load(infile)
        except IOError as e:
            try:
                filename = "./%s" % filename
                with open(fileName,'r') as infile:
                    data = json.load(infile)
            except IOError as e:
                self.addLog("...unable to open file [%s]." % fileName, "red")
                data = {
                    "data":"...ERROR: unable to open file [%s]" % fileName, 
                    "E":"IOError"
                    }
        self.addLog("...retrieved data with length [%s]." % (len(data)))                 
        return {"data":data}

# SETTERS & GETTERS ==========================
    def getBaseUrl(self):
        return self.url
    def setBaseUrl(self, url):
        self.url = url

# LOGGING METHODS ===========================
    def addLog(self, msg, color="white"):
        method_file = sys._getframe(1).f_code.co_filename        
        method_name = sys._getframe(1).f_code.co_name
        method_line = sys._getframe(1).f_lineno
        method_args = sys._getframe(1).f_locals.keys()
        try:
            if(self.logLevel <= 1):
                if color == "white":
                    self.LOG += colored.white(" %s \n" % msg)
                elif color == "red":       
                    self.LOG += colored.red("%s \n" % (str(msg)))
                elif color == "yellow":  
                    self.LOG += colored.yellow("%s \n" % (str(msg)))
                elif color == "green":   
                    self.LOG += colored.green("%s \n" % (str(msg)))
                elif color == "white":   
                    self.LOG += colored.white("%s \n" % (str(msg)))
                elif color == "cyan":    
                    self.LOG += colored.cyan("%s \n" % (str(msg)))
                else: self.LOG += (str(msg))

            if(self.logLevel <= -1): 
                self.LOG += colored.blue("> %s(%s) \n" % (method_name,method_args))

        except IOError, KeyError:
            self.LOG += colored.red(
                ">> ERROR: Failed to log. <%s,%s(%s): line %s>" % (
                                method_file,method_name,method_args,method_line))

    def getLog(self):
        self.LOG += "\n\n"
        return self.LOG

    def timeElapsed(self, methodName, startTime):
        """returns the time between startTime and now and adds an entry to the log."""
        t = time.time() - startTime
        # self.addLog( 
        #     "---elapsed [%s ] for method: <%s>%s" % (
        #         str(t),sys._getframe(1).f_code.co_name, methodName) )
        return t

    def log (self,txt, color):
        level = {"red":5, "yellow":3, "green":2, "white":1, "cyan":0, "blue":-1}
        if self.logLevel <= level[color.lower()]:
            if color == "red":       
                print(colored.red("!!!> ERROR: %s" % txt))
            elif color == "yellow":  
                print(colored.yellow("!> Warning: %s" % txt))
            elif color == "green":   
                print(colored.green("%s" % txt))
            elif color == "white":   
                print(colored.white("   %s" % txt))
            elif color == "cyan":    
                print(colored.cyan("   ...%s" % txt))
            elif color == "blue":    
                print(colored.blue(">%s" % txt))
            else: print(txt)

# SHOW METHODS ===========================
    def showHtmlElements(self,name,elList,n=3):
        res += "Showing %s %s of [%s]..................... \n" % (n,type(elList[0]),name)
        res += "...element keys: " + ", ".join(elList[0].keys()) + " \n"
        for i,el in enumerate(elList):
            res += "(%s) Keys: \n" % i
            for k in el.keys():
                res += "   .get(%s): %s \n" % (k,el.get(k))
            if i+1 >= n: break
        res += "... continues for %s items.\n" % len(elList)
        self.addLog(res)
            
    def showList(self,name, showList,n=5):
        res = "Showing first %s %s of [%s].....................\n" % (n,type(showList[0]),name)
        for i,x in enumerate(showList):
            res += "[%s] %s\n" % (i,x)
            if i+1 >= n: break
        res += "... continues for %s items.\n" % len(showList)
        self.addLog(res)

    def showLod(self,name, showLod,n=5):
        if len(showLod) < 1 or type(showLod) != list: 
            res = "...cannot show lod: [%s]" % showLod
            self.addLog(res)
            return res
        else:
            res = "\n"
            res += "Showing first %s %s of [%s].....................\n" % (n,type(showLod[0]),name)
            keys = showLod[0].keys()
            for i,d in enumerate(showLod):
                res += '[%s]: \n' % i
                for k in keys:
                    res +='    k[%s] %s \n' % (k,d[k])
                if i+1 >= n: break
            res += "... continues for %s items." % len(showLod)
            self.addLog(res)
            return res
    
    def showDict(self,name,showDict,n=10):
        if len(showDict.keys()) < 1 or type(showDict) != list: 
            res = "...cannot show lod: [%s]" % showDict
            self.addLog(res)
            return res
        else:
            res = "\n"
            keys = showDict.keys()
            res += "Showing %s.....................\n" % (name)
            res += "...with keys: \n" + ", ".join(elList[0].keys())            
            for i,k in enumerate(keys):
                res +='    k[%s] %s \n' % (k,d[k])
                if i > n: break
            res += "... continues for %s keys.\n\n" % len(keys)
            self.addLog(res)
            return res


    def showUrl(self,url, queries):
        urlData = jc.crawl(url)
        for i,q in enumerate(queries):
            print "-----------------------------------Q%s" % i
            print "Query(%s): %s" % (i,q)
            res = urlData['tree'].xpath(q)
            print "len(res): %s" % len(res)            
            # print "keys: %s" % ", ".join(res.keys())                 
            print ""
            for m in range(0,len(res)): 
                text = "[ %s ]" % res[m].text_content()
                keys = res[m].keys()
                print "(%s)%s(%s) %s" % (m,res[m],keys,text)
            print("\n")
        return (urlData,res)

    def exploreUrls(self,links,numberOfurls=3):
        queries = [
                '//section[@id="postingbody"]/child::*',
                '//section[@id="postingbody"]']
        print "Results:"
        for u in range(0,numberOfurls):
            test_url = links[u]['url']
            title = links[u]['title']
            print "===================================Output for url [%s]" % u
            print ""
            print "title: %s" % title
            print "url: %s" % test_url
            print ""
            el = showUrl(test_url, queries)
            print "\n"  