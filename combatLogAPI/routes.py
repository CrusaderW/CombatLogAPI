from flask import request, jsonify
from combatLogAPI import logparser

def init_routes(app):

    @app.route('/streamLogs', methods=['POST'])
    def streamLogs():
        json_data = request.get_json()
        logStream = logparser.LogStream(json_data)
        logStream.parse()
        response = logStream.get_response()
        return jsonify(response)
