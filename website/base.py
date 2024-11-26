from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from . import db

base = Blueprint('base', __name__)

class User(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(50))
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        
@base.route('/', methods=['POST', 'GET'])
def clear_session():
    session.clear()
    return redirect(url_for('base.Home'))

@base.route('/home', methods=['POST', 'GET'])
def Home():
    # db.session.query(User).delete()
    # db.session.commit()
    if 'logged_in?' in session:
        if session['logged_in?'] == True:
            print('home (logged in)')
            name = session['name']
            flash(f'Hello {name}, you have logged in!', 'success')
            return render_template('index.html')
        else:
            print('Home (session[logged_in?] is false)')
        return render_template('index.html')
    else:
        print('Home (logged out)')
        return render_template('index.html')

@base.route('/members', methods=['POST', 'GET'])
def Members():
    print('Members')
    return render_template('members.html')

@base.route('/swag', methods=['POST', 'GET'])
def Swag():
    print('Swag')
    return render_template('swag.html')

@base.route('/login', methods=['POST', 'GET'])
def Login():
    if request.method == 'POST':
        print('login: inside if')
        email = request.form['email-login']
        password = request.form['password-login']
        emails_passwords = db.session.query(User.email, User.password).all()
        database_emails = [email[0] for email in emails_passwords]
        database_passwords = [password[1] for password in emails_passwords]
        print(database_emails)
        print(database_passwords)
        if email in database_emails and password in database_passwords:
            user = User.query.filter_by(email=email).first()
            session['email'] = email
            session['password'] = password
            session['name'] = user.name
            session['logged_in?'] = True
            return redirect(url_for('base.Home'))
        else:
            return 'not logged in'
    else:
        print('login: outside if')
        return render_template('login.html')

@base.route('/signup', methods=['POST', 'GET'])
def SignUp():
    if request.method == 'POST':
        print('Sign-up: inside if')
        name = request.form['signup-name']
        email = request.form['signup-email']
        password = request.form['signup-password']
        emails_passwords = db.session.query(User.email, User.password).all()
        database_emails = [email[0] for email in emails_passwords]
        if email in database_emails:
            flash('email already taken, did you spell it correctly?')
            return redirect(url_for('base.SignUp'))
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        session['logged_in?'] = False
        return redirect(url_for('base.Login'))
    else:
        print('Sign-up: outside if')
        return render_template('signup.html')