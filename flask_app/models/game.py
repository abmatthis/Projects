from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session

class Game:
    db = "LFG_Schema" 
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.image = data['image']



    # Read Games Models
    @classmethod
    def get_games(cls):
        query = """
        SELECT *
        FROM games 
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        return results
    
    @classmethod
    def register_users_games(cls, form):
        query = """
        INSERT INTO users_has_games (user_id, game_id) 
        VALUES (%(user_id)s, %(game_id)s)
        ;"""
        results = connectToMySQL(cls.db).query_db(query, form)
        return results
    
    @classmethod
    def get_games_for_users(cls):
        query = """
        SELECT *
        FROM users 
        JOIN users_has_games ON users.id = users_has_games.user_id
        JOIN games ON  users_has_games.game_id = games.id  
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        return results
    
    @classmethod
    def get_games_for_one_users(cls, user_id):
        data = {'user_id': user_id}
        query = """
        SELECT *
        FROM games
        LEFT JOIN users_has_games ON games.id = users_has_games.game_id
        ORDER BY
            CASE
                WHEN user_id = %(user_id)s THEN 0  
                ELSE 1
            END,
        games.id;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
    
    # Update Games Models

    
    # Delete Games Models
    @classmethod
    def delete_users_games(cls, id):
        data = {"user_id" : id}
        query = "DELETE FROM users_has_games WHERE user_id = %(user_id)s;"
        connectToMySQL(cls.db).query_db(query, data)
        return
    
    


# Easy data repolulation after drop table
# INSERT INTO `lfg_schema`.`games` (`name`, `image`) VALUES ('League of Legends', 'lol.png');
# INSERT INTO `lfg_schema`.`games` (`name`, `image`) VALUES ('Dota 2', 'dota.png');
# INSERT INTO `lfg_schema`.`games` (`name`, `image`) VALUES ('Smite', 'smite.png');

# INSERT INTO `lfg_schema`.`games` (`name`, `image`) VALUES ('Diablo 4', 'diablo4.png');
# INSERT INTO `lfg_schema`.`games` (`name`, `image`) VALUES ('World of Warcraft', 'wow.png');
# INSERT INTO `lfg_schema`.`games` (`name`, `image`) VALUES ('Balder's Gate 3', 'bg3.png');

# INSERT INTO `lfg_schema`.`games` (`name`, `image`) VALUES ('Counter Strike', 'cs.png');
# INSERT INTO `lfg_schema`.`games` (`name`, `image`) VALUES ('Apex Legends ', 'apex.png');
# INSERT INTO `lfg_schema`.`games` (`name`, `image`) VALUES ('Fortnite ', 'fortnite.png');

# INSERT INTO `lfg_schema`.`games` (`name`, `image`) VALUES ('Super Smash Bros. Ultimate ', 'ssbu.png');
# INSERT INTO `lfg_schema`.`games` (`name`, `image`) VALUES ('Rocket League', 'rocketleague.png');
# INSERT INTO `lfg_schema`.`games` (`name`, `image`) VALUES ('Among Us ', 'amongus.png');
