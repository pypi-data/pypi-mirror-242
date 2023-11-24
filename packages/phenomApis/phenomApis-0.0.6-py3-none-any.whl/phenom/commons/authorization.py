from phenom.commons.get_token import tokengeneration
from phenom.api.resumeparser.resume_parsing_api import ResumeParsingApi
from phenom.api.exsearch.employees_api import EmployeesApi
from phenom.api.prediction.prediction_api import PredictionApi


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

    # employee search api methods
    def exsearch_api(self):
        return EmployeesApi(self.token(), self.gateway_url, self.apikey)

    # prediction api methods
    def prediction_api(self):
        return PredictionApi(self.token(), self.gateway_url, self.apikey)
