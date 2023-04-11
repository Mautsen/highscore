from flask import Flask, Response, jsonify, request, make_response, render_template
import json
from operator import itemgetter
from repository import *
import requests



app = Flask(__name__)

#scores = [{"id": 1, "name": "jack", "points":123}, {"id": 2, "name": "hannah", "points": 4567}]

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, DELETE'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# JONNA & MATIAS "Fetching all scores":
@app.route("/scores")
def get_scores():
    scores=read_scores()
    # Copy the scores list to avoid modifying the original list.
    sorted_scores = scores
    # Get the 'sort' query parameter from the request, which specifies how to sort the scores.
    sort = request.args.get("sort")
    # If the 'sort' parameter is set to 'asc', sort the scores list in ascending order.
    if sort == "asc":
        sorted_scores = sorted(sorted_scores, key=lambda s: s["points"])
    # If the 'sort' parameter is set to 'desc', sort the scores list in descending order.
    elif sort == "desc":
        sorted_scores = sorted(sorted_scores, key=lambda s: s["points"], reverse=True)
    # Get the 'limit' query parameter from the request, which specifies the maximum number of scores to return.
    limit = request.args.get("limit")
    # If the 'limit' parameter is set, slice the sorted scores list to return only the first 'limit' scores.
    if limit:
        sorted_scores = sorted_scores[:int(limit)]
    # Return the sorted and limited scores list as a JSON response.
    return jsonify(sorted_scores)

# JONNA "Fetching score based on id": 
@app.route('/scores/<int:the_id>')
def get_scores_id(the_id):
    scores = read_scores()
    for score in scores:
        if score["id"] == the_id:
            return jsonify(score), 200
    return make_response ("", 404)

# JONNA "Adding a new score"
# @app.route('/scores', methods=['POST'])
# def add_score():
#     # load given string and turn it into dictionary
#     score = json.loads(request.data)
#     # score = request.json
#     scores = read_scores()
#     # generate new score ID
#     if scores:
#         score_id = scores[-1]['id'] + 1
#     else:
#         score_id = 1
#     # add new score with generated ID
#     score['id'] = score_id
#     scores.append(score)
#     # save updated scores
#     save_to_scores(scores)
#     # return success response
#     return make_response("", 201)

@app.route('/scores', methods=['POST'])
def add_score():
    # load given JSON data and turn it into dictionary
    score = request.get_json()
    if not score:
        return make_response("Invalid JSON data", 400)
    scores = read_scores()
    # generate new score ID
    if scores:
        score_id = scores[-1]['id'] + 1
    else:
        score_id = 1
    # add new score with generated ID
    score['id'] = score_id
    scores.append(score)
    # save updated scores
    save_to_scores(scores)
    # return success response
    return make_response("", 201)

# JONNA "Deleting a score by id":
@app.route('/scores/<int:the_id>', methods=['DELETE'])
def delete_customer(the_id):
    scores = read_scores()
    index_to_be_deleted = -1

    for i in range(0, len(scores)):
        if(scores[i]["id"] == the_id):
            index_to_be_deleted = i
    
    if(index_to_be_deleted != -1):
        scores.pop(index_to_be_deleted)
        # tallennetaan
        save_to_scores(scores)
        return make_response("", 204)
    else:
        return make_response("", 404)

# MATIAS sort scores in asc or desc order
@app.route('/scores', methods=['GET'])
def sort():
    scores = read_scores() 
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
    
#MATIAS limit how many scores are shown
@app.route('/scores', methods=['GET'])
def limit():
    scores = read_scores()
    # finds the limit from url
    limit = request.args.get('limit')

    limit = int(limit)

    #If there is no limit found, return error
    if limit is None:
        return "Limit parameter missing", 400
    #The limit must be in integer
    try:
        limit = int(limit)
    except ValueError:
        return "Limit parameter is not a valid integer", 400

    #Initialize an empty list to hold the scores within the limit
    results = []
    for i in range(0, limit):
        # If i is greater than or equal to the length of scores, break the loop
        if i >= len(scores):
            break
        else: # Otherwise, append the ith score to the results list
            results.append(scores[i])

    return jsonify(results), 200

@app.route('/', methods = ['POST', 'GET'])
def index():
    """
    The index function that handles both GET and POST requests to the root route. When a GET request is made,
    the function reads the data from the database and renders the index.html template with an empty form.
    When a POST request is made, the function reads the form data, validates the name and saves the data to the database.
    It then reads the updated data from the database and renders the index.html template with the updated data.

    Returns:
        str: the rendered HTML template as a string.
    """ 

    if request.method == 'POST':
        name = request.form.get('name')
        points = request.form.get('points')
        score = {'name': name, 'points': points}
        resp = requests.post(url='https://scores-shxw.onrender.com/scores', json=score)
        add_score()
        if resp.status_code == 201:
            scores = read_scores()
            return render_template('scores.html', scores=scores)
        else:
            return "Failed to save score", 500

    # if request.method == 'POST':
    #     id = request.form.get('id') # get user input from post
    #     name = request.form.get('name')
    #     points=request.form.get('points')
    #     name = f"{name}" 
    #     save_to_scores(scores)
    #     read_scores()   
    #     return render_template('scores.html', name=str(name), id=id, points=points)
        #else:
            #raise Exception("Give a proper name for example 'John Wick'")
    else:
        scores = read_scores()
        for score in scores:
            score['id'] = score.pop('id')
            score['name'] = score.pop('name')
            score['points'] = score.pop('points')
        return render_template('scores.html', scores=scores)

if __name__ == "__main__":
    app.run()