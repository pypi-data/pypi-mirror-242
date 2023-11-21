from requests.auth import HTTPBasicAuth


__all__ = ('PastellSession','Session',)

class PastellSession:
    """
    Classe permettant de stocker les informations de session
    Serveur + Authentification
    Cette classe est ensuite étendue par toutes les classes suivantes
    ce qui permet de partager les propriétés server et auth
    """
    def __init__(self, session):
        self.server = session.server
        self.auth = session.auth

class Session:
    """
    Classe permettant d'instancier les informations de session
    Serveur + Authentification
    """
    def __init__(self, server, user, password):
        """
        Usage :
            from pastell.api import Session
            session = Session(url_pastell, user, password)
            if session.valid:
                ...

        Args:
            server ( str ): URL du serveur Pastell
            user ( str ) : user du compte Pastell à utiliser
            password ( str ) : Mot de passe associé
        """
        self.server = server
        self.auth = HTTPBasicAuth(user, password)
        # Check if session is valid
        version = Version(self).get()
        self.valid =  version.success == True
        if self.valid:
            print(f" ------------------------\nPastell version {version.result['version']} \n ------------------------")
        else:
            print(version.result)


class Result():
    def __init__(self, success, result):
        self.success = success
        self.result = result

from .connector import Connector
from .stat import  Stat
from .association import Association
from .version import Version
from .entity import Entity
from .document import Document
from .role import Role
from .utilisateur import Utilisateur