from wtforms import validators
from app.base.models import Courses, Members, MembersPendency, User
from flask_wtf import FlaskForm
from flask_wtf.recaptcha.fields import RecaptchaField
from sqlalchemy.sql.schema import Column, Table
from wtforms  import StringField, PasswordField, BooleanField
from wtforms.fields.core import DateField, IntegerField, RadioField, SelectField
from wtforms.fields.simple import SubmitField, Field
from wtforms.validators import Email, EqualTo, InputRequired, ValidationError, data_required
from wtforms.widgets import TextArea, TextInput
from wtforms.ext.sqlalchemy.fields import QuerySelectField

class ListRaffle:
    def __init__(self, date, description, active, qtd ):
        self.date = date
        self.description = description
        self.active = active
        self.qtd = qtd

class UserRaffle:
    def __init__(self,  cpf, name, email, phone, raffle_id ):
        self.phone = phone
        self.cpf = cpf
        self.name = name
        self.email = email
        self.raffle_id = raffle_id


class CPFValidator(FlaskForm):
    cpf_user = StringField('cpf_user', validators=[data_required()])


class Member(FlaskForm):
    cpf = StringField('cpf', validators=[data_required(), InputRequired(message="Please your firstname.")]   )
    name = StringField('name', validators=[data_required()])
    email = StringField('email', validators=[data_required()])
    phone = StringField('phone', validators=[data_required()])
    linkedin = StringField('linkedin', validators=[data_required()])
    instagram = StringField('instagram', validators=[data_required()])
    facebook = StringField('facebook', validators=[data_required()])
    is_back_people = StringField('is_back_people', validators=[data_required()])

    def validate_email(self, email):
        user = Members.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email já está sendo utilizado!')

    def validate_cpf(self, cpf):
        user = Members.query.filter_by(cpf=cpf.data).first()
        if user is not None:
            raise ValidationError('Cpf já está em uso, por favor realize a troca de senha.')
        return  print("olacpf")
    def validate_linkedin(self, linkedin):
        user = Members.query.filter_by(linkedin=linkedin.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')   
    def validate_phone(self, phone):
        user = Members.query.filter_by(phone=phone.data).first()
        if user is not None:
            raise ValidationError('Celular já está em uso.')
class IsBlackPeople(FlaskForm):
   blackpeople = RadioField('blackpeople', validators=[data_required()], choices=[(1 ,'Sim'), (0, 'Não')])

class MembersScore(FlaskForm):
    score = StringField('score', validators=[data_required()])

class MemberAdress(FlaskForm):
    cep = StringField('cep', validators=[data_required()])
    country = StringField('country', validators=[data_required()])
    state = StringField('state', validators=[data_required()])
    city = StringField('city', validators=[data_required()])
    district = StringField('district', validators=[data_required()])



class MemberDemography(FlaskForm):
    age_range =  SelectField(u'age_range', choices=[(1, '17 anos ou menos'), (2, '18-20 anos'), (3, '21-29 anos'), (4, '30-39 anos'), (5, '40-49 anos'), (6, '50-59 anos'), (7, '60 anos ou mais')])
    gender = SelectField(u'gender', choices=[(1, 'Homem Cisgênero'), (2, 'Mulher Cisgênero'), (3, 'Homem Transgênero'), (4, 'Mulher Transgênero'), (5, 'Homem Transexual'), (6, 'Mulher Transexual'), (7, 'Não sei responder'), (8, 'Prefiro não responder')])
    number_of_people_at_home = IntegerField('number_of_people_at_home', validators=[data_required()])
    is_pcd = RadioField('is_pcd', validators=[data_required()], choices=[(1 ,'Sim'), (0, 'Não')])
    work_or_study_tools = SelectField(u'work_or_study_tools', choices=[(1, 'Possuo computador próprio, celular, internet e espaço reservado na casa'), (2, 'Possuo computador próprio, celular, internet'), (3, 'Não Possuo computador próprio, porém, possuo celular e internet.'), (4, 'Preciso de terceiros para ter acesso'), (5, 'Preciso compartilhar as ferramentas')])
    is_solo_mom = RadioField('is_solo_mom', validators=[data_required()], choices=[(1 ,'Sim'), (0, 'Não')])


class MemberDegreeImportance(FlaskForm):
    help_home_expenses =  RadioField('help_home_expenses', choices=[(0, '0'),(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    be_independent = RadioField('be_independent', choices=[(0, '0'),(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    fund_studies = RadioField('fund_studies', choices=[(0, '0'),(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    support_my_family = RadioField('support_my_family', choices=[(0, '0'),(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    acquire_experience = RadioField('acquire_experience ', choices=[(0, '0'),(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])

class MemberPendency(FlaskForm):
    article_link = StringField('article_link', validators=[data_required()])

class Partner(FlaskForm):
    partner_name =  StringField('partner_name', validators=[data_required()])
    partner_url_image = StringField('partner_url_image', validators=[data_required()])

def courses_query():
    return Courses.query
class Test(FlaskForm):
    testeselect = category = QuerySelectField(query_factory=courses_query,allow_blank=False, get_label='course_name')




class TagListField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
        else:
            self.data = []

class BetterTagListField(TagListField):
    def __init__(self, label='', validators=None, remove_duplicates=True, **kwargs):
        super(BetterTagListField, self).__init__(label, validators, **kwargs)
        self.remove_duplicates = remove_duplicates

    def process_formdata(self, valuelist):
        super(BetterTagListField, self).process_formdata(valuelist)
        if self.remove_duplicates:
            self.data = list(self._remove_duplicates(self.data))

    @classmethod
    def _remove_duplicates(cls, seq):
        """Remove duplicates in a case insensitive, but case preserving manner"""
        d = {}
        for item in seq:
            if item.lower() not in d:
                d[item.lower()] = True
                yield item
