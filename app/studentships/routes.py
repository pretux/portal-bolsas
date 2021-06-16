# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from flask.helpers import flash
from flask import jsonify
from flask.json import dump
from flask_mail import Message, Mail
from wtforms import form
from wtforms.form import FormMeta
from app.studentships import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager, db, mail
from jinja2 import TemplateNotFound
from app.base.models import Members, MemberScore, MembersAdress, MembersDemography, MembersDegreeImportance, MembersPendency, Courses, Partners
from app.studentships.forms import Test, Partner






# @blueprint.route("/member/profile/<uuid>", methods=['get', 'post'])
# def member_profile(uuid):
#     try:
#         if request.method == 'GET':

#             form_pendency = MemberPendency()
#             members_pendency = Members.query\
#                 .join(MembersPendency, Members.uuid == MembersPendency.user_id)\
#                 .add_columns(Members.name, Members.email, Members.created_date, MembersPendency.status_pendency, MembersPendency.article_link)\
#                 .filter(Members.uuid == uuid)\
#                 .filter(MembersPendency.current == True)\
#                 .all()
#             user = Members.query.filter_by(uuid=uuid).first()

#             return render_template("member-profile.html", members_pendency=members_pendency, user=user, form=form_pendency)
#         if request.method == 'POST':
#             pendency = MembersPendency.query.filter(
#                 MembersPendency.user_id == uuid).first()
#             pendency.article_link = request.form["article_link"]
#             pendency.status_pendency = 'Aguardando'
#             db.session.merge(pendency)
#             db.session.commit()
#             flash("Solicitação enviada!", 'success') 
#             return redirect(url_for('members_blueprint.member_profile', uuid=uuid))

#     except Exception as e:
#         print(e)


# @blueprint.route('/studentships_new', methods=['POST', 'GET'])
# def studentship_new():
#     form = NewScholarship()
#     if request.method == 'POST':
#         title = request.form['title']
#         description = request.form['description']
#         description_brief = description[0:255]
#         thumbnail = request.form['thumbnail']
#         date_raffle = request.form['date_raffle']
#         date_course_start = request.form['date_course_start']
#         date_course_finish = request.form['date_course_finish']
#         number_of_vacancies = request.form['number_of_vacancies']
#         registration = ListRaffle(title, description, description_brief, thumbnail, date_raffle,
#                                   date_course_start, date_course_finish, number_of_vacancies, active=0)
#         db.session.add(registration)
#         db.session.commit()
#         return redirect("/studentship_new")
#     return render_template('studentship_new.html', titulo='Bolsas', form=form)


@blueprint.route('/studentships_new/<uuid>', methods=['POST', 'GET'])
def studentship_new(uuid):
    form = Partner()
    partners = Partners.query.all()
    #form.testeselect.query = Courses.query.filter(Courses.partner_uuid == uuid).all()
    if request.method == 'POST':
        flash("post")
        return render_template('studentships_new.html', titulo='Bolsas', form=form, partners=partners)
    return render_template('studentships_new.html', titulo='Bolsas', form=form, partners=partners)

@blueprint.route('/partners/<uuid>', methods=['POST', 'GET'])
def partners(uuid):
    form = Test()
    partners = Partners.query.all()
    form.testeselect.query = Courses.query.filter(Courses.partner_uuid == uuid).all()
    if request.method == 'POST':
        flash("post")
        return render_template('test.html', titulo='Bolsas', form=form, partners=partners)
    return render_template('test.html', titulo='Bolsas', form=form, partners=partners)

