from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

class SingletonSQLAlchemy:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingletonSQLAlchemy, cls).__new__(cls, *args, **kwargs)
            cls._instance.db = SQLAlchemy()
        return cls._instance

    def get_db(self):
        return self.db

db = SingletonSQLAlchemy().get_db()


def clear_database():
    db_instance = SingletonSQLAlchemy().get_db()
    engine = db_instance.engine
    connection = engine.connect()

    try:
        trans = connection.begin()
        for table in reversed(db_instance.metadata.sorted_tables):
            connection.execute(table.delete())
        trans.commit()
    except Exception as e:
        trans.rollback()
        print(f"Error occurred: {e}")
    finally:
        connection.close()
        print('Database cleared!')