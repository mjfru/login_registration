from flask_app.controllers import users
from flask_app import app

if __name__ == '__main__':
    app.run(debug = True)

# Commands to get this thing going in the terminal:
# python -m pipenv install flask PyMySQL (first time only)
# python -m pipenv shell 
# python -m server.py

