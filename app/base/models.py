# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask.json import jsonify
from flask_login import UserMixin
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.types import TypeDecorator
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import Binary, Column, Integer, String, DateTime, Text
import uuid, datetime
from app import db, login_manager

from app.base.util import hash_pass


class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String(10), unique=True)
    email = Column(String(30), unique=True)
    password = Column(Binary)
    roles = db.relationship('Role', secondary='user_roles')

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass( value ) # we need bytes here (not plain str)
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('User.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))





class UserRaffle(db.Model):
    __tablename__ =  "users_raffle"

    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(14), unique=True)
    name = db.Column(db.String(255))
    email =  db.Column(db.String(255))
    phone = db.Column(db.String(255))
 
    def __init__(self, cpf, name, email, phone ):
        self.cpf = cpf
        self.name = name
        self.email = email
        self.phone = phone

    def __repr__(self):
        return  "User: %r" % self.name

class ListRaffle(db.Model):
    __tablename__ = "list_raffle"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.String(255))
    description_brief = db.Column(db.String(255))
    thumbnail = db.Column(db.String(255))
    date_raffle = db.Column(db.DateTime)
    date_course_start = db.Column(db.DateTime)
    date_course_finish = db.Column(db.DateTime)
    number_of_vacancies = db.Column(db.Integer)
    active = db.Column(db.Boolean)

    def __init__(self, title, description,description_brief, thumbnail, date_raffle,date_course_start,date_course_finish, number_of_vacancies, active):

      self.title = title
      self.description = description
      self.description_brief = description_brief
      self.thumbnail = thumbnail
      self.date_raffle = date_raffle
      self.date_course_start = date_course_start
      self.date_course_finish = date_course_finish
      self.number_of_vacancies = number_of_vacancies
      self.active = active
    
    def __repr__(self):
        return '<Bolsa: %r>' % self.title

    
class Subscribed_Raffle(db.Model):
    __tablename__ = "subscribers_raffle"

    id =   db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users_raffle.id'))
    raffle_id = db.Column(db.Integer, db.ForeignKey('list_raffle.id'))   

    user = db.relationship('UserRaffle', foreign_keys=user_id)
    raffle = db.relationship('ListRaffle', foreign_keys=raffle_id)  

    def __init__(self, user_id, raffle_id):
    
      self.user_id = user_id
      self.raffle_id = raffle_id




class Winners_List(db.Model):
    __tablename__ = "winners_list"

    id =   db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users_raffle.id'))
    raffle_id = db.Column(db.Integer, db.ForeignKey('list_raffle.id'))
    delivered_the_article = db.Column(db.Boolean)
    article_link = db.Column(db.String(255))

    user = db.relationship('UserRaffle', foreign_keys=user_id)
    raffle = db.relationship('ListRaffle', foreign_keys=raffle_id)  

    
    def __init__(self, user_id, raffle_id,delivered_the_article, article_link):

      self.user_id = user_id
      self.raffle_id = raffle_id
      self.delivered_the_article = delivered_the_article
      self.article_link = article_link

class Members(db.Model):
    __tablename__ =  "members"

    uuid = db.Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True )
    created_date = Column(DateTime(timezone=True), default=func.now())
    cpf = db.Column(db.String(14), unique=True)
    name = db.Column(db.String(255))
    email =  db.Column(db.String(255))
    phone = db.Column(db.String(255))
    linkedin = db.Column(db.String(255))
    instagram = db.Column(db.String(255))
    facebook = db.Column(db.String(255))
    is_black_people = db.Column(db.Boolean)

    
 
    def __init__(self, cpf, name, email, phone, linkedin, instagram , facebook, is_back_people ):
        self.cpf = cpf
        self.name = name
        self.email = email
        self.phone = phone
        self.linkedin = linkedin
        self.instagram = instagram
        self.facebook = facebook
        self.is_back_people = is_back_people

    def __repr__(self):
        return  self.name

class MembersAdress(db.Model):
    __tablename__ =  "members_address"

    uuid = db.Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True )
    created_date = Column(DateTime(timezone=True), default=func.now())
    cep = db.Column(db.String(14))
    country = db.Column(db.String(255))
    state =  db.Column(db.String(255))
    city = db.Column(db.String(255))
    district = db.Column(db.String(255))
    user_id = db.Column(UUID(), db.ForeignKey('members.uuid'), unique=True)

    member = db.relationship('Members', foreign_keys=user_id)

  
    def __init__(self, cep, country, state, city, district, user_id ):
        self.cep = cep
        self.country = country
        self.state = state
        self.city = city
        self.district = district
        self.user_id = user_id

    def __repr__(self):
        return  "User: %r" % self.name

class MembersDemography(db.Model):
    __tablename__ =  "members_demography"

    uuid = db.Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True )
    created_date = Column(DateTime(timezone=True), default=func.now())
    age_range = db.Column(db.String(14))
    gender = db.Column(db.String(255))
    number_of_people_at_home =  db.Column(db.String(255))
    is_pcd = db.Column(db.Boolean)
    work_or_study_tools =  db.Column(db.String(255))
    is_solo_mom = db.Column(db.Boolean)
    user_id = db.Column(postgresql.UUID(as_uuid=True), db.ForeignKey('members.uuid'))

    member = db.relationship('Members', foreign_keys=user_id)

  
    def __init__(self, age_range, gender, number_of_people_at_home, is_pcd, work_or_study_tools, is_solo_mom, user_id ):
        self.age_range = age_range
        self.gender = gender
        self.number_of_people_at_home = number_of_people_at_home
        self.is_pcd = is_pcd
        self.work_or_study_tools = work_or_study_tools
        self.is_solo_mom = is_solo_mom
        self.user_id = user_id

    def __repr__(self):
        return  "User: %r" % self.age_range


class MembersDegreeImportance(db.Model):
    __tablename__ =  "members_degree_importance"

    uuid = db.Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True )
    created_date = Column(DateTime(timezone=True), default=func.now())
    help_home_expenses = db.Column(db.Integer, unique=True)
    be_independent = db.Column(db.Integer)
    fund_studies =  db.Column(db.Integer)
    support_my_family = db.Column(db.Integer)
    acquire_experience =  db.Column(db.Integer)
    user_id = db.Column(postgresql.UUID(as_uuid=True), db.ForeignKey('members.uuid'))

    member = db.relationship('Members', foreign_keys=user_id)

  
    def __init__(self, help_home_expenses, be_independent, fund_studies, support_my_family, acquire_experience, user_id ):
        self.help_home_expenses = help_home_expenses
        self.be_independent = be_independent
        self.fund_studies = fund_studies
        self.support_my_family = support_my_family
        self.acquire_experience = acquire_experience
        self.user_id = user_id

    def __repr__(self):
        return  "User: %r" % self.user_id



class MemberScore(db.Model):
    __tablename__ =  "members_score"

    uuid = db.Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True )
    created_date = Column(DateTime(timezone=True), default=func.now())
    score = db.Column(db.String(14))
    user_id = db.Column(UUID(), db.ForeignKey('members.uuid'), unique=True)
    member = db.relationship('Members', foreign_keys=user_id)

  
    def __init__(self, score ):
        self.score = score

    def __repr__(self):
        return  "Score: %r" % self.score










########################  MEMBER PENDENCY ######################


class MembersPendency(db.Model):
    __tablename__ =  "members_pendency"

    uuid = db.Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True )
    created_date = Column(DateTime(timezone=True), default=func.now())
    article_link= db.Column(db.String(256))
    pendency = db.Column(db.Boolean)
    status_pendency = db.Column(db.String(10))
    current = db.Column(db.Boolean)
    user_id = db.Column(postgresql.UUID(as_uuid=True), db.ForeignKey('members.uuid'))

    member = db.relationship('Members', foreign_keys=user_id)

  
    def __init__(self, article_link, pendency,status_pendency ,user_id ):
        self.article_link = article_link
        self.pendency = pendency
        self.status_pendency =  status_pendency
        self.user_id = user_id

    def __repr__(self):
        return  "status: %r" % self.status_pendency



######################### PARTNER #######################################

class Partners(db.Model):
    __tablename__ =  "partners"

    uuid = db.Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True )
    created_date = Column(DateTime(timezone=True), default=func.now())
    partner_name= db.Column(db.String(256))
    partner_url_image = db.Column(db.String(256))
    partner_courses = db.Column(db.String(250))
  
    def __init__(self, partner_name, partner_url_image,partner_courses):
        self.partner_name = partner_name
        self.partner_url_image = partner_url_image
        self.partner_courses =  partner_courses

    def __repr__(self):
        return  "Parceiro: %r" % self.partner_name        


######################### Courses #######################################

class Courses(db.Model):
    __tablename__ =  "courses"

    uuid = db.Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True )
    created_date = Column(DateTime(timezone=True), default=func.now())
    course_name= db.Column(db.String(256))
    course_tags = db.Column(db.String(256))
    partner_uuid = db.Column(postgresql.UUID(as_uuid=True), db.ForeignKey('partners.uuid'))

    partner = db.relationship('Partners', foreign_keys=partner_uuid)

  
    def __init__(self, course_name, course_tags,partner_uuid):
        self.course_name = course_name
        self.course_tags = course_tags
        self.partner_uuid =  partner_uuid

    def __repr__(self):
        return  "Course: %r" % self.course_name  



######################### StudantShip #######################################

class Studentship(db.Model):
    __tablename__ =  "studentships"

    uuid = db.Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True )
    created_date = Column(DateTime(timezone=True), default=func.now())
    studentship_name = db.Column(db.String(100))
    studentship_cover = db.Column(db.String(256))
    studentship_link= db.Column(db.String(256))
    studentship_number_of_vacancies = db.Column(db.Integer)
    studentship_start_subscriptions = db.Column(db.DateTime)
    studentship_end_subscriptions = db.Column(db.DateTime)
    studentship_start_course = db.Column(db.DateTime)
    studentship_end_course = db.Column(db.DateTime)
    studentship_result_date = db.Column(db.DateTime)
    partner_uuid = db.Column(postgresql.UUID(as_uuid=True), db.ForeignKey('partners.uuid'))

    partner = db.relationship('Partners', foreign_keys=partner_uuid)

  
    def __init__(self,studentship_name, studentship_cover ,studentship_link, studentship_number_of_vacancies,studentship_start_subscriptions, studentship_end_subscriptions, studentship_start_course, studentship_end_course, studentship_result_date ,partner_uuid ):
        self.studentship_name = studentship_name
        self.studentship_cover = studentship_cover
        self.studentship_link = studentship_link
        self.studentship_number_of_vacancies = studentship_number_of_vacancies
        self.studentship_start_subscriptions =  studentship_start_subscriptions
        self.studentship_end_subscriptions = studentship_end_subscriptions
        self.studentship_start_course =  studentship_start_course
        self.studentship_end_course = studentship_end_course
        self.studentship_result_date =  studentship_result_date
        self.partner_uuid = partner_uuid

    def __repr__(self):
        return  "Studentship: %r" % self.studentship_name




@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None
