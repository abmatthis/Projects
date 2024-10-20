from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import reply, user

# Create Users Controller
@app.route('/reply/process', methods = ['POST'])
def leave_reply():
    reply.Reply.leave_reply(request.form)
    return redirect(f'/user_profile/{request.form.get("commenti_id")}')

# Update comments
@app.route('/reply/update/process', methods = ['POST'])
def edit_reply():
    this_reply = reply.Reply.get_single_reply(request.form.get('id'))
    if this_reply.responder_id == session['user_id']:
        reply.Reply.edit_comment(request.form)
    return redirect(f'/user_profile/{request.form.get("commenti_id")}')


# Delete Users Controller
@app.route('/remove_reply/<int:comment_id>')
def remove_reply(comment_id):
    this_reply = reply.Reply.get_single_comment(comment_id)
    if this_reply.responder_id == session['user_id']:
        reply.Reply.delete_comment(comment_id)
    return redirect(f'/user_profile/{this_reply.commenti_id}')