import json
import requests

from . import PastellSession, Result


class Utilisateur(PastellSession):

    def __init__(self, session):
        super().__init__(session)

    def create(self, params):
        url = f"https://{self.server}/api/v2/utilisateur"
        request = requests.post(url, data=params, auth=self.auth)
        if request.status_code == 201:
            result = json.loads(request.text)
            success = True
        else:
            result = request.text
            success = False

        return Result(success, result)

    def delete(self, id_u):
        url = f"https://{self.server}/api/v2/utilisateur/{id_u}"
        request = requests.delete(url, auth=self.auth)
        result = json.loads(request.text)
        if "result" in result and result["result"] == 'ok':
            result = json.loads(request.text)
            success = True
        else:
            result = request.text
            success = False

        return Result(success, result)

    def removeRole(self, id_u, id_e, role):
        url = f"https://{self.server}/api/v2/utilisateur/{id_u}/role?role={role}&id_e={id_e}"
        request = requests.delete(url, auth=self.auth)
        if request.status_code == 200:
            result = json.loads(request.text)
            success = True
        else:
            result = request.text
            success = False

        return Result(success, result)

    def addRole(self, id_u, role):
        url = f"https://{self.server}/api/v2/utilisateur/{id_u}/role"
        request = requests.post(url, data={"role": role}, auth=self.auth)
        if request.status_code == 201:
            result = json.loads(request.text)
            success = True
        else:
            result = request.text
            success = False

        return Result(success, result)

    def getRoles(self, id_u):
        url = f"https://{self.server}/api/v2/utilisateur/{id_u}/role"
        request = requests.get(url, auth=self.auth)
        if request.status_code == 200:
            result = json.loads(request.text)
            success = True
        else:
            result = request.text
            success = False

        return Result(success, result)

