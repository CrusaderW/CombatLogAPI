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

#This is untested, but should give you in idea what data needs to be in mongodb.
def init_mongo(mongo):
    mongo.db.createCollection('constants')
    db.constants.insert({"NPCs":[
{"id":"1","name":"Ancient Goliath Spider","last_seen":"2020-02-16","added_by":"0"},
{"id":"2","name":"Ancient Mountain Auroch","last_seen":"2020-02-16","added_by":"0"},
{"id":"3","name":"Aracoix Assassin","last_seen":"2020-02-16","added_by":"0"},
{"id":"4","name":"Aracoix Assassin Elite","last_seen":"2020-02-16","added_by":"0"},
{"id":"5","name":"Aracoix Druid","last_seen":"2020-02-16","added_by":"0"},
{"id":"6","name":"Aracoix Druid Chief","last_seen":"2020-02-16","added_by":"0"},
{"id":"7","name":"Goliath Spider","last_seen":"2020-02-18","added_by":"0"},
{"id":"8","name":"Hellcat Slasher","last_seen":"2020-04-25","added_by":"0"},
{"id":"9","name":"Jumping Spider","last_seen":"2020-02-16","added_by":"0"},
{"id":"10","name":"Recluse Spider","last_seen":"2020-02-16","added_by":"0"},
{"id":"11","name":"Satyr Knight Chief","last_seen":"2020-02-16","added_by":"0"},
{"id":"12","name":"Spider Queen","last_seen":"2020-02-16","added_by":"0"},
{"id":"13","name":"Urgu Champion","last_seen":"2020-02-18","added_by":"0"},
{"id":"14","name":"Urgu Champion Chief","last_seen":"2020-02-16","added_by":"0"},
{"id":"15","name":"Urgu Myrmidon","last_seen":"2020-02-18","added_by":"0"},
{"id":"16","name":"Urgu Myrmidon Elite","last_seen":"2020-02-16","added_by":"0"},
{"id":"17","name":"Urgu Ranger","last_seen":"2020-02-18","added_by":"0"},
{"id":"18","name":"Wolf Spider","last_seen":"2020-02-18","added_by":"0"},
{"id":"19","name":"Urgu Ranger Elite","last_seen":"2020-02-18","added_by":"0"},
{"id":"21","name":"Aracoix Druid Boss","last_seen":"2020-02-16","added_by":"17"},
{"id":"22","name":"Aracoix Druid Elite","last_seen":"2020-02-16","added_by":"17"},
{"id":"23","name":"Urgu Champion Elite","last_seen":"2020-02-18","added_by":"17"},
{"id":"24","name":"Urgu Ranger Boss","last_seen":"2020-02-18","added_by":"17"},
{"id":"25","name":"Knotwood","last_seen":"2020-04-28","added_by":"17"},
{"id":"26","name":"Urgu Champion Boss","last_seen":"2020-02-18","added_by":"17"},
{"id":"27","name":"Urgu Myrmidon Boss","last_seen":"2020-02-16","added_by":"17"},
{"id":"28","name":"Satyr Ranger","last_seen":"2020-02-16","added_by":"17"},
{"id":"29","name":"Satyr Templar Captain","last_seen":"2020-02-16","added_by":"17"},
{"id":"30","name":"Practice Dummy","last_seen":"2020-02-16","added_by":"17"},
{"id":"31","name":"Hunger Crystal","last_seen":"2020-02-16","added_by":"17"},
{"id":"32","name":"Iron","last_seen":"2020-02-16","added_by":"17"},
{"id":"33","name":"Ore Mega Node","last_seen":"2020-02-16","added_by":"17"},
{"id":"34","name":"Slag","last_seen":"2020-04-24","added_by":"17"},
{"id":"35","name":"Stone Mega Node","last_seen":"2020-04-28","added_by":"17"},
{"id":"36","name":"Copper","last_seen":"2020-04-18","added_by":"17"},
{"id":"37","name":"Gold","last_seen":"2020-02-16","added_by":"17"},
{"id":"38","name":"Silver","last_seen":"2020-02-16","added_by":"17"},
{"id":"39","name":"Tin","last_seen":"2020-02-16","added_by":"17"},
{"id":"40","name":"Satyr Confessor Captain","last_seen":"2020-02-16","added_by":"17"},
{"id":"41","name":"Boss Spider","last_seen":"2020-02-16","added_by":"17"},
{"id":"42","name":"Satyr Cleric Elite","last_seen":"2020-02-16","added_by":"17"},
{"id":"43","name":"Satyr Knight","last_seen":"2020-02-16","added_by":"17"},
{"id":"44","name":"Satyr Templar","last_seen":"2020-02-16","added_by":"17"},
{"id":"45","name":"Red Elk","last_seen":"2020-04-28","added_by":"17"},
{"id":"46","name":"Hellcat Ambusher","last_seen":"2020-04-25","added_by":"17"},
{"id":"47","name":"Onyx Auroch","last_seen":"2020-04-28","added_by":"17"},
{"id":"48","name":"Mountain Auroch","last_seen":"2020-02-16","added_by":"17"},
{"id":"49","name":"Plains Elk","last_seen":"2020-04-07","added_by":"17"},
{"id":"50","name":"Satyr Cleric","last_seen":"2020-02-16","added_by":"17"},
{"id":"51","name":"Satyr Confessor Elite","last_seen":"2020-02-16","added_by":"17"},
{"id":"52","name":"Satyr Templar Chief","last_seen":"2020-02-16","added_by":"17"},
{"id":"53","name":"Aracoix Druid Captain","last_seen":"2020-02-16","added_by":"17"},
{"id":"54","name":"Cobblestone","last_seen":"2020-04-24","added_by":"17"},
{"id":"55","name":"Muskhog Berserker","last_seen":"2020-02-16","added_by":"17"},
{"id":"56","name":"Hellcat Hunter","last_seen":"2020-04-28","added_by":"17"},
{"id":"57","name":"Aracoix Druid King","last_seen":"2020-02-16","added_by":"17"},
{"id":"58","name":"Hellcat Mauler","last_seen":"2020-02-16","added_by":"17"},
{"id":"59","name":"Painted Auroch","last_seen":"2020-04-07","added_by":"17"},
{"id":"60","name":"Risen Grunt","last_seen":"2020-02-16","added_by":"17"},
{"id":"61","name":"Urgu Champion Captain","last_seen":"2020-02-16","added_by":"17"},
{"id":"62","name":"Urgu Ranger Captain","last_seen":"2020-02-16","added_by":"17"},
{"id":"63","name":"Ancient Jumping Spider R5","last_seen":"2020-02-16","added_by":"17"},
{"id":"64","name":"Ancient Wolf Spider R10","last_seen":"2020-02-16","added_by":"17"},
{"id":"65","name":"Aracoix Assassin Captain","last_seen":"2020-02-16","added_by":"17"},
{"id":"66","name":"Projectile","last_seen":"2020-02-16","added_by":"17"},
{"id":"67","name":"Ancient Hellcat Slasher R5","last_seen":"2020-02-16","added_by":"17"},
{"id":"68","name":"Ancient Jumping Spider","last_seen":"2020-02-16","added_by":"17"},
{"id":"69","name":"Ancient Wolf Spider","last_seen":"2020-02-16","added_by":"17"},
{"id":"70","name":"Satyr Confessor","last_seen":"2020-02-16","added_by":"17"},
{"id":"71","name":"Satyr Templar Elite","last_seen":"2020-02-16","added_by":"17"},
{"id":"72","name":"Ancient Jumping Spider R6","last_seen":"2020-02-16","added_by":"17"},
{"id":"73","name":"Ancient Wolf Spider R9","last_seen":"2020-02-16","added_by":"17"},
{"id":"74","name":"Urgu Myrmidon Chief","last_seen":"2020-02-16","added_by":"17"},
{"id":"75","name":"White Wolf","last_seen":"2020-02-16","added_by":"17"},
{"id":"76","name":"Shadow Wolf","last_seen":"2020-04-24","added_by":"17"},
{"id":"77","name":"Stronghold Guard","last_seen":"2020-04-24","added_by":"17"},
{"id":"78","name":"Satyr Cleric Enbarri","last_seen":"2020-02-16","added_by":"17"},
{"id":"79","name":"Satyr Knight Elite","last_seen":"2020-02-16","added_by":"17"},
{"id":"80","name":"Enbarri Chief","last_seen":"2020-02-16","added_by":"17"},
{"id":"81","name":"Enbarri Elite","last_seen":"2020-04-28","added_by":"17"},
{"id":"82","name":"Enbarri Minion","last_seen":"2020-04-28","added_by":"17"},
{"id":"83","name":"Urgu Chief","last_seen":"2020-02-16","added_by":"17"},
{"id":"84","name":"Urgu Elite","last_seen":"2020-04-07","added_by":"17"},
{"id":"85","name":"Urgu Minion","last_seen":"2020-04-28","added_by":"17"},
{"id":"86","name":"Plague Seed","last_seen":"2020-02-16","added_by":"17"},
{"id":"87","name":"Outpost Guard","last_seen":"2020-04-24","added_by":"17"},
{"id":"88","name":"Satyr Elite","last_seen":"2020-04-28","added_by":"17"},
{"id":"89","name":"Satyr Minion","last_seen":"2020-04-28","added_by":"17"},
{"id":"90","name":"Satyr Ranger Elite","last_seen":"2020-02-16","added_by":"17"},
{"id":"91","name":"Dusk Elk","last_seen":"2020-02-16","added_by":"17"},
{"id":"92","name":"Gray Wolf","last_seen":"2020-04-24","added_by":"17"},
{"id":"93","name":"Satyr Knight King","last_seen":"2020-02-16","added_by":"17"},
{"id":"95","name":"River Auroch","last_seen":"2020-04-04","added_by":"44"}
]})
