
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user



class Comment:
    db = "LFG_Schema" 
    def __init__(self, data):
        self.comment_id = data['comment_id']
        self.body = data['body']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.commenter_id = data['commenter_id']
        self.commenti_id = data['commenti_id']
        self.commenter = None

    
    # Create Users Models
    @classmethod
    def leave_comment(cls, data):
        if not cls.validate_comment(data):
            return False
        query = """
        INSERT INTO comments ( commenter_id, commenti_id, body)
        VALUES ( %(commenter_id)s, %(commenti_id)s, %(body)s)
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
    
    #Read User Models
    @classmethod
    def get_comments(cls):
        query = """
        SELECT *
        FROM comments 
        JOIN users ON users.id = comments.commenter_id
        JOIN users user2 On comments.commenti_id = user2.id 
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        comments = []

        for database_row in results:
            comment = cls(database_row)
            commenter = {
                "id" : database_row['id'],
                "username" : database_row['username'],
                "email" : database_row['email'],
                "password" : database_row['password'],
                "created_at" : database_row['created_at'],
                "updated_at" : database_row['updated_at'],
                "about_me" : database_row['about_me'],
                
            }
            comment.commenter = user.User(commenter)
            comments.append(comment)
        return comments
    
    @classmethod
    def get_single_comment(cls, data):
        query = """
        SELECT *
        FROM comments 
        JOIN users ON users.id = comments.commenter_id
        JOIN users user2 On comments.commenti_id = user2.id 
        WHERE comment_id = %(id)s
        ;"""
        data = { 'id' : data}
        results = connectToMySQL(cls.db).query_db(query, data)
        results = results[0]
        comment = cls(results)

        commenter = {
                "id" : results['id'],
                "username" : results['username'],
                "email" : results['email'],
                "password" : results['password'],
                "created_at" : results['created_at'],
                "updated_at" : results['updated_at'],
                "about_me" : results['about_me'],

            }
        comment.commenter = user.User(commenter) 
        return comment
    
    # Update Users Models
    @classmethod
    def edit_comment(cls, data):
        if not cls.validate_comment(data):
            return False
        query = """
        UPDATE comments
        SET body = %(body)s
        WHERE comment_id = %(id)s
        ;"""
        connectToMySQL(cls.db).query_db(query, data)
        return True


    # Delete Users Models
    @classmethod
    def delete_comment(cls, comment_id):
        data = { 'id' : comment_id}
        query = """
        DELETE FROM comments
        WHERE comment_id = %(id)s
        ;"""
        connectToMySQL(cls.db).query_db(query, data)
        return



    # Delete Users Models
    
    #Helper Models
    @staticmethod
    def validate_comment(data):
        is_valid = True
        if len(data['body']) == 0:
            is_valid = False
        if len(data['body']) >= 200:
            is_valid = False
        return is_valid