from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DataRow(db.Model):
    __tablename__ = "DataRow"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    title = db.Column(db.String(100))
    city = db.Column(db.String(100))
