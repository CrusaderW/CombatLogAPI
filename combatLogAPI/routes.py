from flask import request, jsonify
from combatLogAPI import loghandler, ressourcecalculator, masterDF

def init_routes(app, mongo):

    @app.route('/streamLogs', methods=['POST'])
    def streamLogs():
        json_data = request.get_json()
        logStream = loghandler.LogStream(json_data, mongo)
        response = logStream.store()
        logStream.parse()
        #response = logStream.get_response()
        return jsonify(response)


    @app.route('/ressourcecalculator', methods=['GET'])
    def calculateRessources():
        data = {}
        data['item'] = request.args.get('item')
        data['options'] = request.args.get('options')
        resCalc = ressourcecalculator.SingleItem(data)
        response = resCalc.calculate()
        return jsonify(response)


    @app.route('/getLogsByDate', methods=['GET'])
    def getLogsByTimeFrame():
        date = request.args.get('date')
        logQuery = loghandler.LogQuery(mongo)
        response = logQuery.getAllLogsInDateTimeWindow(date)
        return jsonify(response)


    @app.route('/getParsedLogsByDate', methods=['GET'])
    def getParsedLogsByTimeFrame():
        date = request.args.get('date')
        logQuery = loghandler.LogQuery(mongo)
        response = logQuery.getAllParsedLogsInDateTimeWindow(date)
        return jsonify(response)
