from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# CREATE
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('registration').query_db(query, data)

# READ
    # @classmethod  #! Refactored due to type errors after implementing Login validation, study why this happened.
    # def get_user_by_email(cls, data):
    #     #! Didn't need this --> data = {
    #     #     'email' : email
    #     #     }
    #     query = "SELECT * FROM users WHERE email = %(email)s;"
    #     result = connectToMySQL('registration').query_db(query, data)
    #     #? If no matching user...
    #     if len(result) < 1:
    #         return False
    #     return cls(result[0])

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('registration').query_db(query, data)
        if result:  #? If there is an existing email...
            return cls(result[0])
        return None  #? If the associated email does not exist yet

# REGISTRATION VALIDATION
    @staticmethod
    def validate(user):
        is_valid = True

        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.", category='register') #! Inside get_flashed_messages(), set the parameter to category_filter['register']
            is_valid = False                                                                #? Allows users to see the message in the appropriate box
        if not user['first_name'].isalpha():
            flash("Please enter only letters for your first name.", category='register')
            is_valid = False

        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.", category='register')
            is_valid = False
        if not user['last_name'].isalpha():
            flash("Please enter only letter for your last name.", category='register')
            is_valid = False

        if not EMAIL_REGEX.match(user['email']):
            flash("Please enter a valid email format.", category='register')
            is_valid = False

        if User.get_user_by_email(user['email']):
            flash("Email already registered. Enter a different valid email address.", category='register')
            is_valid = False

        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.", category='register')
            is_valid = False

        if user['password'] != user['confirm_pw']:
            flash("Passwords do not match. Please try again.", category='register')
            is_valid = False
        return is_valid
