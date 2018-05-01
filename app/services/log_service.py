import os, sys, time
import sys
from clint.textui import colored

class LogService():

    def __init__(self, pathToLogFile="c:/push/log_unchristened.txt", logLevel= 0):
        self.pathToLogFile = os.path.normpath(pathToLogFile)
        self.logLevel = logLevel
        self.LOG = ""
        self.todos = []
        self.startLoggingService()
        self.startTime = None

    # TODO METHODS ==========================================
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
        self.log(res)

    # Logging METHODS ==========================================
    def startLoggingService(self):
        if self.logLevel <= -1:
            print ""
            print(colored.blue("   ..........................................."))
            print(colored.blue("   ...Starting LogService()"))
            print(colored.blue("   ...sys.stdout.isatty(): %s" % sys.stdout.isatty()))
            print(colored.blue("   ...pathToLogFile: %s" % pathToLogFile))
            print(colored.blue("   ...logLevel: %s" % self.logLevel))
            print(colored.blue("   ..........................................."))

    def startLog(self, note =""):
        self.startTime = time.time()
        self.LOG = "\n\n[%s] Starting Log : \n" % (self.now())
        if note:
            self.LOG += str(note)

    def tlog(self, msg, color="white"):
        self.log("[%s] %s" % (self.now,msg), color)

    def log(self, msg, color="white"):
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

    def dump(self):
        self.LOG += "\n[%s] dump logs. \n\n" % self.now()
        dump = self.LOG
        self.LOG = None
        return dump
    
    def now(self):
        return time.strftime("%H:%M:%S")

    def elapsed(self, startTime):
        """returns the time between startTime and now and adds an entry to the log."""
        t = time.time() - startTime
        # self.addLog( 
        #     "---elapsed [%s ] for method: <%s>%s" % (
        #         str(t),sys._getframe(1).f_code.co_name, methodName) )
        return t

    def show(self,txt, color):
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
        self.log(res, "cyan")
            
    def showList(self,name, showList,n=5):
        res = "Showing first %s %s of [%s].....................\n" % (n,type(showList[0]),name)
        for i,x in enumerate(showList):
            res += "[%s] %s\n" % (i,x)
            if i+1 >= n: break
        res += "... continues for %s items.\n" % len(showList)
        self.log(res, "cyan")

    def showLod(self,name, showLod,n=5):
        if len(showLod) < 1 or type(showLod) != list: 
            res = "...cannot show lod: [%s]" % showLod
            self.log(res)
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
            self.log(res, "cyan")
    
    def showDict(self,name,showDict,n=10):
        if len(showDict.keys()) < 1 or type(showDict) != list: 
            res = "...cannot show lod: [%s]" % showDict
            self.log(res, "cyan")
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
            self.log(res, "cyan")



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