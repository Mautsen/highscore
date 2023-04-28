# Highscore
Highscore for mobilegame. In the website you can see top ten users and add a new user with points.
In the backend you can:
- Fetch all scores
- Fetch score based on id
- Fetch all scores with limit
- Fetch all scores with ascending or descending order
- Add a new score
- Delete a score by id
- Display high scores in html file format in a browser

# Author
Jonna Kyllönen, 
Matias Leppänen

# Screenshots
![Image of highscore](/highscore.png)


# Tech/framework used

- Python
- HTML
- CSS

# External modules:

- `flask`: a web framework for Python.
- `requests`: a third-party Python library for sending HTTP requests.
- `flask_bcrypt`: a third-party Python library for encrypting passwords using bcrypt hashing.
- `firebase_admin`: a third-party Python library for integrating with the Firebase platform.
- `Gunicorn`: Python HTTP server

# Installation and running:
- See the requirements.txt file or above which external modules are necessary to install before running the code and install them.
- Command for installing the external modules: pip install "module-name-here"

# clone highscore repository
- git clone "copy-the-repository-link-here" (More instructions from here: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
- cd highscore

# start backend
- The file app.py cannot be run at the moment because of firebase. The file client.py uses the backend functions, so you can test them with the command:        python client.py 

# start frontend
https://scores-shxw.onrender.com/

# API implementation
API is deployed to cloud and can be accessed using following url:

https://scores-shxw.onrender.com/

The backend is secured with a hashed password

# Screencast:
[![Screencast](https://img.youtube.com/vi/(https://www.youtube.com/watch?v=k4RMZif1Rdg)/0.jpg)](https://www.youtube.com/watch?v=k4RMZif1Rdg)
