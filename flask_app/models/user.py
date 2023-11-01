
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
        INSERT INTO users ( username, email, password )
        VALUES ( %(username)s, %(email)s, %(password)s)
        ;"""
        results = connectToMySQL(cls.db).query_db(query, user_info)
        session['user_id'] = results
        session['username'] = form["username"]
        return results



    # Read Users Models
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



    # Delete Users Models


    #Helper Models
    @staticmethod
    def validate_user_registration(data):
        is_valid = True
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

        # Name Validate
        if len(data['username']) < 2:
            flash('Username must be at least two letters!', 'registration')
            is_valid = False

        # Email Validate
        if not EMAIL_REGEX.match(data['email']):
            flash('Please use a valid email address!', 'registration')
            is_valid = False
        if User.get_user_by_email(data['email']):
            flash('This email is already in use. Please try again', 'registration')
            is_valid = False

        # Password Validate
        if len(data['password']) < 8:
            flash('Password must be at least 8 charaters long!', 'registration')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('Passwords did not match', 'registration')
            is_valid = False
        return is_valid
    
    @staticmethod
    def parse_user_data(data):
        parsed_data= {
            'username' : data['username'],
            'email' : data['email'],
            'password' : bcrypt.generate_password_hash(data['password']),
            'confirm_password' : bcrypt.generate_password_hash(data['confirm_password'])
        }
        return (parsed_data)
    
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
    def validate_user_about_me(data):
        is_valid = True
        if len(data['about_me']) <= 0:
            flash('Can not be blank. If you don not want to write about yourself you can click the skip at the bottom of the screen and do it later!', 'about_me')
            is_valid = False
        return is_valid