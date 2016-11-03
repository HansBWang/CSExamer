drop table if exists t_user;
drop table if exists t_course;
drop table if exists t_section;
drop table if exists t_quiz;
drop table if exists t_question;
drop table if exists t_quiz_question;
drop table if exists t_quiz_history;
drop table if exists t_submit_history;

create table t_user (
	id integer primary key autoincrement,
	username text unique not null,
	password text not null,
	role integer not null -- 1 student 2 teacher 3 admin
);

create table t_course (
	id integer primary key autoincrement,
	name text not null,
	description text
);

create table t_section (
	id integer primary key autoincrement,
	courseID integer not null,
	name text not null,
	description text
);

create table t_quiz (
	id integer primary key autoincrement,
	sectionID integer not null,
	title text not null,
	description text
);

create table t_question (
	id integer primary key autoincrement,
	question text not null,
	givenCode text not null,
	graderCode text not null
);

create table t_quiz_question (
	quizID integer not null,
	questionID integer not null
);

create table t_submit_history (
	userID integer not null,
	quizID integer not null,
	questionID integer not null,
	answer text not null,
	result text not null,
	time timestamp default current_timestamp
);

-- Insert test data

insert into t_user (username, password, role) values ("Admin", "default", 3);
insert into t_user (username, password, role) values ("Stu1", "123", 1);
insert into t_user (username, password, role) values ("Stu2", "123", 1);
insert into t_user (username, password, role) values ("Stu3", "123", 1);

insert into t_user (username, password, role) values ("Tea1", "123", 2);

insert into t_course (name, description) values ("Course 1", "Course 1 description");

insert into t_section (courseId, name, description) values (1, "Section 1", "Section 1 description");

insert into t_quiz (sectionId, title, description) values (1, "Quiz 1", "It's a test.");
insert into t_quiz (sectionId, title, description) values (1, "Quiz 2", "It's a test.");
insert into t_quiz (sectionId, title, description) values (1, "Quiz 3", "It's a test.");

insert into t_question (question, givenCode, graderCode) values 
(
"Please complete the method to get sum of numbers in a string",
"
public class Quiz {
	public static int getSumOfNumbers(String s) {
		
	}
}
"
,
'
public class Grader {

	public static void main(String[] args){
		int score = 0;
		int scoreMax = 8;
		try{
			if (Quiz.getSumOfNumbers("aabccccAAA")== 0) {
				System.out.println("Test 1 Passed");
				score += 1;
			}else{
				System.out.println("Test 1 faild");
			}
		}catch(Exception e){
			System.out.println("Test 1 faild");
		}
		try{
			if (Quiz.getSumOfNumbers("12 some text 3  7") == 22) {
				System.out.println("Test 2 Passed");
				score += 1;
			}else{
				System.out.println("Test 2 faild");
			}
		}catch(Exception e){
			System.out.println("Test 2 faild");
		}
		try{
			if (Quiz.getSumOfNumbers("12 some text3  7")  == 19) {
				System.out.println("Test 3 Passed");
				score += 1;
			}else{
				System.out.println("Test 3 faild");
			}
		}catch(Exception e){
			System.out.println("Test 3 faild");
		}
		try{
			if (Quiz.getSumOfNumbers("3some") == 0) {
				System.out.println("Test 4 Passed");
				score += 1;
			}else{
				System.out.println("Test 4 faild");
			}
		}catch(Exception e){
			System.out.println("Test 4 faild");
		}
		try{
			if (Quiz.getSumOfNumbers("123") == 123) {
				System.out.println("Test 5 Passed");
				score += 1;
			}else{
				System.out.println("Test 5 faild");
			}
		}catch(Exception e){
			System.out.println("Test 5 faild");
		}
		try{
			if (Quiz.getSumOfNumbers("1 2 3") == 6) {
				System.out.println("Test 6 Passed");
				score += 1;
			}else{
				System.out.println("Test 6 faild");
			}
		}catch(Exception e){
			System.out.println("Test 6 faild");
		}
		try{
			if (Quiz.getSumOfNumbers(" 1 23 ")== 24) {
				System.out.println("Test 7 Passed");
				score += 1;
			}else{
				System.out.println("Test 7 faild");
			}
		}catch(Exception e){
			System.out.println("Test 7 faild");
		}
		try{
			if (Quiz.getSumOfNumbers("")==0) {
				System.out.println("Test 8 Passed");
				score += 1;
			}else{
				System.out.println("Test 8 faild");
			}
		}catch(Exception e){
			System.out.println("Test 8 faild");
		}

		System.out.println("Score: " + score + "/" + scoreMax + " = " + (score*30)/scoreMax);
		if (score != scoreMax) {
			System.exit(1);
		} else {
			System.exit(0);
		}
	}

}
'
);

insert into t_question (question, givenCode, graderCode) values 
(
"Please complete the method to get sum of numbers in a string",
"
public class Quiz {
	public static int getSumOfNumbers(String s) {
		
	}
}
"
,
'
public class Grader {

	public static void main(String[] args){
		int score = 0;
		int scoreMax = 8;
		try{
			if (Quiz.getSumOfNumbers("aabccccAAA")== 0) {
				System.out.println("Test 1 Passed");
				score += 1;
			}else{
				System.out.println("Test 1 faild");
			}
		}catch(Exception e){
			System.out.println("Test 1 faild");
		}
		try{
			if (Quiz.getSumOfNumbers("12 some text 3  7") == 22) {
				System.out.println("Test 2 Passed");
				score += 1;
			}else{
				System.out.println("Test 2 faild");
			}
		}catch(Exception e){
			System.out.println("Test 2 faild");
		}
		try{
			if (Quiz.getSumOfNumbers("12 some text3  7")  == 19) {
				System.out.println("Test 3 Passed");
				score += 1;
			}else{
				System.out.println("Test 3 faild");
			}
		}catch(Exception e){
			System.out.println("Test 3 faild");
		}
		try{
			if (Quiz.getSumOfNumbers("3some") == 0) {
				System.out.println("Test 4 Passed");
				score += 1;
			}else{
				System.out.println("Test 4 faild");
			}
		}catch(Exception e){
			System.out.println("Test 4 faild");
		}
		try{
			if (Quiz.getSumOfNumbers("123") == 123) {
				System.out.println("Test 5 Passed");
				score += 1;
			}else{
				System.out.println("Test 5 faild");
			}
		}catch(Exception e){
			System.out.println("Test 5 faild");
		}
		try{
			if (Quiz.getSumOfNumbers("1 2 3") == 6) {
				System.out.println("Test 6 Passed");
				score += 1;
			}else{
				System.out.println("Test 6 faild");
			}
		}catch(Exception e){
			System.out.println("Test 6 faild");
		}
		try{
			if (Quiz.getSumOfNumbers(" 1 23 ")== 24) {
				System.out.println("Test 7 Passed");
				score += 1;
			}else{
				System.out.println("Test 7 faild");
			}
		}catch(Exception e){
			System.out.println("Test 7 faild");
		}
		try{
			if (Quiz.getSumOfNumbers("")==0) {
				System.out.println("Test 8 Passed");
				score += 1;
			}else{
				System.out.println("Test 8 faild");
			}
		}catch(Exception e){
			System.out.println("Test 8 faild");
		}

		System.out.println("Score: " + score + "/" + scoreMax + " = " + (score*30)/scoreMax);
		if (score != scoreMax) {
			System.exit(1);
		} else {
			System.exit(0);
		}
	}

}
'
);

insert into t_question (question, givenCode, graderCode) values 
(
"Please complete the method to get sum of numbers in a string",
"
public class Quiz {
	public static int getSumOfNumbers(String s) {
		
	}
}
"
,
'
public class Grader {

	public static void main(String[] args){
		int score = 0;
		int scoreMax = 8;
		try{
			if (Quiz.getSumOfNumbers("aabccccAAA")== 0) {
				System.out.println("Test 1 Passed");
				score += 1;
			}else{
				System.out.println("Test 1 faild");
			}
		}catch(Exception e){
			System.out.println("Test 1 faild");
		}
		try{
			if (Quiz.getSumOfNumbers("12 some text 3  7") == 22) {
				System.out.println("Test 2 Passed");
				score += 1;
			}else{
				System.out.println("Test 2 faild");
			}
		}catch(Exception e){
			System.out.println("Test 2 faild");
		}
		try{
			if (Quiz.getSumOfNumbers("12 some text3  7")  == 19) {
				System.out.println("Test 3 Passed");
				score += 1;
			}else{
				System.out.println("Test 3 faild");
			}
		}catch(Exception e){
			System.out.println("Test 3 faild");
		}
		try{
			if (Quiz.getSumOfNumbers("3some") == 0) {
				System.out.println("Test 4 Passed");
				score += 1;
			}else{
				System.out.println("Test 4 faild");
			}
		}catch(Exception e){
			System.out.println("Test 4 faild");
		}
		try{
			if (Quiz.getSumOfNumbers("123") == 123) {
				System.out.println("Test 5 Passed");
				score += 1;
			}else{
				System.out.println("Test 5 faild");
			}
		}catch(Exception e){
			System.out.println("Test 5 faild");
		}
		try{
			if (Quiz.getSumOfNumbers("1 2 3") == 6) {
				System.out.println("Test 6 Passed");
				score += 1;
			}else{
				System.out.println("Test 6 faild");
			}
		}catch(Exception e){
			System.out.println("Test 6 faild");
		}
		try{
			if (Quiz.getSumOfNumbers(" 1 23 ")== 24) {
				System.out.println("Test 7 Passed");
				score += 1;
			}else{
				System.out.println("Test 7 faild");
			}
		}catch(Exception e){
			System.out.println("Test 7 faild");
		}
		try{
			if (Quiz.getSumOfNumbers("")==0) {
				System.out.println("Test 8 Passed");
				score += 1;
			}else{
				System.out.println("Test 8 faild");
			}
		}catch(Exception e){
			System.out.println("Test 8 faild");
		}

		System.out.println("Score: " + score + "/" + scoreMax + " = " + (score*30)/scoreMax);
		if (score != scoreMax) {
			System.exit(1);
		} else {
			System.exit(0);
		}
	}

}
'
);

insert into t_quiz_question (quizID, questionID) values (1,1);
insert into t_quiz_question (quizID, questionID) values (1,2);
insert into t_quiz_question (quizID, questionID) values (1,3);

insert into t_quiz_question (quizID, questionID) values (2,1);
insert into t_quiz_question (quizID, questionID) values (2,2);

insert into t_quiz_question (quizID, questionID) values (3,3);