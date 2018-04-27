import os
import sys
from clint.textui import colored

class LogService():

    def __init__(self, pathToLogFile="c:/push/log_unchristened.txt", logLevel=1):
        self.pathToLogFile = os.path.normpath(pathToLogFile)
        self.logLevel = logLevel
        if self.logLevel <= 1:
            print(colored.cyan("   ..........................................."))
            print(colored.cyan("   ...Starting LogService()"))
            print(colored.cyan("   ...sys.stdout.isatty(): %s" % sys.stdout.isatty()))
            print(colored.cyan("   ...pathToLogFile: %s" % pathToLogFile))
            print(colored.cyan("   ...logLevel: %s" % self.logLevel))
            print(colored.cyan("   ..........................................."))

    def log (self,txt, color):
        # if self.logLevel <= -1:
        #     print colored.blue(">log( txt=\"%s\", color:\"%s\" )" % (txt,color))
        level = {"red":5, "yellow":3, "green":2, "white":1, "cyan":0, "blue":-1}
        attr = []
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