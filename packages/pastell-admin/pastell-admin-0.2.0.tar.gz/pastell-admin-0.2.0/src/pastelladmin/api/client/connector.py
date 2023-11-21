import json

import requests

from . import PastellSession, Result

class Connector(PastellSession):

    def __init__(self, session):
        super().__init__(session)

    def __addToDict(self, item, dictionary):
        if not item["id_e"] in dictionary.keys():
            dictionary[item["id_e"]] = { item["libelle"] : [item["id_ce"]] }
        else:
            if not item["libelle"] in dictionary[item["id_e"]]:
                dictionary[item["id_e"]][item["libelle"]] = [item["id_ce"]]
            else:
                dictionary[item["id_e"]][item["libelle"]].append(item["id_ce"])

    def getAll(self, scope, id_connecteur=None, outputFormat='list') -> Result:
        """
        Get all connectors with one id_connecteur (option) (eg 'depot-pastell')
        for one id_e or all organisms

        Args:
            scope (str): 'all' or id_e
            id_connecteur (str): id_connecteur eg "depot-pastell"
            outputFormat (str): 'list' or 'dict'. Defaults = 'list'

        Returns:
            dict: with 2 keys success (bool) and result (dict)
            result dic structure item :{id_e:{"lib_connector":[id_ce]}} or
            result list structure = raw response from Pastell
            sample result dict : {"123":{"myfirst_connector":["47"]}, {"mysecond_connector":["48"]},"124":{...}}
        """
        url = f"https://{self.server}/api/v2/entite/{scope}/connecteur"
        if scope == 'all':
            url = f"https://{self.server}/api/v2/connecteur/{scope}/"
            if id_connecteur:
                url = f"https://{self.server}/api/v2/connecteur/{scope}/{id_connecteur}"

        request = requests.get(url, auth=self.auth)
        if request.status_code == 200:
            success = True
            connectors = json.loads(request.text)
            if outputFormat == 'list':
                if not id_connecteur:
                    #raw response from PAstell
                    result = connectors
                else:
                    #raw response from PAstell filtered by id_connecteur
                    result = [connector for connector in connectors if connector["id_connecteur"] == id_connecteur]
            elif outputFormat == 'dict':
                #create dict id_e:libelle:[id_ce]
                result = {}
                for connector in connectors:
                    if not id_connecteur or (id_connecteur and connector["id_connecteur"] == id_connecteur):
                        self.__addToDict(connector, result)

        else:
            success = False
            result = request.text

        return Result(success, result)

    def delete(self, id_e, id_ce):
        url = f"https://{self.server}/api/v2/entite/{id_e}/connecteur/{id_ce}"
        request = requests.delete(url, auth=self.auth)
        result = json.loads(request.text)
        if request.status_code == 200:
            print(f"info: Connecteur: {id_ce} supprimé avec succès")

    def update(self, id_e, id_ce, parameters, file=None):
        """_summary_

        Args:
            id_e (_type_): _description_
            id_ce (_type_): _description_
            parameters (_type_): _description_

        Returns:
            _type_: _description_
        """
        if file:
            urlConnecteur = f"https://{self.server}/api/v2/entite/{id_e}/connecteur/{id_ce}/file/definition"
            responseConnecteur = requests.post(urlConnecteur, data=parameters, files=file, auth=self.auth)
        else:
            urlConnecteur = f"https://{self.server}/api/v2/entite/{id_e}/connecteur/{id_ce}/content/"
            responseConnecteur = requests.patch(urlConnecteur, data=parameters, auth=self.auth)

        success = False
        if responseConnecteur.ok:
            success = True
        else:
            print(f"error: Creation config connecteur {id_ce} KO erreur:{responseConnecteur.text}")

        return Result(success, None)

    def create(self, id_e, definition):
        """
        Creation du connecteur sans sa configuration pour l'IDE sélectionnée

        Args:
            id_e (str): Identifiant de l'entité
            definition (dict): Dictionnaire de clés valeurs

        Returns:
            dict: with 2 keys success (bool) and result (str) id_ce created
        """

        url = f"https://{self.server}/api/v2/entite/{id_e}/connecteur/"
        request = requests.post(url, data=definition, auth=self.auth)
        if request.ok:
            data = json.loads(request.text)
            result = data["id_ce"]
            success = True
        else:
            success = False
            result = request.text

        return Result(success, result)

    def action(self, id_e, id_ce, action):
        url = f"https://{self.server}/api/v2/entite/{id_e}/connecteur/{id_ce}/action/{action}"
        request = requests.post(url, auth=self.auth)
        if request.ok:
            data = json.loads(request.text)
            result = data["last_message"]
            success = data["result"]
        else:
            success = False
            result = request.text

        return Result(success, result)

    def detail(self, id_e, id_ce):
        url = f"https://{self.server}/api/v2/entite/{id_e}/connecteur/{id_ce}"
        request = requests.get(url, auth=self.auth)
        if request.ok:
            result = json.loads(request.text)
            success = True
        else:
            success = False
            result = request.text

        return Result(success, result)



