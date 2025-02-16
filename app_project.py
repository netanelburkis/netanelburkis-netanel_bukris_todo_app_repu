import os
from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash  

DB_HOST = os.environ.get("DB_HOST", "db") #Defult to 'db' since Docker compose names it as such.
DB_USER = os.environ.get("DB_USER", "python_todo_list_app") 
DB_PASSWORD = os.environ.get("DB_PASSWORD", "123password")
DB_NAME = os.environ.get("DB_NAME", "todo_list_app_db")

todo_list_app = Flask(__name__)
todo_list_app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
todo_list_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
todo_list_app.secret_key = 'your_secret_key'  

db = SQLAlchemy(todo_list_app)

class Taskes(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False)
    user_name = db.Column(db.String(255), nullable=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

with todo_list_app.app_context():
    db.create_all()

@todo_list_app.route('/login_register', methods=['GET', 'POST'])
def login_register():
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username')
        password = request.form.get('password')
        
        if action == 'login':  
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):  
                session['username'] = username
                return redirect(url_for('main_page_todo_list__app'))
            else:
                return render_template('login_register.html', error="Invalid username or password.")
        
        elif action == 'register':  
            if User.query.filter_by(username=username).first():
                return render_template('login_register.html', error="Username already exists.")
            
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')  
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            
            return redirect(url_for('login_register'))
    
    return render_template('login_register.html')

@todo_list_app.route('/', methods=['GET', 'POST'])
def main_page_todo_list__app():
    if 'username' not in session:  
        return redirect(url_for('login_register'))
    
    user = session['username']  
    action = request.form.get('action')
    task_description = request.form.get('task')
    task_id = request.form.get('task_id')

    if action == 'add' and task_description:
        new_task = Taskes(
            task=task_description,
            completed=False,
            date_added=datetime.now(),
            user_name=user 
        )
        db.session.add(new_task)
        db.session.commit()

    elif action == 'del' and task_id:
        task_to_delete = Taskes.query.get(int(task_id))
        if task_to_delete:
            db.session.delete(task_to_delete)
            db.session.commit()

    elif action == 'toggle' and task_id:
        task_to_toggle = Taskes.query.get(task_id)
        if task_to_toggle:
            task_to_toggle.completed = not task_to_toggle.completed
            db.session.commit()

    query = request.form.get('search', '')
    tasks = Taskes.query.filter(Taskes.user_name == user, Taskes.task.contains(query)).all()

    for task in tasks:
        task.date_added = task.date_added.strftime('%Y-%m-%d %H:%M')
        
    return render_template('main_page_todo_list.html', user=user, tasks=tasks, query=query)

@todo_list_app.route('/by_netanel_bukris')
def by_netanel_bukris():
    return render_template('by_netanel_bukris.html')

if __name__ == "__main__":
    todo_list_app.run(debug=True)