
from application.app import app
from application.models import WorkItem, db
from flask import request

@app.route("/")
def home():
    return {"Status": "Success"}, 200 

@app.route("/work")
def list_work_items():
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
    response = {"id": result.id, "title": result.title}
    return {"Status": "Success", "result": response}
