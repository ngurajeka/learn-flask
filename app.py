import os
from sqlite3 import dbapi2 as sqlite
from flask import Flask, g, make_response, redirect, render_template, request, url_for
from contextlib import closing

PROJECT_DIR = os.path.dirname(os.path.abspath(__name__))

# apps configuration
DATABASE = os.path.join(PROJECT_DIR, 'app.db')
DEBUG = True
SECRET_KEY='skfjsdalfjadskfl;afka;fdasfdsjafls'
USERNAME='admin'
PASSWORD='test123'

app = Flask(__name__)
app.config.from_object(__name__)

# connecting to database
def connect_db():
	return sqlite.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('apps_schema.sql', mode='r') as file:
			db.cursor().executescript(file.read())
		db.commit()

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/team")
def list_team():
	cur = g.db.execute('select * from team order by id asc')
	teams = [dict(id=row[0], username=row[1], firstname=row[2], lastname=row[3], avatar=row[4], role=row[5]) for row in cur.fetchall()]
	return render_template('team/list.html', teams=teams)

@app.route("/team/add", methods=['POST'])
def add_team():
	g.db.execute('insert into team (username, firstname, lastname, role) values (?, ?, ?, ?)', 
			[request.form['username'], request.form['firstname'], request.form['lastname'], request.form['role']])
	g.db.commit()
	return redirect(url_for('list_team'))

@app.errorhandler(404)
def not_found(error):
	response = make_response(render_template('error.html'), 404)
	return response

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)

