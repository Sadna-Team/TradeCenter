from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def clear_database():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("Database cleared")

