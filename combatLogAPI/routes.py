from flask import request, jsonify
from combatLogAPI import logparser, masterDF

def init_routes(app):

    @app.route('/streamLogs', methods=['POST'])
    def streamLogs():
        json_data = request.get_json()
        logStream = logparser.LogStream(json_data)
        response = logStream.store()
        #logStream.parse()
        #response = logStream.get_response()
        return jsonify(response)


    @app.route('/getAllLogs', methods=['GET'])
    def getLogsByTimeFrame():
        #reqData = request.data()
        masterdf = masterDF.masterDF()
        response = masterdf.collect()
        #response = True
        return jsonify(response)
