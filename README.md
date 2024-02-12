# miniUSOS

Projekt na kurs Bazy danych 2.

## Tech stack / Użyte technologie

* Python
* Flask
* PostgreSQL

## Instalacja

Kod aplikacji umieszczony jest w katalogu */app*. Należy w nim umieścić plik *database_creds.json*, który zawiera dane dostępowe do bazy danych PostgreSQL. Format pliku jest następujący:

```json
{
    "database": "<nazwa bazy danych>", 
    "user": "<nazwa użytkownika>",
    "password": "<hasło>",
    "host": "<adres>",
    "port": "<domyślnie 5432>"
}
```
Plik miniusos.sql zawiera skrypt tworzący strukturę bazy danych PostgreSQL wraz z wstawieniem przykładowych rekordów. Wszystkie hasła studentów i prowadzących to '123'.

### Utworzenie i aktywacja środowiska wirtualnego
```sh
cd ./app
python -m venv ./env
./env/scripts/activate
```

### Instalacja zależności
```sh
pip install -r requirements.txt
```

### Uruchomienie aplikacji
```sh
flask --app strona run
```

### Przejdź do **localhost:5000**
