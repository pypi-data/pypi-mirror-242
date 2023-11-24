from phenom.api.commons.get_token import tokengeneration
from phenom.api.resumeparser.resume_parsing_api import ResumeParsingApi



class Authorization(object):
    def __init__(self, url, client_id, client_secret, gateway_url, apikey=None):
        self.url = url
        self.client_id = client_id
        self.client_secret = client_secret
        self.gateway_url = gateway_url
        self.apikey = apikey

    def token(self):
        return tokengeneration(self.url, self.client_id, self.client_secret)

    # resumeparser api methods
    def resumeparser_api(self):
        return ResumeParsingApi(self.token(), self.gateway_url, self.apikey)

