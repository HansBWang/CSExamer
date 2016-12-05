class Course(object):
	"""docstring for Course"""
	def __init__(self, id, name, description):
		super(Course, self).__init__()
		self.id = id
		self.name = name
		self.description = description
		self.sections = None
		self.quizzes = None
		self.questions = None

	def getSections(self, db):
		if self.sections is None:
			self.sections = []
			cur = db.execute('select id, courseID, name, description from t_section where courseID='+str(self.id))
			results = cur.fetchall()
			for result in results:
				section = Section(result[0],result[1],result[2],result[3])
				self.sections.append(section)
		return self.sections

	def getQuizzes(self, db):
		if self.quizzes is None:
			self.quizzes = []
			self.getSections(db)
			for sec in self.sections:
				quizzes = sec.getQuizzes(db)
				for q in quizzes:
					self.quizzes.append(q)
		return self.quizzes	

	def getQuestions(self, db):
		if self.questions is None:
			self.questions = []
			cur = db.execute('select id from t_question where courseID='+str(self.id))
			results = cur.fetchall()
			for result in results:
				questionID = result[0]
				question = Question.getQuestionFromDB(questionID,db)
				self.questions.append(question)
		return self.questions

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
			cur = db.execute('select quizId from t_section_quiz where sectionId='+str(self.id))
			results = cur.fetchall()
			for result in results:
				quizID = result[0]
				quiz = Quiz.getQuizFromDB(quizID, db)
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
	def __init__(self, id, title, description, isPublished):
		super(Quiz, self).__init__()
		self.id = id
		self.title = title
		self.description = description
		self.isPublished = isPublished
		self.questions = None
		self.sections = None

	def getQuestionIds(self, db):
		if self.questions is None:
			self.questions = []
			cur = db.execute('select questionID from t_quiz_question where quizID='+str(self.id))
			results = cur.fetchall()
			questionIds = []
			for result in results:
				questionIds.append(result[0])
		return questionIds

	def getQuestions(self, db):
		if self.questions is None:
			self.questions = []
			qIds = self.getQuestionIds(db)
			for questionID in qIds:
				question = Question.getQuestionFromDB(questionID,db)
				self.questions.append(question)
		return self.questions

	def getSectionIds(self,db):
		cur = db.execute('select sectionId from t_section_quiz where quizId='+str(self.id))
		results = cur.fetchall()
		secIds = []
		for result in results:
			secIds.append(result[0])
		return secIds
		
	def getSections(self,db):
		if self.sections is None:
			self.sections = []
			secIds = self.getSectionIds(db)
			for sectionID in secIds:
				section = Section.getSectionFromDB(sectionID,db)
				self.sections.append(question)
		return self.sections

	def saveChanges(self, sectionIds, questionIds, db):
		db.execute("update t_quiz set title=?, description=?, isPublished=? where id=?", (self.title, self.description, self.isPublished, self.id))
		db.execute("delete from t_quiz_question where quizId="+str(self.id))
		db.execute("delete from t_section_quiz where quizId="+str(self.id))
		for secId in sectionIds:	
			db.execute("insert into t_section_quiz (quizId,sectionId) values (?,?)", (self.id,secId))
		for qId in questionIds:
			db.execute("insert into t_quiz_question (quizId,questionId) values (?,?)", (self.id,qId))
		db.commit()

	@classmethod	
	def newQuiz(self, title, description, sectionIds, questionIds, db):
		db.execute("insert into t_quiz (title, description) values (?,?)", (title, description))
		cur = db.execute("select max(id) from t_quiz")
		newQuizId = (cur.fetchone())[0]
		
		for secId in sectionIds:	
			db.execute("insert into t_section_quiz (quizId,sectionId) values (?,?)", (newQuizId,secId))

		for qId in questionIds:
			db.execute("insert into t_quiz_question (quizId,questionId) values (?,?)", (newQuizId,qId))

		db.commit()

	@classmethod
	def getQuizFromDB(self, id, db):
		cur = db.execute('select title, description, isPublished from t_quiz where id=?', (id,))
		result = cur.fetchone()
		quiz = Quiz(id, result[0], result[1], result[2])
		return quiz

class Question(object):
	"""docstring for Question"""
	def __init__(self, id, question, givenCode, graderCode):
		super(Question, self).__init__()
		self.id = id
		self.question = question
		self.givenCode = givenCode
		self.graderCode = graderCode

	def saveDB(self,db):
		db.execute("update t_question set question=?, givenCode=?, graderCode=? where id=?", (self.question, self.givenCode, self.graderCode, self.id))
		db.commit()

	@classmethod
	def newQuestion(self, courseId, question, givenCode, graderCode, db):
		db.execute("insert into t_question (courseId, question, givenCode, graderCode) values (?,?,?,?)", (courseId, question, givenCode, graderCode))
		db.commit()

	@classmethod
	def getQuestionFromDB(self, id, db):
		cur = db.execute('select question, givenCode, graderCode from t_question where id=?', (id,))
		result = cur.fetchone()
		question = Question(id,result[0],result[1],result[2])
		return question
		

# class User(object):
# 	"""docstring for User"""
# 	def __init__(self, id, db):
# 		super(User, self).__iniid, db()
# 		self.id = id
# 		cur = db.execute('select username, role from t_user where id=?', (id,))
# 		result = cur.fetchone()
# 		self.username = result[0]
# 		self.role = result[1]

# class SubmitHistory(object):
# 	"""docstring for SubmitHistory"""
# 	def __init__(self, userID, quizID, questionID, answer, result, time):
# 		super(SubmitHistory, self).__init__()
# 		self.userID = userID
# 		self.quizID = quizID
# 		self.questionID = questionID
# 		self.answer = answer
# 		self.result = result
# 		self.time = time
	
# 	@classmethod
# 	def insertHistoryToDB(self, userID, quizID, questionID, answer, result, db):
# 		db.execute("insert into t_submit_history (userID, quizID, questionID, answer, result) values (?,?,?,?,?)", (userID, quizID, questionID, answer, result))
# 		db.commit()

# 	@classmethod
# 	def getHistoriesFromDB(self, userID, quizID, questionID, db):
# 		cur = db.execute('select answer, result, time from t_submit_history where userID=? and quizID=? and questionID=? order by time desc', (userID,quizID,questionID))
# 		results = cur.fetchall()
# 		histories = []
# 		for result in results:
# 			history = SubmitHistory(userID,quizID,questionID,result[0],result[1],result[2])
# 			histories.append(history)

# 		return histories