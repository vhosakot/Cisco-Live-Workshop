#! /usr/bin/python

########################################
#                                      #
# Implements a REST server using flask #
#                                      #
########################################

from flask import abort
from flask import Flask, jsonify
from flask import request

app = Flask(__name__)

responses = [
    {
        'id'   : 1,
        'event': u'Cisco Live',
        'city' : u'Las Vegas'
    }
]


# HTTP GET
@app.route('/api/v1.0/responses', methods=['GET'])
def get_responses():
    return jsonify({'responses': responses})


# HTTP POST
@app.route('/api/v1.0/responses', methods=['POST'])
def create_response():
    if not request.json or not 'event' in request.json:
        abort(400)
    response = {
        'id'   : responses[-1]['id'] + 1,
        'event': request.json['event'],
        'city' : request.json.get('city', "")
    }
    responses.append(response)
    return jsonify({'response': response}), 201


# HTTP PUT
@app.route('/api/v1.0/responses/<int:response_id>', methods=['PUT'])
def update_response(response_id):
    response = \
      [response for response in responses if response['id'] == response_id]
    if len(response) == 0:
        abort(404)
    if not request.json:
        abort(400)
    response[0]['event'] = request.json.get('event', response[0]['event'])
    response[0]['city']  = request.json.get('city', response[0]['city'])
    return jsonify({'response': response[0]})


# HTTP DELETE
@app.route('/api/v1.0/responses/<int:response_id>', methods=['DELETE'])
def delete_response(response_id):
    response = \
      [response for response in responses if response['id'] == response_id]
    if len(response) == 0:
        abort(404)
    responses.remove(response[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(host='127.0.100.100',port=9876,debug=True)
