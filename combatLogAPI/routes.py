from flask import request, jsonify
from combatLogAPI import loghandler, masterDF

def init_routes(app, mongo):

    @app.route('/streamLogs', methods=['POST'])
    def streamLogs():
        json_data = request.get_json()
        logStream = loghandler.LogStream(json_data, mongo)
        response = logStream.store()
        #logStream.parse()
        #response = logStream.get_response()
        return jsonify(response)


    @app.route('/getLogsByDate', methods=['GET'])
    def getLogsByTimeFrame():
        date = request.args.get('date')
        logQuery = loghandler.LogQuery(mongo)
        response = logQuery.getAllLogsInDateTimeWindow(date)
        return jsonify(response)
