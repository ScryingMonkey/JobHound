# [START imports]
from app.doers import JobCrawler
from app.services import HubService, LogService
# [END imports]


h = HubService(logLevel=-1)
craigsListNhJobsUrl = "https://nh.craigslist.org/d/jobs/search/jjj"
crawler = JobCrawler(craigsListNhJobsUrl)
