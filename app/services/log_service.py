import os, sys, time
import sys
from clint.textui import colored

class LogService():

    def __init__(self, pathToLogFile="c:/push/log_unchristened.txt", logLevel=5):
        self.pathToLogFile = os.path.normpath(pathToLogFile)
        self.logLevel = logLevel
        self.LOG = ["\n\n"]
        self.todos = []

        method_file = sys._getframe(1).f_code.co_filename
        method_name = sys._getframe(1).f_code.co_name
        method_line = sys._getframe(1).f_lineno
        method_args = sys._getframe(1).f_locals.keys()
        self.startLoggingService(method_file)
        self.startTime = None       

    # TODO METHODS ==========================================
    def todo(self,todo,b=False):
        """Takes in a todo<string> and an optional b<boolean>
        indicating whether the todo has been completed.  Adds 
        a formatted todo to the central TODO list.
        """
        if b:
            todo = colored.green("[X] %s" % todo)
        else:
            todo = colored.yellow("[ ] %s" % todo)
        self.todos.append(todo)
    
    def logTodos(self):
        """Adds all todos to central LOG var and clears
        todo list.
        """
        method_file = sys._getframe(1).f_code.co_filename
        self.LOG.append(colored.white("\nTODOS for [%s]:" % method_file))
        for t in self.todos:
            self.LOG.append("  %s" % t)
            # res += t
        self.todos = []
        # self.log(res)

    # Logging METHODS ==========================================
    def startLoggingService(self, callingFile):
        """Prints a log message describing initial
        logging service conditions.
        """
        self.todo("Review https://github.com/jfeldstein/Craigslist-Autorespond/blob/master/autorespond.py")
        if self.logLevel <= -1:
            print ""
            print(colored.blue("   ..........................................."))
            print(colored.blue("   ...Starting LogService()"))
            print(colored.blue("   ...callingFile: %s" % callingFile))
            print(colored.blue("   ...sys.stdout.isatty(): %s" % sys.stdout.isatty()))
            print(colored.blue("   ...pathToLogFile: %s" % self.pathToLogFile))
            print(colored.blue("   ...logLevel: %s" % self.logLevel))
            print(colored.blue("   ..........................................."))

    def startLog(self,note =""):
        """Initiated central LOG var including 
        optional note.
        """
        method_file = sys._getframe(1).f_code.co_filename
        self.startTime = time.time()
        
        self.log('"\n[%s] Starting Log "%s" at logLevel %s.\n' % (
            self.now(),self.pathToLogFile,self.logLevel), "white")
        if note:
            self.log(str(note), "white")

    def tlog(self, msg, color="white"):
        """Takes in a msg<string> and a color<string> and 
        adds a timestamped and formatted version of msg to
        central LOG var if color > logLevel.
          "red":5:Errors
          "yellow":3:Warnings
          "green":2:Good results
          "white":1:Primary logs
          "cyan":0:Secondary logs
          "blue":-1:Method calls
        """
        self.log("[%s] %s" % (self.now(), msg), color)
    def color(self,msg,color="white"):        
        """Takes in a msg<str> and a color<str> and returns
        a tuple (priority <int>, colored msg <str>).
          "red":5:Errors
          "yellow":3:Warnings
          "green":2:Good results
          "white":1:Primary logs
          "cyan":0:Secondary logs
          "blue":-1:Method calls
        """
        cmap = {
            "red":(5,lambda x: colored.red("!!!> ERROR: %s" % str(x))),
            "yellow":(3,lambda x: colored.yellow("!> Warning: %s" % str(x))),
            "green":(2,lambda x: colored.green("[HURRAY!] %s" % str(x))),
            "white":(1,lambda x: colored.white("  %s" % str(x))),
            "cyan":(0,lambda x: colored.cyan("  ..%s" % str(x))),
            "blue":(-1,lambda x: colored.blue(">%s" % str(x)))
        }
        return (cmap[color][0],cmap[color][1](msg))

    def log(self, msg, color):
        """Takes a msg<string> and a color<string> and 
        adds a formatted version of txt in color to the 
        central LOG var if color > logLevel.
          "red":5:Errors
          "yellow":3:Warnings
          "green":2:Good results
          "white":1:Primary logs
          "cyan":0:Secondary logs
          "blue":-1:Method calls
        """
        method_file = sys._getframe(1).f_code.co_filename        
        method_name = sys._getframe(1).f_code.co_name
        method_line = sys._getframe(1).f_lineno
        method_args = sys._getframe(1).f_locals.keys()
        try:
            nmsg = self.color(msg,color)
            if(nmsg[0] <= self.logLevel):
                self.LOG.append(nmsg[1])
            if(self.logLevel <= -1): 
                self.LOG.append(colored.blue("> %s(%s)" % (
                    method_name,method_args)))
        except UnicodeEncodeError:
            print(colored.red("\n>> ERROR<UnicodeEncodeError>: Log failure.  Dumping."))
            if(msg):
                print(colored.red("    len(msg)=%s; len(LOG)=%s;" % (
                    len(msg),len(self.LOG))))
            else:
                print(colored.red("    msg is null."))
            print(colored.red("    <%s>" % (
                method_file)))
            print(colored.red("    %s(%s): line %s>" % (
                method_name,method_args,method_line)))
            self.dump()

        except IOError, KeyError:
            self.LOG.append(colored.red(
                ">> ERROR: Failed to log. <%s,%s(%s): line %s>" % (
                    method_file,method_name,method_args,method_line)))
            self.LOG.append(colored.red(
                "     msg: %s\n    color:%s" % (
                    msg,color)))

    def dump(self):
        """Clears central LOG var and prints it's contents to terminal.
        """
        self.tlog(
            "Dumping active logs. Logs saved to %s" % (
                self.pathToLogFile), "white")
        self.logTodos()        
        for line in self.LOG:
            print(line)
        self.LOG = []
        # self.__del__()
    
    def now(self):
        return str(time.strftime("%b%d%Y_%H:%M:%S"))

    def elapsed(self, startTime):
        """Takes in a start time and Returns the time 
        between startTime and now.
        """
        t = time.time() - startTime
        # self.addLog( 
        #     "---elapsed [%s ] for method: <%s>%s" % (
        #         str(t),sys._getframe(1).f_code.co_name, methodName) )
        return t

    def show(self,txt, color):
        """ Takes in a string(txt) and a color (red,
        yellow, green, white, cyan, or blue) and prints
        a formatted version of txt in color to terminal 
        if color > logLevel.
          "red":5:Errors
          "yellow":3:Warnings
          "green":2:Good results
          "white":1:Primary logs
          "cyan":0:Secondary logs
          "blue":-1:Method calls
        """
        try:
            nmsg = self.color(msg,color)
            if(nmsg[0] <= self.logLevel):
                print(nmsg[1])
            if(self.logLevel <= -1): 
                self.LOG.append(colored.blue("> %s(%s)" % (
                    method_name,method_args)))
        except UnicodeEncodeError:
            print "Caught exception in LogService().show()!"
            
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
            
    def showList(self, name, showList, n=5):
        """Takes in a name (text description), list, and an 
        optional int(n=5) for how many rows to show.  
        Prints n rows of the list to terminal.
        """
        self.log("Showing first %s %s of [%s].....................\n" % (
            n,type(showList[0]),name), "cyan")
        for i,x in enumerate(showList):
            self.log("[%s] %s\n" % (i,x), "cyan")
            if i+1 >= n: break
        self.log("... continues for %s items.\n" % len(showList), "cyan")
        # self.log(res, "cyan")

    def showLod(self, name, showLod, n=5):
        """Takes in a name (text description), lod, and an 
        optional int(n=5) for how many rows to show.  
        Prints n rows of the lod to terminal.
        """
        if len(showLod) < 1 or type(showLod) != list: 
            res = "...cannot show lod: [%s]" % showLod
            self.log(res, "cyan")
            return res
        else:
            res = "\n"
            res += "Showing first %s %s of [%s].....................\n" % (n,type(showLod[0]),name)
            res += "[\n"
            keys = showLod[0].keys()
            for i,d in enumerate(showLod):
                # d = dict(d)
                # res += 'lod[%s]\n' % i  
                res += "    {\n"                       
                for k in keys:
                    if isinstance(d[k],str) or isinstance(d[k],unicode):
                        res +='    "%s": "%s", \n' % (k,d[k])
                    else:
                        res +='    "%s": %s, \n' % (k,d[k])
                res += '    },\n'          
                if i+1 >= n: break
            res += "]\n"
            res += "... continues for %s items." % len(showLod)
            self.log(res, "cyan")
    
    def showDict(self,name,showDict,n=10):
        """Takes in a name (text description), lod, and an 
        optional int(n=5) for how many keys to show.  
        Prints the first n keys of the dict to the terminal.
        """
        if len(showDict.keys()) < 1 or type(showDict) != list: 
            res = "...cannot show dict: [%s]" % showDict
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