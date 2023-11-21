import json

import requests

from . import PastellSession, Result
class Association(PastellSession):

    def __init__(self, session):
        super().__init__(session)


    def getByEntity(self, id_e, id_ce=None, flux=None):
        """
        Returns list off all flux associations for organism and in option, with the connector identified by his id_ce

        Args:
            id_e (str): Identifiant de l'organisme
            id_ce (str, optional): Identifiant du connecteur. Defaults to None.
            flux (_type_, optional): Identifiant du flux. Defaults to None.

        Returns:
            dict: with 2 keys success (bool) and result (list) of associations
        """
        url = f"https://{self.server}/api/v2/entite/{id_e}/flux"
        request = requests.get(url, auth=self.auth)
        if request.status_code == 200:
            data = json.loads(request.text)
            if id_ce:
                associations = []
                for association in data:
                    if flux:
                        if association["id_ce"] == id_ce and association["flux"] == flux:
                            associations.append(association)
                    else:
                        if association["id_ce"] == id_ce:
                            associations.append(association)
            else:
                associations = data

            success = True
            result = associations
        else:
            result = request.text
            success = False

        return Result(success, result)

    def delete(self, id_e, id_fe):
        url = f"https://{self.server}/api/v2/entite/{id_e}/flux?id_fe={id_fe}"
        request = requests.delete(url, auth=self.auth)
        if request.status_code == 200:
            print(f"info: Suppression de l'association {id_fe} pour l'entité ({id_e} effectuée)")

    def create(self, id_e, flux, id_ce, type):
        """
        Méthode permettant d'associer un connecteur à un flux

        Args:
            id_e (str): Identifiant de l'organisme
            flux (str): Identifiant du flux
            id_ce (str): Identifiant du connecteur
            type (str): type de connecteur (GED...)
        """
        data = {"type": type}
        # Association avec le flux fournis en paramètre
        url = f"https://{self.server}/api/v2/entite/{id_e}/flux/{flux}/connecteur/{id_ce}/"
        response = requests.post(url, data=data, auth=self.auth)
        if response.ok:
            print(f"info: Association connecteur {id_ce} ok type_flux:{flux}, id_e:{id_e}")
        else:
            print(f"error: Association connecteur {id_ce} KO erreur:{response.text}")



