from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import comment, user

# Create Users Controller
@app.route('/comment/process', methods = ['POST'])
def leave_comment():
    comment.Comment.leave_comment(request.form)
    return redirect(f'/user_profile/{request.form.get("commenti_id")}')

# Update comments
@app.route('/comment/update/process', methods = ['POST'])
def edit_comment():
    this_comment = comment.Comment.get_single_comment(request.form.get('id'))
    if this_comment.commenter_id == session['user_id']:
        comment.Comment.edit_comment(request.form)
    return redirect(f'/user_profile/{request.form.get("commenti_id")}')


# Delete Users Controller
@app.route('/remove_comment/<int:comment_id>')
def remove_comment(comment_id):
    this_comment = comment.Comment.get_single_comment(comment_id)
    if this_comment.commenter_id == session['user_id']:
        comment.Comment.delete_comment(comment_id)
    return redirect(f'/user_profile/{this_comment.commenti_id}')