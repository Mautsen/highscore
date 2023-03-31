#from repository import save_to_database, read_database
from flask import Flask, Response, jsonify, request, make_response
import json

app = Flask(__name__)

scores = [{"id": 1, "name": "jack"}, {"id": 2, "name": "hannah"}]

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Methods'] = 'DELETE'
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
def add_customer():
    # load given string and turn it into dictionary
    customer = json.loads(request.data)
    # check if customer ID already exists
    for existing_customer in scores:
        if existing_customer['id'] == customer['id']:
            return make_response("", 409)
    # generate new customer ID
    last_customer_id = scores[-1]['id'] if scores else 0
    customer_id = last_customer_id + 1
    # add new customer with generated ID
    customer['id'] = customer_id
    scores.append(customer)
    # return success response
    return make_response("", 201)

# JONNA "Deleting a score by id":
@app.route('/customers/<int:the_id>', methods=['DELETE'])
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




# @app.route('/scores', methods=['POST'])
# def add_customer():
#     global the_id # Global variable to keep track of the ID of the new customer
#     global scores
#  # Global list to store the existing scores

    
#     customer = json.loads(request.data) # Get the customer data from the request and convert it to a Python dictionary using the json module
    
#     the_id += 1 # Increment the ID to generate a new ID for the new customer
#     customer['id'] = the_id # Assign the new ID to the customer
#     scores.append(customer) # Add the new customer to the list of scores

#     save_to_database(customer) # Save the new customer to the database
    
#     return make_response("", 201) # Return a HTTP 201 Created status code to indicate that the customer was successfully added
#     #401 CONFLICT

if __name__ == "__main__":
    app.run()