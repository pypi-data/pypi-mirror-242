# Package pastelladmin
Scripts pour Pastell


# Installation

Pour la version stable :

```
pip install pastell-admin==0.2.0
```

Pour la version de dev :

```
pip install requests
pip install -i https://test.pypi.org/simple/ pastell-admin==0.2.0
```
# Développement

```
git clone git@github.com:megalis-bretagne/scripts-pastell.git
cd scripts-pastell
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

# Utilisation des scripts

## Sécurité
Ces scripts utilisent des API de Pastell. La configuration s'effectue dans le fichier de config **.pastell-admin** situé dans le dossier de l'utilisateur courant. Si ce fichier n'existe pas, il faut le créer à partir d'une copie de **pastell-admin.dist**. Configurer le fichier **~/.pastell-admin** avec notamment les informations de connexion pour les deux environnements (preprod et prod)

```ini
[preprod]
server = pastell-preprod.mondomaine.org
login = username
password = mypassword

[prod]
server = pastell.mondomaine.org
login = username
password = mypassword
```

## SCRIPT pastell_org

Ce script permet de générer un fichier csv avec la liste des entités Pastell.

### Paramètres

 - `--env` : pour sélectionner l'environnement d'éxécution (**preprod** ou **prod**)
 - `--csv` : fichier csv généré. Par défault il s'agit du fichier /tmp/organismes.csv"
 - `--active` :  Retourne uniquement les entités actives. Par défaut retourne toutes les entités.

### exemple de commande

```
pastell_org --env=preprod --csv=org.csv --active
```

## SCRIPT pastell_find.py

Ce script liste tous les documents pastell dans un état particulier sur une période donnée

Le script génère deux fichiers. Un fichier **csv** pour lecture et un fichier **json** qui peut ensuite servir de source au script **pastell_delete.py**



### Paramètres (clé=valeur)

 - `--env=` : pour sélectionner l'environnement d'éxécution (**preprod** ou **prod**)
 - `--status` : liste des états de dossiers pastell recherchés  exemple **tdt-error** ou si plusieurs valeurs : **accepter-sae erreur-verif-tdt**
 - `--flux` : liste des types de dossiers (flux) à filtrer. eg : **actes-generique** ou **actes-generique,deliberations-studio**. Si non renseigné, le traitement est appliqué à l'ensemble des types de dossier
 - `--org=` : Limite l'analyse à l' id_e fournis en paramètre. exemple. org=1
 - `--output=` : définit le nom des fichiers générés (csv + json). **result** par défaut. Utiliser un chemin relatif.

### Options (clé)

- `--list` :  Pour lister les documents concernés (id_d)
- `--count`: pour uniquement dénombrer le nombre de documents filtrés.
- `--transit`: pour cibler les documents passés par l'état et non (par défaut) les documents dans état courant
- `--json`: pour récupérer une version json du fichier de sortie
- `--merge`: Pour mette à jour un fichier existant (output csv)




### exemples de commande
```
pastell_find --env=preprod \
--status tdt-error --output=data/docs-tdt-error \
--start=2015-01-01 --end=2022-02-10 \
--list --json
```

```
pastell_find --env=preprod \
--status accepter-sae termine --flux actes-generique deliberations-studio \
--output=data/docs-sae --org=1 \
--start=2015-01-01 --end=2022-08-31 \
--count
```

## SCRIPT pastell_docs_delete_from_list.py


Ce script supprime les documents pastell listés dans un fichier json avec la structure suivante :

```json
{ "docs" : [
    {
        "id_e": "1",
        "document": "9uTg9B4"
    },
    {
        "id_e": "7",
        "document": "AubgGTA"
    }
]}
```

Le script produit un fichier de log **delete.log**


### Paramètres

 - `--env` : pour sélectionner l'environnement d'éxécution (**preprod** ou **prod**)
 - `--limit` :  Définit une limite à l'exécution (nombre de documents supprimés) . Default  = 0 c'est à dire sans limite
 - `--source` : définit le nom du fichier en entrée (chemin absolu ou relatif).




### exemple de commande
```
./pastell_docs_delete_from_list.py --env=preprod --source=docs-tdt-error.json
```


## SCRIPT delete_any.py

Ce script supprime tous les documents pastell d'un type de dossier défini et dans un état défini.

### Paramètres

 - `--env` : pour sélectionner l'environnement d'éxécution (**preprod** ou **prod**)
 - `--status` : Etat de dossiers pastell recherchés  exemple **terminate**
 - `--type` :  Définit le type de dossier.exemple **autres-studio-sans-tdt**

### exemple de commande

```
./delete_any.py --env=preprod --status=terminate --type=autres-studio-sans-tdt
```

## SCRIPT pastell_connector

Ce script permet de gérer des connecteurs pour une instance Pastell:

 - statut d'un connecteur (absence, présence, doublons) unitaire ou en masse
 - création de connecteurs et association unitaire ou en masse
 - Mise à jour d'un connecteur unitaire ou en masse
 - Mise à jour et création si nécessaire d'un connecteur unitaire ou en masse
 - Désassociation d'un connecteur unitaire ou en masse
 - Suppression d'un connecteur unitaire ou en masse

### Paramètres

 - `--env` : pour sélectionner l'environnement d'éxécution (**preprod** ou **prod**)
 - `--source` : fichier json contenant la définition du connecteur ou la liste des connecteurs à supprimer ``[{"id_e":"", "id_ce"},]``
 - `--org` : précise l'id_e de l'entité cocernée par la création du connecteur
 - `--recursive` : précise si les entités filles sont également concernées. A associer avec --org=
 - `--flux` : type de dossier (flux) Liste séparée par des vigules. Requis pour les actions de dissociation et de suppression sans fichier source
 - `--action` : Requis. A choisir parmis [create, update, append, dissociate, delete, status]
 - `--libelle` :  Libellé du connecteur. Requis pour les actions de statut, de dissociation et de suppression sans fichier source
 - `--type` : type de connecteur (eg. GED). Requis pour les actions de dissociation et de suppression sans fichier source
 - `--id_connector` : id_connecteur (eg. depot-pastell). Requis pour les actions de dissociation et de suppression sans fichier source
 - `--details` : A utiliser avec l'action status. Option pour afficher les id_e des entités concernées.
 - `--scheduler` : Pour lancer un connecteur de purge en asynchrone.

### exemples de commande

#### Statut d'un connecteur
```
pastell_connector --env=preprod --action=status --libelle=ged-megalis-opendata-sans-tdt --details
```

#### Création d'un connecteur 1
Dans cet exemple, le connecteur est créé sans association pour l'entité n°1 et ses filles
```
pastell_connector --env=preprod --org=1 --recursive --action=create --source=connectors/opendata-sans-tdt.json
```

#### Création d'un connecteur cas 2
Dans cet exemple, le connecteur est créé et associé au flux **autres-studio-sans-tdt** pour toutes les entités qui n'en disposent pas déjà
```
pastell_connector --env=preprod --action=create --flux=autres-studio-sans-tdt --source=connectors/opendata-sans-tdt.json
```

#### Création d'un connecteur cas 3
Dans cet exemple, le connecteur est de purge est créé et déclenché en asynchrone
```
pastell_connector --env=preprod --org=1 --action=create --scheduler --source=connectors/purge.json
```

#### Mise à jour d'un connecteur
Cette mise à jour s'applique uniquement au connecteurs existants
```
pastell_connector --env=preprod --action=update --flux=autres-studio-sans-tdt --source=connectors/opendata-sans-tdt.json
```

#### Création ou mise à jour d'un connecteur
Si le connecteur n'existe pas il est créé sinon il est mis à jour pour l'entité n°1 avec récursivité.
```
pastell_connector --env=preprod --org=1 --recursive --action=append --flux=autres-studio-sans-tdt --source=connectors/opendata-sans-tdt.json
```

#### Dissociation d'un connecteur avec un flux pour toutes les entités
```
pastell_connector --env=preprod --action=dissociate --flux=autres-studio-sans-tdt --type=GED --libelle=ged-megalis-opendata-sans-tdt --id_connector=depot-pastell
```

#### Supression d'un connecteur pour une entité sans récursivité
```
pastell_connector --env=preprod --org=1 --action=delete --libelle=ged-megalis-opendata-sans-tdt --id_connector=depot-pastell --type=GED
```

#### Supression de connecteurs à partir d'une liste
```
pastell_connector --env=preprod --action=delete --source=connectors/connectors_to_delete.json
```

## SCRIPT pastell_stats

Ce script permet de générer un fichier csv en sortie avec les statistiques pastell:


### Paramètres

- `--env` : pour sélectionner l'environnement d'éxécution (**preprod** ou **prod**)
- `--csv` : fichier csv généré. Par défault il s'agit du fichier /tmp/stats-yyyy-mm-aa.csv"
- `--org` : précise l'id_e de l'entité concernée par la création du connecteur
- `--flux` : Filtre les stats pour un type de flux
- `--infos` : pour afficher le statut des organismes et  notamment si l'entité est active

### exemples de commande

```
pastell_stats --env=preprod --org=1 --csv=info.csv --infos
```

```
pastell_stats --env=preprod  --csv=/tmp/statistiques.csv
```


## SCRIPT pastell_associations

Ce script permet de générer un fichier csv en sortie avec les associations connecteur / flux


### Paramètres

- `--env` : pour sélectionner l'environnement d'éxécution (**preprod** ou **prod**)
- `--csv` : fichier csv généré. Par défault il s'agit du fichier /tmp/associations.csv"
- `--org` : précise l'id_e de l'entité concernée par la création du connecteur


### exemples de commande

```
pastell_associations --env=preprod --org=1 --csv=associations.csv
```

## SCRIPT pastell_connector_instances

Ce script permet de générer un fichier csv en sortie avec toutes les instances de connecteurs pastell


### Paramètres

- `--env` : pour sélectionner l'environnement d'éxécution (**preprod** ou **prod**)
- `--csv` : fichier csv généré. Par défault il s'agit du fichier /tmp/instances.csv"
- `--org` : précise l'id_e de l'entité concernée par la création du connecteur


### exemples de commande

```
pastell_connector_instances --env=preprod --org=1 --csv=instances.csv
```

## SCRIPT pastell_matrice

Ce script permet de générer un fichier csv en sortie avec la matrice de rôles Pastell


### Paramètres

- `--env` : pour sélectionner l'environnement d'éxécution (**preprod** ou **prod**)
- `--csv` : fichier csv généré. Par défault il s'agit du fichier /tmp/matrice.csv"


### exemples de commande

```
pastell_matrice --env=preprod --csv=roles.csv
```

# Utilisation pour des développements


## Client API

```python
from src.pastelladmin.api.client import Session, Version

session = (server="mon-serveur-pastel.org", user="username", password="Mon password")
version_pastell = Version(session).get().result
print(version)
```
## Scripts

```python
from src.pastelladmin.pastell_stats import stats

stats(env="prod", org="1")
```