from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, json
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os
import requests

load_dotenv()
uri = os.getenv('MONGO_URL')
# Create a new client and connect to the server 
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.dbtest
collection = db["flask_tutrials"]
app = Flask(__name__)
app.secret_key = "demoflaskapplication"

@app.route("/")
def home():
    return render_template("index.html", hello="Hello World")

@app.route("/api/submittodoitem", methods=["GET", "POST"])
def users_create():
    if request.method == "POST":
        data = request.form   

        errors = []
        if not data.get("name"):
            errors.append("Name is required")
        if not data.get("description"):
            errors.append("Description is required")
        
        if errors:
            # Show validation errors on same page
            for err in errors:
                flash(err, "error")
            print(errors)
            return render_template("todo.html", data=data)
            
        db.users.insert_one(dict(data))
        return redirect(url_for("success", message="Data submitted successfully"))
    return render_template("todo.html", data=[])


@app.route("/api/users/create", methods=["GET", "POST"])
def users_create():
    if request.method == "POST":
        data = request.form   

        errors = []
        if not data.get("username"):
            errors.append("Username is required")
        if not data.get("email") or "@" not in data.get("email"):
            errors.append("Valid email is required")
        
        if errors:
            # Show validation errors on same page
            for err in errors:
                flash(err, "error")
            print(errors)
            return render_template("create_user.html", data=data)
            
        db.users.insert_one(dict(data))
        return redirect(url_for("success", message="Data submitted successfully"))
    return render_template("create_user.html", data=[])

@app.route("/api/users/post", methods=["POST"])
def users_post():
    data = request.form   

    errors = []

    if not data.get("username"):
        errors.append("Username is required")
    if not data.get("email") or "@" not in data.get("email"):
        errors.append("Valid email is required")
    print(errors)
    if errors:
        # Show validation errors on same page
        for err in errors:
            flash(err, "error")
        return render_template("create_user.html")
        
    db.users.insert_one(dict(data))
    return redirect(url_for("success", message="Data submitted successfully"))
    #return "Data inserted"

@app.route("/api/success")
def success():
    return render_template("success.html", message=request.values.get("message"))

@app.route("/api/users")
def users():
    data = db.flask_tutrials.find()
    data = list(data)
    for item in data:
        del item["_id"]
    print(data)
    return data

@app.route("/api")
def getData():
    data = {"name":"Ram", "age": 34}
    # Save it to a file
    with open("test.json", "w") as file:
        json.dump(data, file, indent=2)
    
    # (Optional) Read it back if you want
    with open("test.json", "r") as read_file:
        saved_data = json.load(read_file)
    return jsonify(saved_data)

if __name__ == "__main__":
    app.run("localhost", port=5001, debug=True)
