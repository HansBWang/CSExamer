import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
	 render_template, flash

from checker import Checker

from classes import Quiz, Question, SubmitHistory

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'CSExamer.db'),
	SECRET_KEY='development key',
))
app.config.from_envvar('CSEXAMER_SETTINGS', silent=True)

def connect_db():
	app.logger.debug('connect_db')
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

def get_db():
	app.logger.debug('get_db()')
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

def init_db():
	db = get_db()
	with app.open_resource("schema.sql", mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print 'Initialized the database.'

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

@app.route('/login', methods=['GET','POST'])
def login():
	error = None
	username = None
	if request.method == 'POST':
		username = request.form['username']
		db = get_db()
		cur = db.execute('select id, password from t_user where username=?', (request.form['username'],))
		result = cur.fetchall()
		if len(result) == 1:
			if request.form['password'] != result[0][1]:
				error = 'Invalid password'
			else:
				session['logged_in'] = True
				session['userid'] = result[0][0]
				session['username'] = username
				flash('You were logged in')
				return redirect(url_for('show_homepage'))
		else:
			error = 'Invalid username'

	return render_template('login.html', error=error, username=username)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('userid', None)
    session.pop('username', None)
    flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/')
def show_homepage():
	if not session.get('logged_in'):
		return redirect(url_for('login'))

	db = get_db()
	quizzes = Quiz.getAllQuizzes(db)

	return render_template('homepage.html', quizzes = quizzes)

@app.route('/show_quiz')
def show_quiz():
	if not session.get('logged_in'):
		return redirect(url_for('login'))

	quizID = int(request.args.get('quizID'))
	db = get_db()
	quiz = Quiz.getQuizFromDB(quizID,db)
	questions = quiz.getQuestions(db)
	return render_template('quiz.html', quiz = quiz, questions = questions)

@app.route('/show_question')
def show_question():
	if not session.get('logged_in'):
		return redirect(url_for('login'))

	db = get_db()
	quizID = int(request.args.get('quizID'))
	questionID = int(request.args.get('questionID'))
	quiz = Quiz.getQuizFromDB(quizID,db)
	question = Question.getQuestionFromDB(questionID,db)
	userID = session['userid']
	histories = SubmitHistory.getHistoriesFromDB(userID, quizID, questionID, db)

	return render_template('question.html', quiz = quiz, question = question, histories = histories)

@app.route('/submit', methods=['POST'])
def submit_answer():
	if not session.get('logged_in'):
		abort(401)

	db = get_db()
	quizID = int(request.args.get('quizID'))
	questionID = int(request.args.get('questionID'))
	userID = session['userid']

	code = request.form['text']

	graderCode = Question.getGraderCodeFromDB(questionID,db)
	checker = Checker()
	result = checker.runCheck(code,graderCode)
	answer = code

	SubmitHistory.insertHistoryToDB(userID, quizID, questionID, answer, result, db)

	flash(result)

	return redirect(url_for('show_question', quizID = quizID, questionID = questionID))

