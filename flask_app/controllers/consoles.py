from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import  user, console



# Read Users Controller
@app.route('/select/consoles')
def console_select():
    if 'user_id' in session:
        consoles = console.Console.get_consoles()
        return render_template('console_select.html', consoles = consoles)
    return redirect('/')



# Update Users Controller
@app.route('/select/console/process', methods = ['POST'])
def update_users_console():
    if 'user_id' in session:
        consoles_list = request.form.getlist('console_id')

        for console_id in consoles_list:
            data ={
                'user_id' : request.form.get('user_id'),
                'console_id' : console_id
                }
            console.Console.register_users_console(data)
        return redirect('/select/games')
    return redirect('/')



