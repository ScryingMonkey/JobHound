class User(DataContainer):

    UNI_LIST = [] # class variable.  All instances will have a reference to this list.

    def __init__(self, name, email):
        self.uid = 0
        self.name = name
        self.email = email
        self.jobProfiles = None
        self.campaigns = ""




    