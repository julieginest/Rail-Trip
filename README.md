from django.contrib.auth.decorators import login_required

# Rail-Trip

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

```python
@login_required Force l'utilisateur à être login pour accéder à telle chose
@require_POST # Faire en sorte que la view ne fait que une requête POST
```