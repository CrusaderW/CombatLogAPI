import os
from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from combatLogAPI import routes
from combatLogAPI import db_credentials

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # initialize db connection
    print(db_credentials.user + db_credentials.pw)
    app.config["MONGO_URI"] = "mongodb://"+ db_credentials.user +":"+ db_credentials.pw +"@localhost:27017/Crowfall"
    mongo = PyMongo(app)

    #enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    routes.init_routes(app, mongo)

    return app
