# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from flask import json
from flask.helpers import flash
from flask import jsonify
from flask.json import dump
from flask_mail import Message, Mail
from sqlalchemy import desc
from sqlalchemy.sql.expression import distinct
from sqlalchemy.sql.sqltypes import JSON
from wtforms import form
from wtforms.form import FormMeta
from app.members import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager, db, mail
from jinja2 import TemplateNotFound
from app.base.models import Members, MemberScore, MembersAdress, MembersDemography, MembersDegreeImportance, MembersPendency
from app.members.forms import BetterTagListField, IsBlackPeople, Member, MemberAdress, MemberDemography, MemberDegreeImportance, MemberPendency, TagListField
from validate_docbr import CPF

import babel
import random
import app.members


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


@blueprint.route('/members', defaults={'raffle_id': None}, methods=['POST', 'GET'])
@blueprint.route('/members/<int:raffle_id>/list', methods=['POST', 'GET'])
def all_winners(raffle_id):

    if request.method == "POST":
        print("Hello Word")
        return jsonify("ok")

    else:
        memberscore = MemberScore.query.all()
        print(memberscore)
        score = Members.query.join(
            MemberScore, Members.id == MemberScore.user_id).all()
        print(score)
        membersjson = []
        for member in score:
            membersjson.append("Member Name: " + str(member.name))
            print(membersjson)
        return jsonify(membersjson)


@blueprint.route('/newmember/oi', methods=['POST', 'GET'])
def newmember():
    NewMemberForm = Member()
    print(request.form)
    if request.method == "POST":
        user = Members.query.filter_by(cpf=request.form['cpf']).first()
        cpf = request.form['cpf']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        linkedin = request.form['linkedin']
        instagram = request.form['instagram']
        facebook = request.form['facebook']
        is_back_people = 0
        registration = Members(cpf, name, email, phone,
                               linkedin, instagram, facebook, is_back_people)
        cpf_valid = cpf_check.validate(request.form['cpf'])

        if cpf_valid:
            if user == None:
                db.session.add(registration)
                db.session.commit()
            else:
                print("Já registrado")
                # user = Members.query.filter_by(cpf=request.form['cpf']).first()
                # user.name = request.form['name']
                # user.cpf = request.form['cpf']
                # user.email = request.form['email']
                # user.phone = request.form['phone']
                # db.session.merge(user)
                # db.session.commit()
        else:
            print('Cpf Invalido')

    else:
        return render_template('newmember.html', form=NewMemberForm)


def newmember_step_2():
    return render_template('newmember-step2.html')


@blueprint.route('/newmember', methods=['POST', 'GET'])
def newmember_test():
    form = Member()
    r = ""
    try:
        if request.method == 'GET':
            return render_template('member_new-step1.html', form=form)

        if request.method == 'POST':
            user = Members.query.filter_by(cpf=form.cpf.data).first()
            cpf_valid = cpf_check.validate(str(form.cpf.data))
            if cpf_valid:
                if user != None and user.cpf == form.cpf.data:
                    is_back_people = Members.query.filter_by(
                        cpf=request.form['cpf']).filter(Members.is_back_people == 1).first()
                    if is_back_people == None:
                        flash(
                            "Usuario já existe em nossa base de dados, solicite a troca de senha.")
                        return redirect('/login')
                    else:
                        flash("Contate alguem da administação da Pretux")
                        return redirect('/index')
                else:
                    form = Member()
                    step2 = IsBlackPeople()
                    cpf = request.form['cpf']
                    name = request.form['name']
                    email = request.form['email']
                    phone = request.form['phone']
                    linkedin = request.form['linkedin']
                    instagram = request.form['instagram']
                    facebook = request.form['facebook']
                    is_black_people = 1
                    registration = Members(
                        cpf, name, email, phone, linkedin, instagram, facebook, is_black_people)
                    db.session.add(registration)
                    db.session.commit()
                    db.session.refresh(registration)
                    # return render_template('newmember-step2.html', form=step2, cpf=form.cpf.data)
                    return redirect(url_for('members_blueprint.newmember_steptwo', uuid=registration.uuid))

                    # return render_template('newmember-step2.html',form=step2, uuid=registration.uuid )

            else:
                flash("Cpf invalido")
    except Exception as e:
        print(e)


@blueprint.route('/newmember/step/2/<uuid>', methods=['POST', 'GET'])
def newmember_steptwo(uuid):
    try:
        if request.method == 'GET':
            form = IsBlackPeople()
            return render_template('member_new-step2.html', form=form)
        if request.method == 'POST':
            form = IsBlackPeople()
            user = Members.query.filter_by(uuid=uuid).first()
            blackpeople = request.form['blackpeople']
            print(blackpeople)
            if blackpeople == "1":
                return redirect(url_for('members_blueprint.newmember_stepthree', uuid=uuid))

            else:
                user.is_black_people = 0
                db.session.merge(user)
                db.session.commit()
            return render_template('member_new-step2.html', form=form)
    except Exception as e:
        print(e)


@blueprint.route('/newmember/step/3/<uuid>', methods=['POST', 'GET'])
def newmember_stepthree(uuid):
    try:
        if request.method == 'GET':
            formAdress = MemberAdress()
            formDemo = MemberDemography()
            return render_template('member_new-step3.html', formAdress=formAdress, formDemo=formDemo)
        if request.method == 'POST':
            formAdress = MemberAdress()
            formDemo = MemberDemography()
            user_id = uuid
            state = request.form['state']
            city = request.form['city']
            country = "Brasil"
            district = request.form['district']
            cep = request.form['cep']

            age_range = 0
            gender = 0
            number_of_people_at_home = 0
            work_or_study_tools = 0
            is_pcd = int(request.form['is_pcd'])
            is_solo_mom = int(request.form['is_solo_mom'])

            member_demography = MembersDemography(
                age_range, gender, number_of_people_at_home, work_or_study_tools, is_pcd, is_solo_mom, user_id)
            member_address = MembersAdress(
                cep, country, state, city, district, user_id)
            db.session.add(member_address)
            db.session.add(member_demography)
            db.session.commit()
            return redirect(url_for('members_blueprint.newmember_stepfour', uuid=uuid))
    except Exception as e:
        print(e)


@blueprint.route('/newmember/step/4/<uuid>', methods=['POST', 'GET'])
def newmember_stepfour(uuid):
    try:
        if request.method == 'GET':
            form = MemberDegreeImportance()
            return render_template('member_new-step4.html', formDemo=form)
        if request.method == 'POST':
            form = MemberDegreeImportance()
            help_home_expenses = request.form['help_home_expenses']
            be_independent = request.form['be_independent']
            fund_studies = request.form['fund_studies']
            support_my_family = request.form['support_my_family']
            acquire_experience = request.form['acquire_experience']

            member_importance = MemberDegreeImportance(
                help_home_expenses, be_independent, fund_studies, support_my_family, acquire_experience)

            db.session.add(member_importance)
            db.session.commit()
            return jsonify("Grau de importancia atualizado")
    except Exception as e:
        print(e)


@blueprint.route("/oi/step4", methods=['GET'])
def check_cep():
    editform = MemberDegreeImportance()
    return render_template('member_new-step3.html', formDemo=editform)


@blueprint.route("/oi/random3", methods=['get', 'post'])
def random3():
    print(request.form)
    lower = int(request.form['lowerlim'])
    upper = int(request.form['upperlim'])
    n = random.randint(lower, upper + 1)
    return render_template("random3.html", number=n)


@blueprint.route("/member/admin/profile/<uuid>", methods=['get', 'post'])
def member_admin_profile(uuid):
    members_pendency = Members.query\
        .join(MembersPendency, Members.uuid == MembersPendency.user_id)\
        .add_columns(Members.name, Members.email, Members.created_date, MembersPendency.status_pendency, MembersPendency.article_link)\
        .filter(Members.uuid == MembersPendency.user_id)\
        .filter(MembersPendency.status_pendency == "Aguardando")\
        .all()
    user = Members.query.filter_by(uuid=uuid).first()
    flash("All OK", 'success')
    return render_template("member-admin-profile.html", members_pendency=members_pendency, user=user)


@blueprint.route("/member/profile/<uuid>", methods=['get', 'post'])
def member_profile(uuid):
    try:
        if request.method == 'GET':

            form_pendency = MemberPendency()
            members_pendency = Members.query\
                .join(MembersPendency, Members.uuid == MembersPendency.user_id)\
                .add_columns(Members.name, Members.email, Members.created_date, MembersPendency.status_pendency, MembersPendency.article_link)\
                .filter(Members.uuid == uuid)\
                .filter(MembersPendency.current == True)\
                .all()
            user = Members.query.filter_by(uuid=uuid).first()

            return render_template("member-profile.html", members_pendency=members_pendency, user=user, form=form_pendency)
        if request.method == 'POST':
            pendency = MembersPendency.query.filter(
                MembersPendency.user_id == uuid).first()
            pendency.article_link = request.form["article_link"]
            pendency.status_pendency = 'Aguardando'
            db.session.merge(pendency)
            db.session.commit()
            flash("Solicitação enviada!", 'success') 
            return redirect(url_for('members_blueprint.member_profile', uuid=uuid))

    except Exception as e:
        print(e)


@blueprint.route("/members", methods=['get', 'post'])
def member_list():
    members = Members.query\
        .join(MembersPendency, Members.uuid == MembersPendency.user_id)\
        .add_columns(Members.name, Members.email, Members.created_date, MembersPendency.status_pendency)\
        .filter(Members.uuid == MembersPendency.user_id)\
        .filter(MembersPendency.current == True)\
        .all()
    flash("All OK")
    flash("All OK", 'success')
    flash("All Normal", 'info')
    flash("Not So OK", 'error')
    flash("So So", 'warning')
    return render_template("members.html", members=members)

# @blueprint.route("/test", methods=['get', 'post'])
# def test():
#     test = TagListField()
#     return render_template("teste.html", form=test)

