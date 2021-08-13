from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'Hello there'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)


class users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    address = db.Column(db.String(100))

    def __init__(self, name, email, phone, address):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address


@app.route('/home')
@app.route('/')
def home():
    return render_template('Index.html')


@app.route('/view')
def view():
    return render_template('view.html', values=users.query.all())


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        user = request.form['nm']
        session['user'] = user
        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session['email'] = found_user.email
            session['phone'] = found_user.phone
            session['address'] = found_user.address
        else:
            usr = users(user, '', '', '')
            db.session.add(usr)
            db.session.commit()

        return redirect(url_for('user'))
    else:
        if 'user' in session:
            flash('Already logged in')
            return redirect(url_for('user'))

        return render_template('login.html')


@app.route('/user', methods=['POST', 'GET'])
def user():
    email = None
    phone = None
    address = None
    if 'user' in session:
        user = session['user']
        if request.method == 'POST':
            email = request.form["email"]
            phone = request.form["phone"]
            address = request.form["address"]
            session['email'] = email
            session['phone'] = phone
            session['address'] = address
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            found_user.phone = phone
            found_user.address = address
            db.session.commit()
            return redirect(url_for('view'))
        else:
            if 'email' in session:
                email = session['email']
            if 'phone' in session:
                phone = session['phone']
            if 'address' in session:
                address = session['address']
        return render_template('user.html')
    else:
        flash('You are not logged in')


@app.route('/logout')
def logout():
    flash('You have been logged out')
    session.pop('user', None)
    session.pop('email', None)
    session.pop('phone', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
