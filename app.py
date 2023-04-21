from flask import Flask, Response, jsonify, request, make_response, render_template, abort
import json
from operator import itemgetter
from repository import *
import requests
from validation import *
from flask_bcrypt import Bcrypt
import dropbox
import os

access_token = os.getenv("avain")
dbx = dropbox.Dropbox(access_token)

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Replace 'secret' with the hashed version of the password
password_hash = bcrypt.generate_password_hash('secret').decode('utf-8')

# Password authentication decorator
def require_password(func):
    def wrapper(*args, **kwargs):
        # Get the password from the query parameters of the request
        pw = request.args.get("pw")
        #If no password is given OR the password doesn't match, the program aborts with error message
        if not pw or not bcrypt.check_password_hash(password_hash, pw):
            abort(401, "Authentication required")
        # If the password is correct, call the decorated function with the original arguments and return the result
        return func(*args, **kwargs)
    # Set the name of the wrapper function to be the same as the name of the endpoint function
    wrapper.__name__ = func.__name__
    return wrapper

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, DELETE'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# JONNA & MATIAS "Fetching all scores":
@app.route("/scores")
@require_password
def get_scores():
    """
    Returns a list of score objects in JSON format, sorted and limited based on the given query parameters.

    Query Parameters:
    - sort: string value indicating how to sort the scores list. Possible values are "asc" (for ascending order) and "desc" (for descending order).
    - limit: integer value indicating the maximum number of scores to return.

    Returns:
    - A JSON response containing a list of score objects in the specified order and limit, with an HTTP status code of 200 (OK).
    """
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
@require_password
def get_scores_id(the_id):
    """
    Returns the score object with the given id as a JSON response.

    Args:
    - the_id: integer value representing the id of the desired score object

    Returns:
    - A JSON response containing the score object with the given id and an HTTP status code of 200 (OK) if a matching score object is found.
    - An empty response and an HTTP status code of 404 (Not Found) if no matching score object is found.
    """
    scores = read_scores()
    for score in scores:
        if score["id"] == the_id:
            return jsonify(score), 200
    return make_response ("", 404)

# MATIAS Created a function for getting the 10th score so that in the game the app will compare the players points to the 10th score.
@app.route('/scores/last_score')
def get_last_score():
    scores = read_scores()
    scores=sorted(scores, key=lambda k: int(k['points']), reverse=True)
    last_score=scores[9]
    return jsonify(last_score), 200

# # JONNA "Adding a new score" (Backend) 
@app.route('/scores', methods=['POST'])
def add_score():
    """
    Adds a new score to the list of scores and generates ID.

    Args:
        None

    Returns:
        - A response with an HTTP status code of 201 (Created) if the score is added successfully.
        - A response with an HTTP status code of 400 (Bad Request) if the JSON data is invalid.
    """
    # load given JSON data and turn it into dictionary
    score = request.get_json()
    if not score:
        return make_response("Invalid JSON data", 400)
    
        # validate username
    username = score.get('name')
    if not validate_username(username):
        return make_response("Invalid username", 400)
    if not username_in_use(username):
        return make_response("Username already in use", 400)
    
    scores = read_scores()
    # generate new score ID
    if scores:
        score_id = scores[-1]['id'] + 1
    else:
        score_id = 1
    # add new score with generated ID
    score['id'] = score_id
    scores.append(score)
    #save to dropbox
    scores_json = json.dumps(scores)
    dbx.files_upload(scores_json.encode("utf-8"), '/scores.txt',  mode=dropbox.files.WriteMode("overwrite"))
    # save updated scores
    save_to_scores(scores)
    # return success response
    return make_response("", 201)

# JONNA "Deleting a score by id":
@app.route('/scores/<int:the_id>', methods=['DELETE'])
@require_password
def delete_customer(the_id):
    """
    Deletes the score object with the given id.

    Args:
    - the_id (int): the id of the score object to be deleted.

    Returns:
    - A tuple containing an empty response and an HTTP status code of 204 (No Content) if a matching score object is found and deleted.
    - A tuple containing an empty response and an HTTP status code of 404 (Not Found) if no matching score object is found.

    Raises:
    - ValueError: if the_id parameter is not an integer.

    """
    scores = read_scores()
    # Reads the scores from the database

    index_to_be_deleted = -1
    # Initializes the index of the score object to be deleted to -1

    for i in range(0, len(scores)):
        if(scores[i]["id"] == the_id):
            index_to_be_deleted = i
    # Loops through the scores list to find the index of the score object with the given id.       
    
    if(index_to_be_deleted != -1):
        scores.pop(index_to_be_deleted)
          # Removes the score object at the identified index from the scores list.

        save_to_scores(scores)
         # Saves the updated scores to the database.

        return make_response("", 204)
        # Returns a response with status code 204 (No Content) to indicate that the score object was successfully deleted.

    else:
        return make_response("", 404)
        # Returns a response with status code 404 (Not Found) to indicate that no matching score object was found.

# MATIAS sort scores in asc or desc order
@app.route('/scores', methods=['GET'])
@require_password
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
@require_password
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

# JONNA add new score (Frontend)
# @app.route('/scores', methods=['POST'])
def add_score_to_database(score):
    """
    Add a new score to the database.

    Args:
        score (dict): The new score to add to the database.

    Returns:
        bool: True if the score was successfully added to the database, False otherwise.
    """
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
    return True

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
        # Get the values of 'name' and 'points' from the form data and create a dictionary 'score' containing these values.
         
        if not validate_username(name):
            return render_template('scores.html', error='Username may contain up to ten letters without special characters and the first letter must be capitalized')
        # If the name is not valid (according to the 'validate_username' function), return 'scores.html' template with an error message.
        if not username_in_use(name):
            return render_template('scores.html', error='Username is already in use.')


        score = {'name': name, 'points': points}
        # Create a new dictionary 'score' containing the name and points values.
       
        if add_score_to_database(score):

            scores = read_scores()
            sorted_scores = sorted(scores, key=lambda x: int(x['points']), reverse=True)[:10]
            return render_template('scores.html', scores=sorted_scores)
        else:
            return "Failed to save score", 500
        # If the score was added to the database successfully, read the updated scores from the database
        # and render the 'scores.html' template with the updated scores. Otherwise, return an error message.
    else:
        scores = read_scores()
        # for score in scores:
        #     score['id'] = score.pop('id')
        #     score['name'] = score.pop('name')
        #     score['points'] = score.pop('points')
        scores = sorted(scores, key=lambda k: int(k['points']), reverse=True)[:10]
        return render_template('scores.html', scores=scores)
        # If the request method is not POST, read the scores from the database and show 'scores.html' template with the scores.

if __name__ == "__main__":
    app.run()

