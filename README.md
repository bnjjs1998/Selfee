# Selfee - API Django Pokedex

API Django pour:
- authentification (session + token)
- gestion des groupes Pokemon par type
- listing des Pokemon accessibles selon les groupes de l'utilisateur

## Prerequis

- Python 3.11+
- pip

## Installation (PowerShell)

```powershell
cd C:\Users\bapti\Desktop\Selfee
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Initialisation de la base

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Lancer le serveur

```powershell
python manage.py runserver
```

Base URL locale: http://127.0.0.1:8000

## Lancer les tests

```powershell
python manage.py test
```

Tests cibles:

```powershell
python manage.py test Pokedex_selfee.Pokedex_App.tests.test_group_views
python manage.py test Pokedex_selfee.Pokedex_App.tests.test_pokemon_views
```

## Endpoints

### Auth

- GET /api/hello/ une route qui 
- POST /api/login/
- GET /api/session/
- POST /api/logout/
- DELETE /api/logout/
- GET /api/user/me

### Groupes Pokemon

- POST /api/group/<pokemon_type>/add/
- POST /api/group/<pokemon_type>/remove/
- DELETE /api/group/<pokemon_type>/remove/

### Pokemon

- GET /api/pokemon/
  Retourne la liste des Pokemon accessibles selon les groupes de l'utilisateur.
  Format de sortie: id + name.

- GET /api/pokemon/<pokemon_name>/
  Retourne le detail d'un Pokemon, avec types filtres selon les groupes de l'utilisateur.

## Commandes shell (PowerShell)

Note: superuser ou user classique, les deux fonctionnent.

### 1) Login

```powershell
$body = @{ username = "bnjjs"; password = "1234" } | ConvertTo-Json -Compress
$login = Invoke-RestMethod -Method POST `
  -Uri "http://127.0.0.1:8000/api/login/" `
  -ContentType "application/json" `
  -Body $body

$login
```

### 2) Ajouter un type

```powershell
Invoke-RestMethod -Method POST `
  -Uri "http://127.0.0.1:8000/api/group/grass/add/" `
  -Headers @{ Authorization = "Token $($login.token)" }
```

### 3) Verifier la session

```powershell
Invoke-RestMethod -Method GET `
  -Uri "http://127.0.0.1:8000/api/session/" `
  -Headers @{ Authorization = "Token $($login.token)" }
```

### 4) Recuperer user/me

```powershell
Invoke-RestMethod -Method GET `
  -Uri "http://127.0.0.1:8000/api/user/me" `
  -Headers @{ Authorization = "Token $($login.token)" }
```

### 5) Retirer un type par ex le type grass mais il faut les remplacer par le types souhaité


```powershell
Invoke-RestMethod -Method DELETE `
  -Uri "http://127.0.0.1:8000/api/group/grass/remove/" `
  -Headers @{ Authorization = "Token $($login.token)" }
```

### 6) Lister les Pokemon accessibles

```powershell
Invoke-RestMethod -Method GET `
  -Uri "http://127.0.0.1:8000/api/pokemon/" `
  -Headers @{ Authorization = "Token $($login.token)" }
```

Afficher toute la liste sans troncature dans PowerShell:

```powershell
$resp = Invoke-RestMethod -Method GET `
  -Uri "http://127.0.0.1:8000/api/pokemon/" `
  -Headers @{ Authorization = "Token $($login.token)" }

$resp.pokemons.Count
$resp.pokemons | Format-Table -AutoSize
```

### 7) Detail d'un Pokemon

```powershell
Invoke-RestMethod -Method GET `
  -Uri "http://127.0.0.1:8000/api/pokemon/bulbasaur/" `
  -Headers @{ Authorization = "Token $($login.token)" }
```

## Notes

- Les endpoints p kemon sont proteges (authentification requise).
- En PowerShell, curl est un alias de Invoke-WebRequest.
- Utilise /api/pokemon/ (avec slash final) pour eviter une redirection qui peut faire perdre le header Authorization.

ù*
# tetst

