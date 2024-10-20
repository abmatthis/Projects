from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user, comment



class Reply:
    db = "LFG_Schema" 
    def __init__(self, data):
        self.response_id = data['response_id']
        self.body = data['body']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.comment_id = data['comment_id']
        self.responder_id = data['responder_id']
        self.responder = None


    # Create Replies Models
    @classmethod
    def leave_reply(cls, data):
        if not cls.validate_reply(data):
            return False
        query = """
        INSERT INTO replies ( comment_id, responder_id, body)
        VALUES ( %(comment_id)s, %(responder_id)s, %(body)s)
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
    
    #Read Replies Models
    @classmethod
    def get_replies(cls):
        query = """
        SELECT *
        FROM replies 
        JOIN comments ON comments.comment_id = replies.original_post_id
        JOIN users ON id  = replies.responder_id
        ORDER BY comments.created_at ASC;
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        replies = []

        for database_row in results:
            reply = cls(database_row)
            responder = {
                "id" : database_row['id'],
                "username" : database_row['username'],
                "email" : database_row['email'],
                "password" : database_row['password'],
                "created_at" : database_row['created_at'],
                "updated_at" : database_row['updated_at'],
                "about_me" : database_row['about_me'],
                
            }
            reply.responder = user.User(responder)
            replies.append(reply)
        return replies

    
    def get_single_reply(cls, data):
        query = """
        SELECT *
        FROM replies 
        JOIN comments ON comments.commenter_id = replies.comment_id
        JOIN users On user.id  = replies.responder_id
        WHERE comment_id = %(id)s
        ;"""
        data = { 'id' : data}
        results = connectToMySQL(cls.db).query_db(query, data)
        results = results[0]
        reply = cls(results)

        responder = {
                "id" : results['id'],
                "username" : results['username'],
                "email" : results['email'],
                "password" : results['password'],
                "created_at" : results['created_at'],
                "updated_at" : results['updated_at'],
                "about_me" : results['about_me'],

            }
        reply.responder = user.User(responder) 
        return reply
    

    # Update Users Models
    @classmethod
    def edit_reply(cls, data):
        if not cls.validate_reply(data):
            return False
        query = """
        UPDATE replies
        SET body = %(body)s
        WHERE response_id = %(id)s
        ;"""
        connectToMySQL(cls.db).query_db(query, data)
        return True


    # Delete Users Models
    @classmethod
    def delete_reply(cls, response_id):
        data = { 'id' : response_id}
        query = """
        DELETE FROM replies
        WHERE response_id = %(id)s
        ;"""
        connectToMySQL(cls.db).query_db(query, data)
        return
    

    #Replies Helper Models
    @staticmethod
    def validate_reply(data):
        is_valid = True
        if len(data['body']) == 0:
            is_valid = False
        # if len(data['body']) >= 200:
        #     is_valid = False
        return is_valid