#from repository import save_to_database, read_database
from flask import Flask, Response, jsonify, request, make_response
import json
from operator import itemgetter

app = Flask(__name__)

scores = [{"id": 1, "name": "jack", "points":123}, {"id": 2, "name": "hannah", "points": 4567}]

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, DELETE'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# JONNA "Fetching all scores":
@app.route("/scores")
def get_scores():
    return jsonify(scores)

# JONNA "Fetching score based on id": 
@app.route('/scores/<int:the_id>')
def get_scores_id(the_id):
    for score in scores:
        if score["id"] == the_id:
            return jsonify(score), 200
    return make_response ("", 404)

# JONNA "Adding a new score"
@app.route('/scores', methods=['POST'])
def add_score():
    # load given string and turn it into dictionary
    score = json.loads(request.data)
    # generate new score ID
    if scores:
        score_id = scores[-1]['id'] + 1
    else:
        score_id = 1
    # add new score with generated ID
    score['id'] = score_id
    scores.append(score)
    # return success response
    return make_response("", 201)

# JONNA "Deleting a score by id":
@app.route('/scores/<int:the_id>', methods=['DELETE'])
def delete_customer(the_id):
    index_to_be_deleted = -1

    for i in range(0, len(scores)):
        if(scores[i]["id"] == the_id):
            index_to_be_deleted = i
    
    if(index_to_be_deleted != -1):
        scores.pop(index_to_be_deleted)
        return make_response("", 204)
    else:
        return make_response("", 404)

# MATIAS sort scores in asc or desc order
@app.route('/scores/sort', methods=['GET'])
def sort():
    # Extract the 'sort' query parameter from the URL (after "?")
    order = request.args.get('sort')
    # Sort the scores dictionary based on the 'points' field
    if order == 'desc':
        # If the order is desc then the reverse is True
        sorted_scores = sorted(scores, key=itemgetter("points"), reverse=True)
        # Return the sorted scores in JSON format along with a success status code
        return jsonify(sorted_scores), 200
    elif order == 'asc':
        sorted_scores = sorted(scores, key=itemgetter("points"), reverse=False)
        # Return the sorted scores in JSON format along with a success status code in ascending order
        return jsonify(sorted_scores), 200
    else:
        # Return an empty response with a 404 status code if the 'sort' parameter is missing or invalid
        return make_response("", 404)


if __name__ == "__main__":
    app.run()