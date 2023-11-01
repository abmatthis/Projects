from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session

class Console:
    db = "LFG_Schema" 
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.image = data['image']

    # Read Users Models
    @classmethod
    def get_consoles(cls):
        query = """
        SELECT *
        FROM consoles 
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        return results
    
    @classmethod
    def register_users_console(cls, form):
        query = """
        INSERT INTO users_has_consoles (user_id, console_id) 
        VALUES (%(user_id)s, %(console_id)s)
        ;"""
        results = connectToMySQL(cls.db).query_db(query, form)
        return results
    
    @classmethod
    def get_consoles_for_one_users(cls, user_id):
        data = {'user_id': user_id}
        query = """
        SELECT *
        FROM consoles
        LEFT JOIN users_has_consoles ON consoles.id = users_has_consoles.console_id
        ORDER BY
            CASE
                WHEN user_id = %(user_id)s THEN 0  
                ELSE 1
            END,
        consoles.id;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

# Easy data repolulation after drop table
# INSERT INTO `lfg_schema`.`consoles` (`name`, `image`) VALUES ('ps5', 'ps5.png');
# INSERT INTO `lfg_schema`.`consoles` (`name`, `image`) VALUES ('xboxone', 'xboxone.png');
# INSERT INTO `lfg_schema`.`consoles` (`name`, `image`) VALUES ('switch', 'switch.png');
# INSERT INTO `lfg_schema`.`consoles` (`name`, `image`) VALUES ('pc', 'pc.png');

