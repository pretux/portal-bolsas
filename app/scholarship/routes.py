# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from flask.helpers import flash
from flask import jsonify
from flask_mail import Message, Mail
from sqlalchemy import desc
from sqlalchemy.sql.sqltypes import JSON
from wtforms.form import FormMeta
from app.scholarship import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager, db, mail
from jinja2 import TemplateNotFound
from app.base.models import UserRaffle, ListRaffle, Subscribed_Raffle, Winners_List
from app.scholarship.forms import NewScholarship, NewUserForm, EditForm, EditFormPendency
from validate_docbr import CPF

import babel
import random
import app.scholarship


cpf_check = CPF()


@blueprint.route('/index2')
@login_required
def index2():

    return render_template('index.html', segment='index')


@blueprint.route('/<template>')
@login_required
def route_template2(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template(template, segment=segment)

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except:
        return render_template('page-500.html'), 500

# Helper - Extract current page name from request


def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None


@blueprint.route('/scholarship_list')
def sorteios():
    lista_sorteios = ListRaffle.query.order_by(ListRaffle.active).all()
    print(lista_sorteios)
    return render_template('scholarship_all.html', titulo='Bolsas', raffles=lista_sorteios)


@blueprint.route('/scholarship', methods=['POST', 'GET'])
def scholarship():
    form = NewScholarship()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        description_brief = description[0:255]
        thumbnail = request.form['thumbnail']
        date_raffle = request.form['date_raffle']
        date_course_start = request.form['date_course_start']
        date_course_finish = request.form['date_course_finish']
        number_of_vacancies = request.form['number_of_vacancies']
        registration = ListRaffle(title, description, description_brief, thumbnail, date_raffle,
                                  date_course_start, date_course_finish, number_of_vacancies, active=0)
        db.session.add(registration)
        db.session.commit()
        return redirect("/scholarship_list")
    return render_template('scholarship_new.html', titulo='Bolsas', form=form)


@blueprint.route('/manage_raffle')
def manage_raffle():
    lista_sorteios = ListRaffle.query.order_by(ListRaffle.active).all()
    return render_template('manager_raffle.html', titulo='Bolsas', raffles=lista_sorteios)


@blueprint.route('/allwinners', defaults={'raffle_id': None}, methods=['POST', 'GET'])
@blueprint.route('/allwinners/<int:raffle_id>/list', methods=['POST', 'GET'])
def all_winners(raffle_id):

    if request.method == "POST":
        print("Hello Word")
        return jsonify("ok")

    else:

        if raffle_id == None:
            form = EditFormPendency()
            winners = UserRaffle.query.join(
                Winners_List, UserRaffle.id == Winners_List.user_id).filter().order_by(UserRaffle.name).all()
            return render_template('winners_all.html', titulo='Ganhadores', winners=winners,  form=form, raffle_id=None)
        else:
            form = EditFormPendency()
            winnersraffle = UserRaffle.query.join(Winners_List, UserRaffle.id == Winners_List.user_id).filter(
                Winners_List.raffle_id == raffle_id).order_by(UserRaffle.name).all()
            print(winnersraffle)
            return render_template('winners_all.html', titulo='Ganhadores', winners=winnersraffle, form=form, raffle_id=raffle_id)


@blueprint.route('/subscribers_list', defaults={'raffle_id': None}, methods=['POST', 'GET'])
@blueprint.route('/subscribers_list/<int:raffle_id>/list', methods=['POST', 'GET'])
def subscribers_list(raffle_id):

    if raffle_id == None:
        form = EditFormPendency()
        winners = UserRaffle.query.join(
            Winners_List, UserRaffle.id == Winners_List.user_id).filter().order_by(UserRaffle.name).all()
        return render_template('winners_all.html', titulo='Ganhadores', winners=winners,  form=form)
    else:
        form = EditFormPendency()
        subscriberraffle = UserRaffle.query.join(Subscribed_Raffle, UserRaffle.id == Subscribed_Raffle.user_id).filter(
            Subscribed_Raffle.raffle_id == raffle_id).order_by(UserRaffle.name).all()
        return render_template('scholarship_subscriber_list.html', titulo='Inscritos', subscribers=subscriberraffle, form=form)


@blueprint.route('/signup_scholarship/', defaults={'raffle_id': None})
@blueprint.route('/signup_scholarship/<int:raffle_id>', methods=['POST', 'GET'])
def signup_scholarship(raffle_id):
    form = NewUserForm()
    r = ListRaffle.query.filter_by(id=raffle_id).first()
    try:
        if request.method == 'GET':
            if r != None:
                if r.id == raffle_id:
                    return render_template('scholarship_subscriber_check_cpf.html', raffle_id=raffle_id, form=form)
                else:
                    return redirect('/scholarship_list')

        if request.method == 'POST':
            user = UserRaffle.query.filter_by(cpf=form.cpf.data).first()
            cpf_valid = cpf_check.validate(str(form.cpf.data))
            if cpf_valid:
                if user != None and user.cpf == form.cpf.data:
                    pendente = UserRaffle.query.join(Winners_List, UserRaffle.id == Winners_List.user_id).filter(
                        Winners_List.delivered_the_article == 1).filter(UserRaffle.cpf == form.cpf.data).first()
                    if pendente == None:
                        return email_verify_if_user_exists(user.email, user.cpf, raffle_id=raffle_id)
                    else:
                        flash(
                            "Usuario tem artigo pendente, contate alguem da administação da Pretux")

                else:
                    form = NewUserForm()
                    return render_template('scholarship_subscriber.html', form=form, raffle_id=raffle_id)
                   # return render_template('scholarship_subscriber.html', form=form, cpf=form.cpf.data
            else:
                flash("Cpf invalido")
    except Exception as e:
        print(e)
    return render_template('scholarship_subscriber_check_cpf.html', form=form, raffle_id=raffle_id)


@blueprint.route('/scholarship_subscriber_create', methods=['POST'])
def scholarship_subscriber_create():
    user = UserRaffle.query.filter_by(cpf=request.form['cpf']).first()

    name = request.form['name']
    cpf = request.form['cpf']
    email = request.form['email']
    phone = request.form['phone']
    raffle_id = request.form["raffle_id"]
    registration = UserRaffle(cpf, name, email, phone)
    cpf_valid = cpf_check.validate(request.form['cpf'])
    if cpf_valid:
        if user == None:
            db.session.add(registration)
            db.session.commit()
            db.session.refresh(registration)
            raffle_registration = Subscribed_Raffle(registration.id, raffle_id)
            db.session.add(raffle_registration)
            db.session.commit()
        else:
            user = UserRaffle.query.filter_by(cpf=request.form['cpf']).first()
            user.name = request.form['name']
            user.cpf = request.form['cpf']
            user.email = request.form['email']
            user.phone = request.form['phone']
            db.session.merge(user)
            db.session.commit()
            raffle_registration = Subscribed_Raffle(user.id, raffle_id)
            db.session.add(raffle_registration)
            db.session.commit()
    else:
        flash('Cpf Invalido')
    return redirect('/')


@blueprint.route('/email_verify', methods=["POST"])
def email_verify():
    otp = secrets.token_hex(4)
    email = request.form["email"]
    msg = Message('Código de Verificação PRETUX: ',
                  sender='rehzende@hotmail.com', recipients=[email])
    msg.body = str(otp)
    mail.send(msg)
    return render_template('scholarship_subscriber_valide_email.html')


def email_verify_if_user_exists(email, cpf, raffle_id):
    form = EditForm()
    email = email
    msg = Message('OTP', sender='rehzende@hotmail.com', recipients=[email])
    msg.body = str("OIOIOI")
    mail.send(msg)
    return render_template('scholarship_subscriber_valide_email.html', form=form, cpf=cpf, raffle_id=raffle_id)


@blueprint.route('/email_validate', methods=["POST"])
def email_validate():
    print(request.form)
    user_otp = request.form['email_check']
    if "OIOIOI" == user_otp:
        return editUser(request.form['cpf'], request.form['raffle_id'])
    return "<h3>failure, OTP does not match</h3>"


def editUser(cpf, raffle_id):
    editform = EditForm()
    user = UserRaffle.query.filter_by(cpf=cpf).first()
    editform = EditForm(formdata=request.form, obj=user)
    return render_template('scholarship_subscriber.html', form=editform, raffle_id=raffle_id, cpf=cpf, obj=user)


@blueprint.route('/doraffle/<raffle_id>', methods=['POST', 'GET'])
def do_raffle(raffle_id):
    users = []
    qtd = ListRaffle.query.filter_by(id=raffle_id).first()
    if qtd.active:

        flash("Sorteio já realizado!")
        return redirect('/allwinners/' + raffle_id + '/list')
    else:
        lista_inscritos = UserRaffle.query.join(Subscribed_Raffle, UserRaffle.id == Subscribed_Raffle.user_id).filter(
            Subscribed_Raffle.raffle_id == raffle_id).order_by(UserRaffle.name).all()
        for user in lista_inscritos:
            users.append(user.id)
        print("Quantidade de usuarios")
        quantidade_inscritos = len(users)
        quantidade_vagas = qtd.number_of_vacancies
        if quantidade_inscritos < 1:
            flash("Não há quantidade de inscritos o suficiente para o sorteio!")
        else:
            if quantidade_inscritos < quantidade_vagas:
                quantidade_vagas = quantidade_inscritos

        winners = random.sample(users, quantidade_vagas)

        for winner in winners:
            user_winner = Winners_List(winner, raffle_id, 0, "")
            db.session.add(user_winner)
            db.session.commit()
        qtd.active = 1
        db.session.add(qtd)
        db.session.commit()

    return redirect('/allwinners/' + raffle_id + '/list')


@blueprint.route('/send_email_winners/<raffle_id>', methods=['POST', 'GET'])
def send_email_winners(raffle_id):
    
    if request.method == 'POST':
        winners = UserRaffle.query.join(Winners_List, UserRaffle.id == Winners_List.user_id).filter(Winners_List.raffle_id == raffle_id).all()
        print(winners)
        for winner in winners:
            email = winner.email
            msg = Message('PRETUX Comunidade - Bolsa! ',
                        sender='rehzende@hotmail.com', recipients=[email])
            msg.body = str("Parabens")
            mail.send(msg)
        return redirect('/allwinners/' + raffle_id + '/list')
    return redirect('/allwinners/' + raffle_id + '/list')
    


@blueprint.route('/mofify_winner/<raffle_id>', methods=['POST', 'GET'])
def mofify_winner(user_id):
    editform = EditForm()
    user = Winners_List.query.filter_by(user_id=user_id).first()
    editform = EditForm(formdata=request.form, obj=user)
    return render_template('scholarship_subscriber.html', form=editform, user_id=user_id, obj=user)


@blueprint.route('/teste', methods=['POST', 'GET'])
def teste():

    if request.method == "POST":
        print("Hello Word")
        return jsonify({"teste": "ok"})
