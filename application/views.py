
from application.app import app
from application.models import WorkItem, db, SubTask, User
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

@app.route("/")
def home():
    return {"Status": "Success"}, 200 

@app.route("/signup", methods=["POST"])
def signup():
    params = request.authorization
    try:
        user = User(**params)
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        return {"Status": "Error", "result": "User already exists"}, 400
    return {"Status": "Success", "result": "User created"}



@app.route("/login", methods=["POST"])
def login():
    params = request.authorization
    if authenticate(params):
        return {"Status": "Success", "result": "User logged in"}

def authenticate(params):
    # checks with the DB
    # returns if it's a valid user
    try:
        user = User.query.filter_by(username=params["username"]).first()
        return user and user.password == params["password"]
    except (KeyError, TypeError):
        return False

@app.route("/work")
def list_work_items():
    auth_info = request.authorization or {}
    if not authenticate(auth_info):
        return {"Status": "Error", "result": "User not autheniticated"}

    if authenticate(auth_info):
        result = WorkItem.query.filter_by().all()
        response = [{"id": res.id, "title":res.title} for res in result]
        return {"Status": "Success", "result": response}


@app.route("/work", methods=["POST"])
def add_work_items():

    params = request.json
    # Dont worry about this for now, 
    # just to show something is possible
    for key in params:
        if key not in dir(WorkItem):
            return {"Status": "Error", "result": "Wrong input format"}, 401
    # {"title": "abc"}
    # **params will convert the dict into `title="abc"`
    result = WorkItem(**params)
    db.session.add(result)
    db.session.commit()
    
    return {"Status": "Success", "result": params}, 201

@app.route("/work/<item_id>", methods=["GET"])
def get_work_item(item_id):
    result = WorkItem.query.filter_by(id=item_id).first()
    if result:
        response = {"id": result.id, "title": result.title}
        return {"Status": "Success", "result": response}
    else:
        return {"Status": "Error"}, 404

@app.route("/work/<item_id>/task", methods=["GET"])
def get_sub_task(item_id):
    result = SubTask.query.filter_by(work_item_id=item_id).all()
    response = []
    for row in result:
        response.append({"id": row.id, "title": row.title})
    return {"Status": "Success", "result": response}


@app.route("/work/<item_id>/task", methods=["POST"])
def add_sub_task(item_id):
    result = WorkItem.query.filter_by(id=item_id).first()
    if not result:
        return {"Status": "Error"}, 404

    params = request.json
    for key in params:
        if key not in dir(SubTask):
            return {"Status": "Error", "result": "Wrong input format"}, 401

    params["work_item_id"] = item_id
    result = SubTask(**params)
    db.session.add(result)
    db.session.commit()
    
    return {"Status": "Success", "result": params}, 201
