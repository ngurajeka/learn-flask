import os
from sqlite3 import dbapi2 as sqlite
from flask import Flask, g, make_response, redirect, render_template, request, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from contextlib import closing

PROJECT_DIR = os.path.dirname(os.path.abspath(__name__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(PROJECT_DIR, 'apps.db')

db = SQLAlchemy(app)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(50), unique=True)
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32))
    role = db.Column(db.String(15))

    def __init__(self, username, email, firstname, lastname, role):
        self.username = username
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.role = role

    def __repr__(self):
        return '<User %r>' % self.username

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/team")
def list_team():
    teams = Team.query.all()
    return render_template('team/list.html', teams=teams)

@app.route("/team/add", methods=['POST'])
def add_team():
    username = request.form['username']
    email = request.form['email']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    role = request.form['role']
    if username and email and firstname and lastname and role:
        team = Team(username, email, firstname, lastname, role)
        db.session.add(team)
        db.session.commit()
    return redirect(url_for('list_team'))

@app.errorhandler(404)
def not_found(error):
    response = make_response(render_template('error.html'), 404)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001, debug=True)
