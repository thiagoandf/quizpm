# -*-coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/quizpm'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(80), nullable=False)
    is_teacher = db.Column(db.Boolean, default=False)

    def __init__(self, id, password, is_teacher):
        self.id = id
        self.password = generate_password_hash(password)
        self.is_teacher = is_teacher

    def __repr__(self):
        return u"User - id={0}".format(self.id)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    points_lifetime = db.Column(db.Integer, index=True, default=0)
    points_current = db.Column(db.Integer, index=True, default=0)
    gender = db.Column(db.String(20), index=True, nullable=False)
    age = db.Column(db.Integer, index=True, nullable=False)
    semester = db.Column(db.Integer, index=True, default=1)
    current_avatar = db.Column(db.Integer, db.ForeignKey('avatar.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete='cascade'))
    purchases = db.relationship('Purchase', backref='student')
    questions_answered = db.relationship('AnsweredQuestion', backref='student')

    def __init__(self, id, name, gender, age, semester, course_id):
        self.id = id
        self.name = name
        self.gender = gender
        self.age = age
        self.semester = semester
        self.course_id = course_id

    def __repr__(self):
        return u"Student - id={0}".format(self.id)


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    students = db.relationship('Student', backref='course')
    categories = db.relationship('Category', backref='course')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return u'Course - id={0}'.format(self.id)


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete='cascade'))
    questions = db.relationship('Question', backref='category ')

    def __init__(self, name, course_id):
        self.name = name
        self.course_id = course_id

    def __repr__(self):
        return u'Category - id={0}'.format(self.id)


class Avatar(db.Model):
    __tablename__ = 'avatar'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Integer, index=True, default=0)
    image_path = db.Column(db.String(64), nullable=False)
    purchases = db.relationship('Purchase', backref='avatar')
    usedby = db.relationship('Student', backref='avatar')

    def __init__(self, name, price, image_path):
        self.name = name
        self.price = price
        self.image_path = image_path

    def __repr__(self):
        return u"Avatar - id={0}".format(self.id)


class Purchase(db.Model):
    __tablename__ = 'purchase'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    avatar_id = db.Column(db.Integer, db.ForeignKey('avatar.id', ondelete='cascade'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='cascade'))

    def __init__(self, timestamp, avatar_id, student_id):
        self.timestamp = timestamp
        self.avatar_id = avatar_id
        self.student_id = student_id

    def __repr__(self):
        return u"Purchase - id={0}".format(self.id)


class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    questions = db.relationship('Question', backref='teacher')

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return u"Teacher - id={0}".format(self.id)


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(164), nullable=False)
    difficulty = db.Column(db.String(64), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id', ondelete='cascade'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='cascade'))
    alternatives = db.relationship('Alternative', backref='question')
    questions_answered = db.relationship('AnsweredQuestion', backref='question')

    def __init__(self, text, difficulty, teacher_id, category_id):
        self.text = text
        self.difficulty = difficulty
        self.teacher_id = teacher_id
        self.category_id = category_id

    def __repr__(self):
        return u"Question - id={0}".format(self.id)


class Alternative(db.Model):
    __tablename__ = 'alternative'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(164), nullable=False)
    correction_text = db.Column(db.String(164), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='cascade'))

    def __init__(self, text, correction_text, is_correct, question_id):
        self.text = text
        self.correction_text = correction_text
        self.is_correct = is_correct
        self.question_id = question_id

    def __repr__(self):
        return u"Alternative - id={0}".format(self.id)


class AnsweredQuestion(db.Model):
    __tablename__ = 'answered_question'
    id = db.Column(db.Integer, primary_key=True)
    accumulated_points = db.Column(db.Integer, default=0)
    failed_attempts = db.Column(db.Integer, default=0)
    time_taken = db.Column(db.Time, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='cascade'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='cascade'))

    def __init__(self, failed_attempts, time_taken, student_id, question_id):
        self.failed_attempts = failed_attempts
        self.time_taken = time_taken
        self.student_id = student_id
        self.question_id = question_id

    def __repr__(self):
        return u"Answered Question - id={0}".format(self.id)

