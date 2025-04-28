from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DataRow(db.Model):

    __tablename__ = "DataRow"
    __sqlite_autoincrement__ = True
    __table_args__ = {"extend_existing": True}

    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    title = db.Column(db.String(100))
    city = db.Column(db.String(100))

    def __repr__(self):
        return f"<DataRow: {self.name}, {self.title}, {self.city}>"
