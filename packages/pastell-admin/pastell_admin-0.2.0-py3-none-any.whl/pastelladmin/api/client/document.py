import json
from datetime import datetime
import requests

from . import PastellSession, Result


class Document(PastellSession):
    def __init__(self, session):
        super().__init__(session)

    def detail(self, id_e, id_d):
        url = f"https://{self.server}/api/v2/entite/{id_e}/document/{id_d}"
        request = requests.get(url, auth=self.auth)
        success = False
        if request.status_code == 200:
            result = json.loads(request.text)
            success = True
        else:
            result = request.text

        return Result(success, result)

    def check_file_receive(self, id_e: str, id_d: str, type: str, num: int) -> Result:
        url = f"https://{self.server}/api/v2/entite/{id_e}/document/{id_d}/file/{type}/{num}?receive=true"
        request = requests.get(url, auth=self.auth)
        success = request.status_code == 200
        result = json.loads(request.text) if success else request.text

        return Result(success, result)

    def update(self, id_e, id_d, data):
        url = f"https://{self.server}/api/v2/entite/{id_e}/document/{id_d}"
        request = requests.patch(url, auth=self.auth, data=data)
        success = None
        if request.status_code == 200:
            result = json.loads(request.text)
            success = True
        else:
            result = request.text
            success = False

        return Result(success, result)

    def action(self, id_e, id_d, action):
        url = f"https://{self.server}/api/v2/entite/{id_e}/document/{id_d}/action/{action}"
        request = requests.post(url, auth=self.auth)
        success = None
        if request.status_code == 201:
            result = json.loads(request.text)
            success = True
        else:
            result = request.text
            success = False

        return Result(success, result)

    def getByFilter(
        self,
        id_e,
        dossier=None,
        status=None,
        start=None,
        end=None,
        transit=False,
        pagination=1000,
        limit=0,
    ):
        # check types
        date_format = "%Y-%m-%d"
        for date in (start, end):
            if date:
                assert datetime.strptime(date, date_format)
        assert type(pagination) == int
        assert type(limit) == int
        assert type(transit) == bool
        success = None
        # On positionne l'offset à 0 pour la première requête
        offset = 0
        if limit > 0 and limit < pagination:
            pagination = limit
        completed = False
        parameters = {}
        result = []
        # Construct URL parameters
        if dossier:
            parameters["type"] = dossier
        if status and transit:
            parameters["etatTransit"] = status
            if start:
                parameters["state_begin"] = start
            if end:
                parameters["state_end"] = end
        elif status and not transit:
            parameters["lastetat"] = status
            if start:
                parameters["last_state_begin"] = start
            if end:
                parameters["last_state_end"] = end
        elif start:
            parameters["last_state_begin"] = start

        while not completed:
            pagination_parameters = {"limit": pagination, "offset": offset}
            url = f"https://{self.server}/api/v2/entite/{id_e}/document"
            request = requests.get(
                url, params={**parameters, **pagination_parameters}, auth=self.auth
            )
            if request.status_code == 200:
                docs_json = json.loads(request.text)
                if len(docs_json) > 0:
                    # On augmente l'offset de la limite pour une éventuelle prochaine requête
                    offset += pagination
                    result.extend(docs_json)
                    if limit > 0 and len(docs_json) >= limit:
                        completed = True
                        success = True
                else:
                    # 0 enregistrement donc on a tout récupérer
                    completed = True
                    success = True
                if len(docs_json) < pagination:
                    completed = True
                    success = True
            else:
                result = f"erreur de récupération des documents pour l'entité {id_e}"
                success = False
                break

        return Result(success, result)
