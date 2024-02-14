import psycopg2
from config import Postgres


# The Database class that implements the Singleton pattern
class Database():
    _connection = None

    def __init__(self):
        raise RuntimeError('Call connect() instead')

    @classmethod
    def connect(cls):
        if cls._connection is None:
            print('Creating new instance')
            cls._connection = cls.__new__(cls)
            # Connection to the PostgreSQL database
            con = psycopg2.connect(
                database=Postgres.DATABSE,
                user=Postgres.USER,
                password=Postgres.PASSWORD,
                host=Postgres.HOST,
                port=Postgres.PORT
            )
            cls._connection = con
        return cls._connection


if __name__ == '__main__':
    try:
        con = Database.connect()
        print("Pomyslnie polaczono!")
    except Exception as ex:
        print("Wystapil wyjatek! " + str(ex))
