from urllib.parse import urlencode
import json

import requests

from . import PastellSession, Result


class Stat(PastellSession):

    def __init__(self, session):
        super().__init__(session)

    def get(self, id_e=None, type=None):
        url = f"https://{self.server}/api/v2/document/count"
        if id_e or type:
            params = {}
            if id_e:
                params["id_e"] = id_e
            if type:
                params["type"] = type
            url = f"{url}?{urlencode(params)}"
        request = requests.get(url, auth=self.auth)
        if request.status_code == 200:
            result = json.loads(request.text)
            success = True
        else:
            result = request.text
            success = False

        return Result(success, result)

