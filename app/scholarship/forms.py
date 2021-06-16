from flask_wtf import FlaskForm
from wtforms  import StringField, PasswordField, BooleanField
from wtforms.fields.core import DateField, IntegerField
from wtforms.validators import data_required
from wtforms.widgets import TextArea

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


class EditForm(FlaskForm):
    phone = StringField('phone', validators=[data_required()])
    cpf = StringField('cpf', validators=[data_required()]   )
    name = StringField('name', validators=[data_required()])
    email = StringField('email', validators=[data_required()])
    email_check = StringField('email_check')

class NewUserForm(FlaskForm):
    phone = StringField('phone', validators=[data_required()])
    cpf = StringField('cpf', validators=[data_required()])
    name = StringField('name', validators=[data_required()])
    email = StringField('email', validators=[data_required()])
    email_check = StringField('email_check')


class NewScholarship(FlaskForm):
    title = StringField('title', validators=[data_required()])
    description = StringField('description', validators=[data_required()], widget=TextArea())
    description_brief = StringField('description_brief', validators=[data_required()])
    thumbnail = StringField('thumbnail', validators=[data_required()])
    date_raffle = DateField('date_raffle', format='%m/%d/%Y', validators=[data_required()])
    date_course_start = DateField('date_course_start', format='%m/%d/%Y',validators=[data_required()])
    date_course_finish = DateField('date_course_finish',format='%m/%d/%Y', validators=[data_required()])
    number_of_vacancies = IntegerField('number_of_vacancies', validators=[data_required()])    


class EditFormPendency(FlaskForm):
    article_link = StringField('article_link', validators=[data_required()])
    delivered_the_article = StringField('delivered_the_article', validators=[data_required()]   )
