#from repository import save_to_database, read_database
from flask import Flask, Response, jsonify, request, make_response
import json

app = Flask(__name__)

scores = [{"id": 1, "name": "jack", "rating":123}, {"id": 2, "name": "hannah", "rating": 4567}]

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
    
@app.route('/scores/sort=<string:order>')
def sort(order):
    print(f"Order: {order}")
    reverse = False
    if order == "desc":
        reverse = True
    sorted_scores = sorted(scores, key=lambda x: int(x["rating"]), reverse=reverse)
    return jsonify(sorted_scores), 200


if __name__ == "__main__":
    app.run()