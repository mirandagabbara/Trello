# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request, session, url_for, copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from .utils.database.database  import database
from werkzeug.datastructures   import ImmutableMultiDict
from pprint import pprint
import json
import random
import functools
from . import socketio
db = database()


#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function

def getUser():
    return db.reversibleEncrypt('decrypt', session.get('email')) if session.get('email') else 'Unknown'

@app.route('/login')
def login():
    return render_template('login.html', user=getUser())

@app.route('/logout')
def logout():
    session.pop('email', default=None)
    return redirect('/')

@app.route('/processlogin', methods=["POST", "GET"])
def processlogin():
    email = request.form.get("email")
    password = request.form.get("password")
    
    print("Received email:", email)
    print("Received password:", password)

    if not email or not password:
        return json.dumps({'success': 0, 'error': 'Email and password are required.'})

    auth_result = db.authenticate(email, password)
    if auth_result.get('success'):
        session['email'] = db.reversibleEncrypt('encrypt', email)
        return json.dumps({'success': 1, 'redirect': url_for('dashboard')})
    else:
        return json.dumps({'success': 0, 'error': 'Invalid credentials'})
        
@app.context_processor
def inject_user():
    return {'user': getUser()}

@app.route('/signup')
def signup():
	return render_template('signup.html')

@app.route('/processsignup', methods=["POST"])
def processsignup():
    email = request.form.get("email")
    password = request.form.get("password")
    
    if not email or not password:
        return json.dumps({'success': 0, 'error': 'Email and password are required.'})
    
    signup_result = db.createUser(email, password)
    if signup_result.get('success'):
        return json.dumps({'success': 1})
    else:
        return json.dumps({'success': 0, 'error': signup_result.get('error')})
    

#######################################################################################
# CHATROOM RELATED
#######################################################################################
@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html', user=getUser())


# Event when a user joins the chat room
@socketio.on('joined', namespace='/chat')
def joined(data):
    user = getUser()
    join_room('main')
    emit(
        'status',
        {
            'msg': f"{user} has entered the chat room.",
            'style': 'color: blue; text-align: center;'
        },
        room='main'
    )


# Event when a user sends a message
@socketio.on('message', namespace='/chat')
def handle_message(data):
    user = getUser()
    message = data.get('msg', '')
    emit(
        'message',
        {'msg': f"{user}: {message}"},
        room='main'
    )


# Event when a user leaves the chat room
@socketio.on('left', namespace='/chat')
def left(data):
    user = getUser()
    leave_room('main')
    emit(
        'status',
        {
            'msg': f"{user} has left the chat room.",
            'style': 'color: gray; text-align: center;'
        },
        room='main'
    )



#######################################################################################
# OTHER
#######################################################################################
@app.route('/')
def root():
	return redirect('/home')

@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')

"""
@app.route('/resume')
def resume():
	resume_data = db.getResumeData()
	pprint(resume_data)
	return render_template('resume.html', resume_data = resume_data)
"""

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r
