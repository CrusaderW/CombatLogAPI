from flask import request, jsonify
from combatLogAPI import logparser

def init_routes(app):

    @app.route('/streamLogs', methods=['POST'])
    def streamLogs():
        json_data = request.get_json()
        logStream = logparser.LogStream(json_data)
        response = logStream.parse()
        return jsonify(response)
