from data_container import DataContainer
from job_profile import JobProfile
from job_opportunity import JobOpportunity

class JobCampaign(DataContainer):
# A total effort to locate a position based on a job profile.
# Contains many individual JobOpportunities, each representing a single position.
    def __init__(self):
        self.id = 0
        self.state = "new"
        self.leads 
        self.opportunities
        self.interviews

        
        # potential job campaign states = [
        #   "new",
        #   "active",
        #   "scheduled",
        #   "on hold",
        #   "closed"
        # ]