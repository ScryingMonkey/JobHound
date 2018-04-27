import json
from app.services import LogService
# [END imports]

class HubService():

    leadList = [
                {'name':"Test Job 1", 'description':"A pretty good job."}, 
                {'name':"Test Job 2", 'description':"An ok job."}, \
                {'name':"Test Job 3", 'description':"A not very fun job."} 
                ]

    def __init__(self, pathToLogFile="c:/push/log_unchristened.txt",logLevel=1):
        self.l = LogService(pathToLogFile=pathToLogFile, logLevel=logLevel)
        self.l.log("...........................................", 'cyan')
        self.l.log("Starting HubService()", 'cyan')
        self.l.log("pathToLogFile: %s" % pathToLogFile, 'cyan')
        self.l.log("logLevel: %s" % logLevel, 'cyan')
        self.l.log("...........................................", 'cyan')

    def log(self,txt, color):
        self.l.log(txt,color)

    def getLeadListJson(self):
        return json.dumps({'data': self.leadList})

    def setLeadList(self, jsonString):
        return json.loads(jsonString)