from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, comment, game, console

# Create Users Controller
@app.route('/register', methods = ['POST'])
def register_user():
    if 'user_id' in session:
        return redirect(f'/user_profile/{session["user_id"]}')
    if user.User.register_user(request.form):
        return redirect('/select/consoles')
    return redirect('/')


# Read Users Controller
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(f'/user_profile/{session["user_id"]}')
    return render_template('registration.html')

@app.route('/returning_user')
def login_screen():
    if 'user_id' in session:
        return redirect(f'/user_profile/{session["user_id"]}')
    return render_template('login.html')

@app.route('/user_profile/<int:user_id>')
def user_profile(user_id): 
    these_comments = comment.Comment.get_comments()
    this_user =user.User.get_user_by_id(user_id)
    this_users_games = game.Game.get_games_for_users()
    return render_template("user_profile.html", comments = these_comments, user = this_user, games = this_users_games)


@app.route('/add/about_me')
def create_about_me_page():
    if 'user_id' in session: 
        return render_template("create_about_me.html")
    return redirect('/')

@app.route('/edit/user_profile/<int:user_id>')
def edit_account_page(user_id):
    if 'user_id' in session:
        this_user = user.User.get_user_by_id(user_id)
        games  = game.Game.get_games_for_one_users(user_id)
        consoles = console.Console.get_consoles_for_one_users(user_id)
        return render_template("edit_profile.html", user = this_user, games = games, consoles = consoles)
    return redirect('/')

@app.route('/find/gamers')
def view_all_users():
    users = user.User.get_all_users()
    games = game.Game.get_games_for_users()
    consoles = console.Console.get_consoles_for_users()
    return render_template("view_all_users.html", users = users, games = games, consoles = consoles)




# Update Users Controller
@app.route('/login', methods = ['POST'])
def user_login():
    if user.User.validate_user_login(request.form):
        return redirect(f'/user_profile/{session["user_id"]}')
    return redirect('/returning_user')

@app.route('/about_me/process', methods = ['POST'])
def update_about_me():
    if 'user_id' in session: 
        if user.User.add_about_me(request.form):
            return redirect(f'/user_profile/{session["user_id"]}')
        
        return redirect('/add/about_me')
    return redirect('/')

@app.route('/update/user_info_password', methods = ['POST'])
def update_user():
    if 'user_id' in session:
        user.User.update_user_password(request.form)
        return redirect(f'/edit/user_profile/{session["user_id"]}')
    return redirect('/')



# Delete Users Controller
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


