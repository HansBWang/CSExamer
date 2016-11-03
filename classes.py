class Course(object):
	"""docstring for Course"""
	def __init__(self, id, name, description):
		super(Course, self).__init__()
		self.id = id
		self.name = name
		self.description = description
		self.sections = None

	def getSections(self, db):
		if self.sections is None:
			self.sections = []
			cur = db.execute('select id, courseID, name, description from t_section where courseID='+str(self.id))
			results = cur.fetchall()
			for result in results:
				section = Section(result[0],result[1],result[2],result[3])
				self.sections.append(section)
		return self.sections

	@classmethod	
	def getCourseFromDB(self, id, db):
		cur = db.execute('select name, description from t_course where id=?', (id,))
		result = cur.fetchone()
		course = Course(id, result[0], result[1])
		return course

	@classmethod
	def getAllCourses(self, db):
		cur = db.execute('select id, name, description from t_course')
		result = cur.fetchall()
		courses = []
		for data in result:
			course = Course(data[0],data[1],data[2])
			courses.append(course)
		return courses

class Section(object):
	"""docstring for Course"""
	def __init__(self, id, courseID, name, description):
		super(Section, self).__init__()
		self.id = id
		self.courseID = courseID
		self.name = name
		self.description = description
		self.quizzes = None

	def getQuizzes(self, db):
		if self.quizzes is None:
			self.quizzes = []
			cur = db.execute('select id, sectionID, title, description from t_quiz where sectionID='+str(self.id))
			results = cur.fetchall()
			for result in results:
				quiz = Quiz(result[0],result[1],result[2],result[3])
				self.quizzes.append(quiz)
		return self.quizzes

	@classmethod	
	def getSectionFromDB(self, id, db):
		cur = db.execute('select courseID, name, description from t_section where id=?', (id,))
		result = cur.fetchone()
		section = Section(id, result[0], result[1], result[2])
		return section

class Quiz(object):
	"""docstring for Quiz"""
	def __init__(self, id, sectionID, title, description):
		super(Quiz, self).__init__()
		self.id = id
		self.sectionID = sectionID
		self.title = title
		self.description = description
		self.questions = None

	def getQuestions(self, db):
		if self.questions is None:
			self.questions = []
			cur = db.execute('select questionID from t_quiz_question where quizID='+str(self.id))
			results = cur.fetchall()
			for result in results:
				questionID = result[0]
				question = Question.getQuestionFromDB(questionID,db)
				self.questions.append(question)
		return self.questions
	
	@classmethod
	def getQuizFromDB(self, id, db):
		cur = db.execute('select sectionID,title, description from t_quiz where id=?', (id,))
		result = cur.fetchone()
		quiz = Quiz(id, result[0], result[1], result[2])
		return quiz
	
	# @classmethod
	# def getAllQuizzes(self, db):
	# 	cur = db.execute('select id, title, description from t_quiz')
	# 	result = cur.fetchall()
	# 	quizzes = []
	# 	for data in result:
	# 		quiz = Quiz(data[0],data[1],data[2])
	# 		quizzes.append(quiz)
	# 	return quizzes

class Question(object):
	"""docstring for Question"""
	def __init__(self, id, question, givenCode):
		super(Question, self).__init__()
		self.id = id
		self.question = question
		self.givenCode = givenCode

	@classmethod
	def getQuestionFromDB(self, id, db):
		cur = db.execute('select question, givenCode from t_question where id=?', (id,))
		result = cur.fetchone()
		question = Question(id,result[0],result[1])
		return question

	@classmethod
	def getGraderCodeFromDB(self, id, db):
		cur = db.execute('select graderCode from t_question where id=?', (id,))
		result = cur.fetchone()
		graderCode = result[0]
		return graderCode

class User(object):
	"""docstring for User"""
	def __init__(self, id, db):
		super(User, self).__iniid, db()
		self.id = id
		cur = db.execute('select username, role from t_user where id=?', (id,))
		result = cur.fetchone()
		self.username = result[0]
		self.role = result[1]

class SubmitHistory(object):
	"""docstring for SubmitHistory"""
	def __init__(self, userID, quizID, questionID, answer, result, time):
		super(SubmitHistory, self).__init__()
		self.userID = userID
		self.quizID = quizID
		self.questionID = questionID
		self.answer = answer
		self.result = result
		self.time = time
	
	@classmethod
	def insertHistoryToDB(self, userID, quizID, questionID, answer, result, db):
		db.execute("insert into t_submit_history (userID, quizID, questionID, answer, result) values (?,?,?,?,?)", (userID, quizID, questionID, answer, result))
		db.commit()

	@classmethod
	def getHistoriesFromDB(self, userID, quizID, questionID, db):
		cur = db.execute('select answer, result, time from t_submit_history where userID=? and quizID=? and questionID=? order by time desc', (userID,quizID,questionID))
		results = cur.fetchall()
		histories = []
		for result in results:
			history = SubmitHistory(userID,quizID,questionID,result[0],result[1],result[2])
			histories.append(history)

		return histories