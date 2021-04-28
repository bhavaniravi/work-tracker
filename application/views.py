
from application.app import app
from application.models import WorkItem, db, SubTask, User
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from flask_jwt import jwt_required, JWT, current_identity


def identity(payload):
    user_id = payload['identity']
    print (user_id)
    return User.query.filter_by(id=user_id).first()

def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        return user 

jwt = JWT(app, authenticate, identity)

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

# /login is replaced with /auth 

@app.route("/work")
@jwt_required()
def list_work_items():
    # 
    result = WorkItem.query.filter_by(created_by=current_identity.id).all()
    response = [{"id": res.id, "title":res.title} for res in result]
    return {"Status": "Success", "result": response}


@app.route("/work/shared")
@jwt_required()
def shared_work_items():
    # Page.query.with_parent(some_tag)
    result = WorkItem.query.with_parent(current_identity).all()
    response = [{"id": res.id, "title":res.title, "created_by": res.created_by, "current_user": current_identity.id} for res in result]
    return {"Status": "Success", "result": response}


@app.route("/work", methods=["POST"])
@jwt_required()
def add_work_items():

    params = request.json
    # Dont worry about this for now, 
    # just to show something is possible
    for key in params:
        if key not in dir(WorkItem):
            return {"Status": "Error", "result": "Wrong input format"}, 401
    # {"title": "abc"}
    # **params will convert the dict into `title="abc"`

    params["created_by"] = current_identity.id
    params["shared_with"] = [User.query.filter_by(id=user_id).first() for user_id in params["shared_with"]]
    result = WorkItem(**params)
    db.session.add(result)
    db.session.commit()
    
    return {"Status": "Success", "result": {"title": result.title}}, 201

@app.route("/work/<item_id>", methods=["GET"])
@jwt_required()
def get_work_item(item_id):
    result = WorkItem.query.filter_by(id=item_id).first()
    if result:
        response = {"id": result.id, "title": result.title}
        return {"Status": "Success", "result": response}
    else:
        return {"Status": "Error"}, 404

@app.route("/work/<item_id>/task", methods=["GET"])
@jwt_required()
def get_sub_task(item_id):
    result = SubTask.query.filter_by(work_item_id=item_id).all()
    response = []
    for row in result:
        response.append({"id": row.id, "title": row.title})
    return {"Status": "Success", "result": response}


@app.route("/work/<item_id>/task", methods=["POST"])
@jwt_required()
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
