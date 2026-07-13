# Selfee - API Django Pokedex

API Django qui gere l'authentification (session + token) et la gestion de groupes Pokemon par type.

## Prerequis

- Python 3.11+
- pip

## Installation (PowerShell)

```powershell
cd C:\Users\bapti\Desktop\Selfee
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install Django djangorestframework requests
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

Base URL locale: `http://127.0.0.1:8000`

## Lancer les tests

```powershell
python manage.py test
```

Test cible (groupes):

```powershell
python manage.py test Pokedex_selfee.Pokedex_App.tests.test_group_views
```

## Endpoints principaux

### Auth

- `GET /api/hello/`
- `POST /api/login/`
- `GET /api/session/`
- `POST /api/logout/`
- `DELETE /api/logout/`
- `GET /api/user/me`

### Groupes Pokemon

- `POST /api/group/<pokemon_type>/add/`
- `DELETE /api/group/<pokemon_type>/remove/`

## Commande à utiliser dans le shell

### 1) Login (PowerShell)


j'ai utiliser un superutilisateur pour les différentes opération mais on peut le faire avec user classique, je n'ai juste pas la route register car ce n'est pas demander dans ce test.

python manage.py createsuperuser

```powershell

$body = @{ username = "bnjjs"; password = "1234" } | ConvertTo-Json -Compress
$login = Invoke-RestMethod -Method POST `
  -Uri "http://127.0.0.1:8000/api/login/" `
  -ContentType "application/json" `
  -Body $body

$login
```
### 2) Ajouter un type au user connecte

Avec cookie de session actif (apres login)
```powershell
curl -X POST http://127.0.0.1:8000/api/group/grass/add/
```

### 3) Supprimer un type (PowerShell)

```powershell
$body = @{ username = "bnjjs"; password = "1234" } | ConvertTo-Json -Compress
$login = Invoke-RestMethod -Method POST `
  -Uri "http://127.0.0.1:8000/api/login/" `
  -ContentType "application/json" `
  -Body $body

Invoke-RestMethod -Method POST `
  -Uri "http://127.0.0.1:8000/api/group/grass/add/" `
  -Headers @{ Authorization = "Token $($login.token)" }

Invoke-RestMethod -Method DELETE `
  -Uri "http://127.0.0.1:8000/api/group/grass/remove/" `
  -Headers @{ Authorization = "Token $($login.token)" }
  
```
 Invoke-RestMethod -Method GET `
  -Uri "http://127.0.0.1:8000/api/user/me" `
  -Headers @{ Authorization = "Token $($login.token)" } 

## Notes

- Les endpoints de groupes sont proteges: utilisateur authentifie requis.
- La base par defaut est SQLite (`db.sqlite3`).
- En PowerShell, `curl` est un alias de `Invoke-WebRequest`, donc la syntaxe `-H/-d` style cURL ne fonctionne pas.
- Sur ce projet j'utilise Invoke-RestMethod`.
