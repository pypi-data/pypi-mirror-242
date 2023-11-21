import json

import requests

from . import PastellSession, Result
from .stat import Stat


class Entity(PastellSession):

    def __init__(self, session):
        super().__init__(session)

    def getAllWithStatus(self):
        """
        Méthode permettant de retourner tous les organismes actifs(entités) Pastell

        Returns:
             dict: with 2 keys success (bool) and result (dict with 3 lists)
        """
        stats = Stat(self).get()
        success = False
        if stats.success:
            active = []
            no_active = []
            for ide, obj in stats.result.items():
                if obj["info"]["is_active"] == "1":
                    active.append(obj["info"])
                else:
                    no_active.append(obj["info"])
            print(f"info: {len(no_active)} entités sont inactives et {len(active)} entités sont actives")
            succcess = True
            result = {'all': [*active, *no_active],'active': active, 'no_active': no_active}
        else:
            result = stats.result
        return Result(True, result)



    def getAll(self):
        """
        Méthode permettant de retourner tous les organismes (entités) Pastell

        Returns:
             dict: with 2 keys success (bool) and result (list)
        """

        url = f"https://{self.server}/api/v2/entite"
        request = requests.get(url, auth=self.auth)

        if request.status_code == 200:
            result = json.loads(request.text)
            success = True
        else:
            result = request.text
            success = False

        return Result(success, result)

    def getFilles(self, id_e, tree=None):
        """
        Méthode permettant de retourner tous les organismes filles (entités/services)  d'une entité Pastell

        Returns:
             dict: with 2 keys success (bool) and result (list)
        """
        #Interdit pour entité racine 0
        assert int(id_e) > 0

        entities = [id_e]
        work = [id_e]
        level = 1
        calls = 0
        erreur = False
        while len(work) > 0 and not erreur:
            newLevel = []
            finished = []
            for ide in work:
                request = Entity(self).detail(ide)
                if request.success:
                    calls +=1
                    filles = []
                    if len(request.result["entite_fille"]) > 0:
                        filles = [e["id_e"] for e in request.result["entite_fille"]]
                        entities.extend(filles)
                        newLevel.extend(filles)
                    #print (f"level : {level} : call {calls} : {ide} --> {filles}")
                    finished.append(ide)
                else:
                    erreur = True
                    result = request.result
                    break
            if not erreur:
                for id in finished:
                    work.remove(id)
                work.extend(newLevel)
                level += 1
        entities.sort(key = int)
        result = [{"id_e": entity} for entity in entities]
        return Result(not erreur, result)

    def detail(self, id_e) -> Result:
        """
        Méthode permettant de retourner le détail d'un organisme donné (fourni par id_e)

        Args:
            id_e ( str ): identifiant de l'entité.

        Returns:
            dict: with 2 keys success (bool) and result (dict)
        """
        assert isinstance(id_e, str)
        url = f"https://{self.server}/api/v2/entite/{id_e}"
        request = requests.get(url, auth=self.auth)
        if request.status_code == 200:
            result = json.loads(request.text)
            success = True
        else:
            result = request.text
            success = False

        return Result(success, result)




