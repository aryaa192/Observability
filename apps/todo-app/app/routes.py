from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models import User, Todo

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if 'username' in session:
        user = User.find_user(session['username'])
        tasks = Todo.get_tasks(user['_id'])
        return render_template('todo.html', tasks=tasks)
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.check_password(username, password):
            session['username'] = username
            return redirect(url_for('main.index'))
    return render_template('login.html')

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        User.create_user(username, password)
        session['username'] = username
        return redirect(url_for('main.index'))
    return render_template('signup.html')

@main.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main.index'))

@main.route('/add', methods=['POST'])
def add():
    if 'username' in session:
        user = User.find_user(session['username'])
        title = request.form['title']
        description = request.form['description']
        Todo.create_task(user['_id'], title, description)
    return redirect(url_for('main.index'))
