from flask import request, jsonify
from combatLogAPI import loghandler, masterDF#, ressourcecalculator,

def init_routes(app, mongo):

    @app.route('/streamLogs', methods=['POST'])
    def streamLogs():
        json_data = request.get_json()
        logStream = loghandler.LogStream(json_data, mongo)
        response = logStream.store()
        logStream.parse()
        #response = logStream.get_response()
        return jsonify(response)
    '''
    @app.route('/ressourcecalculator', methods=['GET'])
    def calculateRessources():
        data = {}
        data['item'] = request.args.get('item')
        data['options'] = request.args.get('options')
        resCalc = ressourcecalculator.SingleItem(data)
        response = resCalc.calculate()
        return jsonify(response)
    '''
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


    @app.route('/getMyPersonalLogs', methods=['GET'])
    def getMyPersonalLogs():
        date = request.args.get('date')
        username = request.args.get('username')
        logQuery = loghandler.LogQuery(mongo)
        response = logQuery.getMyPersonalLogs(date, username)
        return jsonify(response)


    @app.route('/getNPCs', methods=['GET'])
    def getNPCNames():
        logQuery = loghandler.LogQuery(mongo)
        response = logQuery.getNPCs()
        return jsonify(response)
