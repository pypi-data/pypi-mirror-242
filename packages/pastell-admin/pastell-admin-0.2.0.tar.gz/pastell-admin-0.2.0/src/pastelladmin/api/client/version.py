import json
import requests

from . import PastellSession, Result

class Version(PastellSession):

    def __init__(self, session):
        super().__init__(session)

    def get(self):
        url = f"https://{self.server}/api/v2/version"
        request = requests.get(url, auth=self.auth)
        if request.status_code == 200:
            result = json.loads(request.text)
            success = True
        else:
            result = request.text
            success = False

        return Result(success, result)