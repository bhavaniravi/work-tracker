# load db url from the env variable. you can use python-dotenv package

from flask import Flask, request
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.environ["DATABASE_URL"]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

import models



@app.route("/")
def home():
    return {"Status": "Success"}, 200 

@app.route("/work")
def list_work_items():
    result = models.WorkItem.query.filter_by().all()
    print (result)
    return {"Status": "Success", "result": result}


@app.route("/work", methods=["POST"])
def add_work_items():
    params = request.json
    # Dont worry about this for now, 
    # just to show something is possible
    for key in params:
        if key not in dir(models.WorkItem):
            return {"Status": "Error", "result": "Wrong input format"}, 401
    # {"title": "abc"}
    # **params will convert the dict into `title="abc"`
    result = models.WorkItem(**params)
    models.db.session.add(result)
    models.db.session.commit()
    
    return {"Status": "Success", "result": params}, 201

@app.route("/work/<item_id>", methods=["GET"])
def get_work_item(item_id):
    result = models.WorkItem.query.filter_by(id=item_id).first()
    response = {"id": result.id, "title": result.title}
    return {"Status": "Success", "result": response}



# Run the app in port 5000 and in debug mode
if __name__ == '__main__':
    models.db.create_all()
    models.db.init_app(app)
    app.run(port=5000, debug=True)