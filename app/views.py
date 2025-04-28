import os
from collections import namedtuple
from flask import Flask, jsonify, request, render_template
from sqlalchemy import select
from app import app
from app.config import getsettings
from app.models import DataRow, db
from sqlite3.dbapi2 import DatabaseError, IntegrityError, OperationalError
from datetime import datetime

db.init_app(app)


@app.route("/upload", methods=["POST", "PUT"])
def upload():
    """Upload a file pipe-delimited file and save its contents to a database."""
    print(request.headers)
    data_wrapper = []
    current_data = check_db()
    columns = DataRow.__table__.columns.keys()[1:]
    collect_data = namedtuple("collect_data", columns)
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file:
        now = datetime.now()
        file.filename = f"{now.strftime('%Y%m%d%H%M%S')}_{file.filename}"
        filepath = os.path.join(getsettings().UPLOAD_FOLDER, file.filename)
        os.makedirs(getsettings().UPLOAD_FOLDER, exist_ok=True)
        file.save(filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            if len(f.readlines()) == 0:  # there is a better way of doing this
                return jsonify({"error": "File is empty"}), 400
            else:
                f.seek(0)  # Reset file pointer to the beginning
                next(f)  # remember to skip the header line of the file
                for line in f:
                    parts = line.strip().split("|")

                    if parts not in current_data:
                        collect_data_entry = collect_data._make(parts)
                        data_wrapper.append(collect_data_entry)
                        row = DataRow(**collect_data_entry._asdict())
                        db.session.add(row)
                    else:
                        return (
                            jsonify({"error": f"Duplicate entry found: {parts}"}),
                            400,
                        )
                try:
                    db.session.commit()
                    return (
                        jsonify(
                            {
                                "message": "File uploaded successfully",
                                "data": data_wrapper,
                            }
                        ),
                        200,
                    )
                except (DatabaseError, OperationalError) as e:
                    print(f"Error: {e}")
                    db.session.rollback()
                    return jsonify({"error": "No file uploaded"}), 400
    else:
        return jsonify({"error": "No file uploaded"}), 500


@app.route("/login", methods=["POST", "GET"])
def login():
    print(request.method)
    print(request.form)
    if request.method == "POST":
        username = request.form.get("email", "nothing Entered")
        password = request.form.get("password", "nothing Entered")
        print(f"Username: {username}")
        print(f"Password: {password}")
        return "Data received"
    else:
        return render_template("login.html")


@app.route("/success", methods=["POST", "GET"])
def success():
    """Return a success message."""
    print(request.method)
    req = request.headers
    return f"this is success .. \n {req} \n"


@app.route("/view_db", methods=["GET"])
def view_db():
    """View the contents of the database."""
    select_data = select(DataRow)
    results = db.session.execute(select_data).scalars().all()
    data = [row.__dict__ for row in results]
    for row in data:
        row.pop("_sa_instance_state", None)
        print(row)
    return render_template("view_db.html", data=data), 200


@app.route("/create_db/<key>", methods=["POST", "GET"])
def create_db(key):
    """Create the database."""
    if key == getsettings().key.strip():

        try:
            db.create_all()
            return jsonify({"message": "Database created successfully"}), 200
        except (DatabaseError, IntegrityError) as e:
            print(f"Error: {e}")
            db.session.rollback()
            return jsonify({"error": "Database already exists"}), 400
    else:
        return jsonify({"error": "Invalid key"}), 403


def check_db():
    """Check the database for existing entries."""
    search = select(DataRow)
    results = db.session.execute(search).scalars().all()
    data = [row.__dict__ for row in results]
    for row in data:
        row.pop("_sa_instance_state", None)

    return data
