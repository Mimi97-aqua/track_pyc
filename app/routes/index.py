from flask import Blueprint, jsonify, request

index_route = Blueprint('index', __name__)


@index_route.route('/', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'TRACE'])
def index():
    if request.method == 'GET':
        return jsonify({
            'status': 'success',
            'message': 'Welcome to Track PYC!'
        }), 200
    else:
        return jsonify({
            'status': 'error',
            'message': 'Invalid HTTP Method'
        }), 405
