import psycopg2
import json

# The Database class that implements the Singleton pattern
class Database():
    _connection = None

    def __init__(self):
        raise RuntimeError('Call connect() instead')

    @classmethod
    def connect(cls):
        if cls._connection is None:
            #print('Creating new instance')
            cls._connection = cls.__new__(cls)
            # Wczytanie danych dostepowych do bazy danych
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
            cls._connection = con
        return cls._connection


if __name__ == '__main__':
    try:
        con = Database.connect()
        print("Pomyslnie polaczono!")
    except Exception as ex:
        print("Wystapil wyjatek! " + str(ex))
