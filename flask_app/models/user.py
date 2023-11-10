
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import game

import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


class User:
    db = "LFG_Schema" 
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.about_me = data['about_me']
        self.games = [None]




    # Create Users Models
    @classmethod
    def register_user(cls, form):
        if not cls.validate_user_registration(form):
            return False
        user_info = cls.parse_user_data(form)
        query = """
        INSERT INTO users ( username, email, password, about_me )
        VALUES ( %(username)s, %(email)s, %(password)s, %(about_me)s)
        ;"""
        results = connectToMySQL(cls.db).query_db(query, user_info)
        session['user_id'] = results
        session['username'] = form["username"]
        return results



    # Read Users Models
    @classmethod
    def get_all_users(cls):
        query = """
        SELECT *
        FROM users 
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users


    @classmethod
    def get_user_by_email(cls, email):
        data = { 'email' : email }
        query = """
        SELECT *
        FROM users
        WHERE email = %(email)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def get_user_by_id(cls, id):
        data = { 'id' : id }
        query = """
        SELECT *
        FROM users
        WHERE id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def get_user_by_username(cls, username):
        data = { 'username' : username }
        query = """
        SELECT *
        FROM users
        WHERE username = %(username)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            return cls(results[0])
        return False




    # Update Users Models
    @classmethod
    def add_about_me(cls, data):
        if not cls.validate_user_about_me(data):
            return False
        query = """
        UPDATE users
        SET about_me = %(about_me)s
        WHERE id = %(id)s
        ;"""
        connectToMySQL(cls.db).query_db(query, data)
        return True
    
    @classmethod
    def update_user_password(cls, form):
        if not cls.validate_user_update_password(form):
            return False
        user_info = cls.parse_user_data(form)
        query = """
        UPDATE users
        SET password= %(password)s
        WHERE id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, user_info)
        return results

    # Delete Users Models


    #Helper Models
    @staticmethod
    def validate_user_registration(data):
        is_valid = True
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

        # Name Validate
        if len(data['username']) < 2:
            flash('Username must be at least two letters!', 'username')
            is_valid = False
        if User.get_user_by_username(data['username']):
            flash('This Username is taken, sorry', 'username')
            is_valid = False

        # Email Validate
        if not EMAIL_REGEX.match(data['email']):
            flash('Please use a valid email address!', 'email')
            is_valid = False
        if User.get_user_by_email(data['email']):
            flash('This email is already in use. Please try again', 'email')
            is_valid = False

        # Password Validate
        if len(data['password']) < 8:
            flash('Password must be at least 8 charaters long!', 'password')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('Passwords did not match', 'confirm_password')
            is_valid = False
        return is_valid
    
    @staticmethod
    def parse_user_data(data):
        parsed_data= {}
        #Added conditionals to parse_user_data for when only password is being updated
        if 'id' in data:
            parsed_data['id'] = data['id']
        else:
            parsed_data['id'] = None
    
        if 'username' in data:
            parsed_data['username'] = (data['username']).capitalize()
        else:
            parsed_data['username'] = None
        
        if 'email' in data:
            parsed_data['email'] = data['email']
        else:
            parsed_data['email'] = None
        
        parsed_data['about_me'] = ''

        parsed_data['password'] = bcrypt.generate_password_hash(data['password'])
        parsed_data['confirm_password'] = bcrypt.generate_password_hash(data['confirm_password'])

        return parsed_data

    
    @staticmethod
    def validate_user_login(form):
        user_by_email = User.get_user_by_email(form['email']) 
        if user_by_email:
            if bcrypt.check_password_hash(user_by_email.password, form['password']):
                session['user_id'] = user_by_email.id
                session['username'] = user_by_email.username
                return True
        flash('Incorrect password or email','login')
        return False
    
    @staticmethod
    #move this into validate user registration later
    def validate_user_about_me(data):
        is_valid = True
        if len(data['about_me']) <= 0:
            flash('If you do not want to write about yourself you can click the skip at the bottom of the screen and do it later!', 'about_me')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_user_update_password(data):
        #move this into validate user registration later
        is_valid = True

        # Password Validate
        if len(data['password']) < 8:
            flash('Password must be at least 8 charaters long!', 'update_user')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('Passwords did not match', 'update_user')
            is_valid = False
        return is_valid