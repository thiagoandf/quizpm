# -*-coding: utf-8 -*-

from database import db
from database import Teacher

db.drop_all()
db.create_all()

# Ordem para inserir dados:
# Course
# Teacher
# Category
# Question
# Alternative
# Avatar
# Student
# Purchase
# QuestionAnswered
# User

jailson = Teacher(id = 11510001, name='Jailson Mendes')
db.session.add(jailson)
db.session.commit()