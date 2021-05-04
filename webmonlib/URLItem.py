from json import JSONEncoder

class URLItem(JSONEncoder):
    '''
    Data class to hold the information collected
    '''
    def __init__(self, url:str = None, reactiontime:float = 0.0, success:bool = False ):
        '''
        - url: string of url
        - reactiontime: float of time to respond to open and get data
        - success: bool specifies if the connection was successful or not
        '''
        self.property_url:str = url
        self.property_reactiontime:float = reactiontime
        self.property_success:bool = success

    @property
    def Url(self):
        return self.property_url

    @property
    def ReactionTime(self):
        return self.property_reactiontime

    @property
    def Success(self):
        return self.property_success        