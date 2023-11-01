from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import  user, game



# Read Users Controller
@app.route('/select/games')
def game_select():
    if 'user_id' in session:
        games = game.Game.get_games()
        return render_template('game_select.html', games = games)
    return redirect('/')



# Update Users Controller
@app.route('/select/game/process', methods = ['POST'])
def update_users_games():
    if 'user_id' in session:
        games_list = request.form.getlist('game_id')
        
        for game_id in games_list:
            data ={
                'user_id' : request.form.get('user_id'),
                'game_id' : game_id
                }
            game.Game.register_users_games(data)
        return redirect('/add/about_me')
    return redirect('/')