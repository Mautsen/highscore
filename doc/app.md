Module app
==========

Functions
---------

    
`add_score()`
:   Adds a new score to the list of scores and generates ID.
    
    Args:
        None
    
    Returns:
        - A response with an HTTP status code of 201 (Created) if the score is added successfully.
        - A response with an HTTP status code of 400 (Bad Request) if the JSON data is invalid.

    
`add_score_to_database(score)`
:   Add a new score to the database.
    
    Args:
        score (dict): The new score to add to the database.
    
    Returns:
        bool: True if the score was successfully added to the database, False otherwise.

    
`after_request(response)`
:   Adds headers to the response to enable Cross-Origin Resource Sharing (CORS).
    
    CORS is a mechanism that allows many resources (e.g., fonts, JavaScript, etc.) on a web page to be requested
    from another domain outside the domain the resource originated from. By default, web browsers block CORS requests.
    
    The headers added to the response enable CORS requests from any origin ('*') and allow the GET, POST, and DELETE
    methods to be used.
    
    Args:
        response (Flask response object): The response to add headers to.
    
    Returns:
        A Flask response object with headers added to enable CORS requests.

    
`delete_customer(*args, **kwargs)`
:   

    
`get_last_score()`
:   Returns the score object with the 10th 'points' value. This was made for Unity, so that it would check if the player gets to the top 10 list.
    
    Returns:
    - A JSON response containing the score object with the highest 'points' value, with an HTTP status code of 200 (OK).

    
`get_scores(*args, **kwargs)`
:   

    
`get_scores_id(*args, **kwargs)`
:   

    
`index()`
:   The index function that handles both GET and POST requests to the root route. When a GET request is made,
    the function reads the data from the score-file and renders the index.html template with a form.
    When a POST request is made, the function reads the form data, validates the name and saves the data to the database.
    It then reads the updated data from the score-file and renders the index.html template with the updated data.
    
    Returns:
        str: the rendered HTML template as a string.

    
`require_password(func)`
:   Decorator function for password authentication.
    
    This function takes in a function as a parameter and returns a new function that wraps the original function with password authentication. If the correct password is not provided, an HTTPException with a 401 status code and an "Authentication required" message will be raised.
    
    Parameters:
    func (function): The function to be decorated with password authentication.
    
    Returns:
    function: A new function that wraps the original function with password authentication.
    
    Raises:
    HTTPException: If no password is provided or the provided password does not match the hashed password.