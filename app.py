#from repository import save_to_database, read_database
from flask import Flask, Response, jsonify, request, make_response
import json
from operator import itemgetter

app = Flask(__name__)

#scores = [{"id": 1, "name": "jack", "points":123}, {"id": 2, "name": "hannah", "points": 4567}]

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, DELETE'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# JONNA read_scores
def read_scores():
    try:
        with open('scores.txt', 'r') as f:
            file_contents = f.read()
            if file_contents.strip() == '':
                # tiedosto on tyhjä, palautetaan tyhjä lista
                return []
            else:
                scores = json.loads(file_contents)
                if isinstance(scores, dict):
                    # jos json-tiedosto sisältää yhden nimen, muutetaan se listaksi
                    scores = [scores]
    except FileNotFoundError:
        scores = []
    return scores

# JONNA save_scores to the scores.txt
def save_scores(scores):
    # tallennetaan tiedot json-muodossa tiedostoon
    with open('scores.txt', 'w') as f:
        json.dump(scores, f)

# JONNA "Fetching all scores":
# @app.route("/scores")
# def get_scores():
#     return jsonify(scores)

@app.route("/scores")
def get_scores():
    # luetaan tiedot tiedostosta
    scores = read_scores()
    # palautetaan tiedot json-muodossa
    return jsonify(scores)

# JONNA "Fetching score based on id": 
@app.route('/scores/<int:the_id>')
def get_scores_id(the_id):
    scores = read_scores()
    for score in scores:
        if score["id"] == the_id:
            return jsonify(score), 200
    return make_response ("", 404)

# JONNA "Adding a new score"
@app.route('/scores', methods=['POST'])
def add_score():
    # load given string and turn it into dictionary
    score = json.loads(request.data)
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
    save_scores(scores)
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
        save_scores(scores)
        return make_response("", 204)
    else:
        return make_response("", 404)

# MATIAS sort scores in asc or desc order
@app.route('/scores/sort', methods=['GET'])
def sort():
    # JONNA TEKI ALLA OLEVAN LISÄYKSEN, KUN POISTI GLOBAALIN LISTAN, ETTÄ SAATAIS TALLENNUS TOIMIMAAN, MUOKKAA
    # TAI POISTA JOS EI TOIMI NÄIN HYVIN TÄSSÄ!!!!!!!!! (OLEN PAHOILLANI:()
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


if __name__ == "__main__":
    app.run()