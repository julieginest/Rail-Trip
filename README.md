# 🚆Bienvenue dans RailTrip

## 🗎 Contexte :
Notre projet offre une nouvelle vision le concept traditionnel du roadtrip en le réinventant à travers le voyage en train. Nous avons développé une application web intuitive, conçue pour simplifier la planification et la gestion de vos déplacements. Que vous soyez connecté ou non, l'application propose des fonctionnalités adaptées pour répondre à toutes vos attentes en matière de voyage.

## 🔍 Fonctionnalités :

- **POUR TOUS LES UTILISATEURS** : 
    <br>Les nouveaux utilisateurs peuvent créer un compte en fournissant un pseudo, un mot de passe et en acceptant les conditions d'utilisation et la politique de confidentialité. L'utilisateur peut ensuite accéder à des fonctionalités avancées (indiqué ci-dessous).<br>
    Gestion de la création d'un compte : ```App>App>views>register.py ```

- **POUR LES UTILISATEURS NON CONNECTES** :
<br>Rechercher des trajets :
    - Entrer une **ville de départ**, une **ville d'arrivé**, une **date de départ**, et une **heure de départ**. 
    - L'application renvoie les billets disponibles pour ce trajet avec le **prix**
    ```App>App>views>home.py```

- **POUR LES UTILISATEURS CONNECTES** :
1. Création des roadtrips:
    - Créer un rodatrip en spécifiant une **ville de départ**, **deux étapes** et une **ville d'arrivée**.
    - Les roadtrips peuvent être **publics** ou **privés**.
    - Recevoir des propositions de billets pour chaque trajet du roadtrip.
    - **Enregistrer** votre roadtrip (sans sélection des billets)
    - Les roadtrips enregistrés sont accessibles dans vos enregistrements, où vous pouvez redemander l'affichage des billets.

2. Gestion des roadtrips :
    - **Consulter** les roadtrips **publics** des autres utilisateurs. <br>```App>App>>views>consulter.py```
    - **Filtrez** les roadtrips par **durée en jours** ou par **ville de départ** <br>```App>App>templates>views>consulter.py```
    - **Ajouter** un roadtrip d'un autre utilisateur à vos favoris. <br>```App>App>>views>consulter.py```
    - **Supprimer** vos roadtrips et vos favoris selon vos besoins. 
    <br>Suppression un roadtrip : ```App>App>>views>enregistrements.py```
    <br>Supprimer un favoris : ```App>App>>views>favoris.py```

## 🔨 Installation et paramétrage :
- Prérequis (logiciel)
- Commandes à exécuter
- BDD

## Démarage du projet





## Variables d'environement:

- API_KEY : Clef de l'API SNCF
- API_LINK : Adresse de l'API

<!--  -->

- DATABASE_ADRESS : Adresse de mariadb
- DATABASE_NAME : Nom de la base de donnée
- DATABASE_USER : Utilisateur MariaDB
- DATABASE_PASSWORD : Mot de passe de l'utilisateur MariaDB

## Structure:

```
/Rail-Trip
├─ App-RailTrip    --Dossier python venv--
│  └─ App          --Dossier Django--
│
├─ README.md       --Ce fichier--
└─ .env            --Ficher des variables d'environment--
```
