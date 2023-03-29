#from repository import save_to_database, read_database
from flask import Flask, Response, jsonify, request, make_response
import json

app = Flask(__name__)

the_id=2
scores = [{"id": 1, "name": "jack"}, {"id": 2, "name": "hannah"}]

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Methods'] = 'DELETE'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route("/scores")
def get_customers():
    read_database()
    return jsonify(scores
)

@app.route('/scores/<int:the_id>')
def get_customer(the_id):
    read_database()
    customer = -1
    for i in range (0,len(scores)):
        if(scores[i]["id"] == the_id):
            customer = i
            break
    if customer != -1:
        for i in range(customer, len(scores)):
            scores[i]['id'] = scores[i]['id'] - 1
        return jsonify(scores
    [customer])
    else:
        return make_response(jsonify(message="Customer not found"), 404)

@app.route('/scores/<int:the_id>', methods = ['DELETE'])
def delete_customer(the_id):
    # initialize customer index
    customer = -1
    
    # loop through scores
    # list to find matching id
    for i in range (0,len(scores)):
        if(scores[i]["id"] == the_id):
            # if found, set customer index to current index i and exit loop
            customer = i
            break
    
    # if customer with given id exists
    if customer != -1:
        # remove the customer from the list
        scores.pop(customer)
        
        # update the id of remaining scores
    
        for i in range(customer, len(scores)):
            scores[i]['id'] = scores[i]['id'] - 1
        
        # return 204 status code (No Content)
        return make_response("", 204)
    else:
        # if customer not found, return 404 status code (Not Found) with error message
        return make_response(jsonify(message="Customer not found"), 404)

@app.route('/scores', methods=['POST'])
def add_customer():
    global the_id # Global variable to keep track of the ID of the new customer
    global scores
 # Global list to store the existing scores

    
    customer = json.loads(request.data) # Get the customer data from the request and convert it to a Python dictionary using the json module
    
    the_id += 1 # Increment the ID to generate a new ID for the new customer
    customer['id'] = the_id # Assign the new ID to the customer
    scores.append(customer) # Add the new customer to the list of scores

    save_to_database(customer) # Save the new customer to the database
    
    return make_response("", 201) # Return a HTTP 201 Created status code to indicate that the customer was successfully added
    #401 CONFLICT

if __name__ == "__main__":
    app.run()