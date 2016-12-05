import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
	 render_template, flash

from checker import Checker

from classes import Course, Section, Quiz, Question

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
		cur = db.execute('select id, password, role from t_user where username=?', (request.form['username'],))
		result = cur.fetchall()
		if len(result) == 1:
			if request.form['password'] != result[0][1]:
				error = 'Invalid password'
			else:
				session['logged_in'] = True
				session['userid'] = result[0][0]
				session['username'] = username
				session['role'] = result[0][2]
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
    session.pop('role',None)
    flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/add_entity', methods=['GET','POST'])
def add_entity():
	etype = request.args.get('entity_type')
	sid = request.args.get('super_entity_id')
	if request.method == 'POST':
		name = request.form['name']
		description = request.form['description']
		db = get_db()
		
		if etype == 'Course':
			db.execute("insert into t_course (name, description) values (?,?)", (name, description))
			db.commit()
			flash('Success')
			return redirect(url_for('show_homepage'))
		if etype == 'Section':
			db.execute("insert into t_section (courseID, name, description) values (?,?,?)", (sid, name, description))
			db.commit()
			flash('Success')
			return redirect(url_for('show_course', courseID=sid))
		elif etype == 'Quiz':
			db.execute("insert into t_quiz (sectionID, title, description) values (?,?,?)", (sid, name, description))
			db.commit()
			flash('Success')
			return redirect(url_for('show_section', sectionID=sid))
		else:
			flash('unsupported type error')
			return redirect(url_for('show_homepage'))
	else:
		return render_template('add_entity.html', entity_type = etype, super_entity_id = sid)

@app.route('/')
def show_homepage():
	if not session.get('logged_in'):
		return redirect(url_for('login'))
	
	role = session['role']
	db = get_db()

	# teacher
	if role>1:
		courses = Course.getAllCourses(db)
		return render_template('homepage_t.html', courses = courses)
	else:
		return render_template('homepage_s.html', sections = [])

@app.route('/show_course')
def show_course():
	if not session.get('logged_in'):
		return redirect(url_for('login'))

	courseID = int(request.args.get('courseID'))
	db = get_db()
	
	course = Course.getCourseFromDB(courseID,db)
	sections = course.getSections(db)

	return render_template('course.html', course = course, sections = sections)

@app.route('/show_question_pool')
def show_question_pool():
	if not session.get('logged_in'):
		return redirect(url_for('login'))

	courseID = int(request.args.get('courseID'))
	db = get_db()
	
	course = Course.getCourseFromDB(courseID,db)
	questions = course.getQuestions(db)

	return render_template('question_pool.html', course = course, questions = questions)

@app.route('/new_question', methods=['GET','POST'])
def new_question():
	if not session.get('logged_in'):
		return redirect(url_for('login'))

	courseID = int(request.args.get('courseID'))
	db = get_db()	
	if request.method == 'POST':
		if request.form['action'] != 'cancel':
			question = request.form['question']
			givenCode = request.form['givenCode']
			graderCode = request.form['graderCode']
			Question.newQuestion(courseID,question,givenCode,graderCode,db)
			flash("Question saved!")
		if request.form['action'] != 'save&next':
			return redirect(url_for('show_question_pool', courseID = courseID))

	return render_template('new_question.html', courseID = courseID)

@app.route('/edit_question', methods=['GET','POST'])
def edit_question():
	if not session.get('logged_in'):
		return redirect(url_for('login'))

	courseID = int(request.args.get('courseID'))
	questionID = int(request.args.get('questionID'))

	db = get_db()	
	q = Question.getQuestionFromDB(questionID,db)

	if request.method == 'POST':
		if request.form['action'] == 'save':
			q.question = request.form['question']
			q.givenCode = request.form['givenCode']
			q.graderCode = request.form['graderCode']
			q.saveDB(db)
			flash("Question saved!")
			return redirect(url_for('show_question_pool', courseID = courseID))

	return render_template('edit_question.html', courseID = courseID, question = q)

@app.route('/show_quizzes')
def show_quizzes():
	if not session.get('logged_in'):
		return redirect(url_for('login'))
	
	courseID = int(request.args.get('courseID'))
	db = get_db()
	course = Course.getCourseFromDB(courseID,db)
	quizzes = course.getQuizzes(db)
	return render_template('quizzes.html', course = course, quizzes = quizzes)

@app.route('/new_quiz', methods=['GET','POST'])
def new_quiz():
	if not session.get('logged_in'):
		return redirect(url_for('login'))

	courseID = int(request.args.get('courseID'))
	db = get_db()	
	course = Course.getCourseFromDB(courseID,db)
	sections = course.getSections(db)
	questions = course.getQuestions(db)

	if request.method == 'POST':
		if request.form['action'] == 'save':
			title = request.form['title']
			description = request.form['description']
			sectionIds = request.form.getlist('section')
			questionIds = request.form.getlist('question')
			Quiz.newQuiz(title, description, sectionIds, questionIds, db)
			flash("Quiz saved!")
		return redirect(url_for('show_quizzes', courseID=courseID))

	return render_template('new_quiz.html', courseID = courseID, sections = sections, questions = questions)

@app.route('/show_section')
def show_section():
	if not session.get('logged_in'):
		return redirect(url_for('login'))

	sectionID = int(request.args.get('sectionID'))
	db = get_db()
	
	section = Section.getSectionFromDB(sectionID,db)
	quizzes = section.getQuizzes(db)

	return render_template('section.html', section = section, quizzes = quizzes)

# @app.route('/show_quiz')
# def show_quiz():
# 	if not session.get('logged_in'):
# 		return redirect(url_for('login'))

# 	quizID = int(request.args.get('quizID'))
# 	db = get_db()
# 	quiz = Quiz.getQuizFromDB(quizID,db)
# 	questions = quiz.getQuestions(db)
# 	return render_template('quiz.html', quiz = quiz, questions = questions)

# @app.route('/show_question')
# def show_question():
# 	if not session.get('logged_in'):
# 		return redirect(url_for('login'))

# 	db = get_db()
# 	quizID = int(request.args.get('quizID'))
# 	questionID = int(request.args.get('questionID'))
# 	quiz = Quiz.getQuizFromDB(quizID,db)
# 	question = Question.getQuestionFromDB(questionID,db)
# 	userID = session['userid']
# 	histories = SubmitHistory.getHistoriesFromDB(userID, quizID, questionID, db)

# 	return render_template('question.html', quiz = quiz, question = question, histories = histories)

# @app.route('/submit', methods=['POST'])
# def submit_answer():
# 	if not session.get('logged_in'):
# 		abort(401)

# 	db = get_db()
# 	quizID = int(request.args.get('quizID'))
# 	questionID = int(request.args.get('questionID'))
# 	userID = session['userid']

# 	code = request.form['text']

# 	graderCode = Question.getGraderCodeFromDB(questionID,db)
# 	checker = Checker()
# 	result = checker.runCheck(code,graderCode)
# 	answer = code

# 	SubmitHistory.insertHistoryToDB(userID, quizID, questionID, answer, result, db)

# 	flash(result)

# 	return redirect(url_for('show_question', quizID = quizID, questionID = questionID))