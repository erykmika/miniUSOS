import psycopg2
import json

def connect():
    # Wczytanie danych dostepowych do bazy danych
    login_data = None
    with open("database_creds.json", "r") as creds:
        login_data = json.loads(creds.read())
    # Polaczenie z baza danych PostgreSQL
    con = psycopg2.connect(
        database=login_data["database"],
        user=login_data["user"],
        password=login_data["password"],
        host=login_data["host"],
        port=login_data["port"]
    )
    return con

if __name__ == '__main__':
    try:
        con = connect()
        print("Pomyslnie polaczono!")
    except Exception as ex:
        print("Wystapil wyjatek! " + str(ex))
