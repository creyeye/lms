from peewee import SqliteDatabase, Model, CharField, ForeignKeyField, TextField, DateTimeField, IntegerField
from datetime import datetime


database = SqliteDatabase('lms.db')


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    username = CharField()
    password = CharField(max_length=25)
    role = CharField()


class Course(BaseModel):
    title = CharField()
    description = CharField()


class Lesson(BaseModel):
    course = ForeignKeyField(Course, backref='lessons')
    title = CharField()
    content = TextField()


class Task(BaseModel):
    lesson = ForeignKeyField(Lesson, backref='tasks')
    description = TextField()
    deadline = DateTimeField()
    max_score = IntegerField()


class Submission(BaseModel):
    student = ForeignKeyField(User, backref='submissions')
    task = ForeignKeyField(Task, backref='submissions')
    solution = TextField()
    submitted_at = DateTimeField(default=datetime.now())
    score = IntegerField(default=0)
    teacher_comments = TextField(default=' ')


User.create_table()
Course.create_table()
Lesson.create_table()
Task.create_table()
Submission.create_table()
