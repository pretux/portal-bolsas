from flask.helpers import flash
from sqlalchemy.orm.scoping import clslevel
from app.scholarship.forms import CPFValidator,EditForm, NewUserForm, NewScholarship
from app.scholarship.checkcpf import isCpfValid
from flask import  render_template, request, redirect,jsonify
from app import app, db
from app.base.models import UserRaffle, ListRaffle, Subscribed_Raffle, Winners_List
import babel, random

   


@app.route('/sorteios')
def sorteios():
  lista_sorteios = ListRaffle.query.all()

  return render_template('lista_sorteios_cards.html', titulo='Bolsas', raffles=lista_sorteios)

@app.route('/scholarship', methods=['POST', 'GET'])
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
    registration = ListRaffle(title, description,description_brief, thumbnail, date_raffle,date_course_start,date_course_finish, number_of_vacancies)
    print(registration)
    db.session.add(registration)
    db.session.commit()
    return redirect("/sorteios")
  return render_template('new_scholarship.html', titulo='Bolsas', form=form)


@app.route('/inscritos')
def inscritos():
  lista_inscritos = ListRaffle.query.order_by(ListRaffle.date_raffle).all()
  return render_template('realizar_sorteio.html', titulo='Inscritos' ,bolsas=lista_inscritos) 

@app.route('/raffle/',defaults={'raffle_id': None} )
@app.route('/raffle/<raffle_id>/sortear')
def raffle(raffle_id):

  lista_inscritos = UserRaffle.query.join(Subscribed_Raffle, UserRaffle.id==Subscribed_Raffle.user_id).filter(Subscribed_Raffle.raffle_id==raffle_id).order_by(UserRaffle.name).all()
  print(lista_inscritos)
  return render_template('lista_inscritos.html', titulo='Inscritos' ,bolsas=lista_inscritos, raffle_id= raffle_id) 

@app.route('/winners/',defaults={'raffle_id': None} )
@app.route('/winners/<raffle_id>/')
def winners(raffle_id):

  winners = UserRaffle.query.join(Winners_List, UserRaffle.id==Winners_List.user_id).filter(Winners_List.raffle_id==raffle_id).order_by(UserRaffle.name).all()
  print(winners)
  return render_template('winners.html', titulo='Ganhadores' ,winners=winners) 

@app.route('/allwinners/')
def all_winners():

  winners = UserRaffle.query.join(Winners_List, UserRaffle.id==Winners_List.user_id).filter().order_by(UserRaffle.name).all()
  print(winners)
  return render_template('all_winners.html', titulo='Ganhadores' ,winners=winners) 



@app.route('/inscrever-se/',defaults={'raffle_id': None} )
@app.route('/inscrever-se/<int:raffle_id>/bolsa', methods=['POST', 'GET'])
def novo(raffle_id):
    form = NewUserForm()
    r = ListRaffle.query.filter_by(id= raffle_id).first()
    if r != None :
        if r.id == raffle_id :
            return render_template('login.html', titulo= r.title, raffle_id=raffle_id, form=form)
        else:
          return redirect('/sorteios')  
    else:   
        return redirect('/sorteios')


@app.route('/criar', methods=['POST'])
def criar():
    name = request.form['nome']
    cpf = request.form['cpf']
    email = request.form['email']
    phone = request.form['phone']
    raffle_id = request.form["raffle_id"]
    registration = UserRaffle(cpf, name, email, phone)
    raffle_registration = Subscribed_Raffle()
    db.session.add(registration)
    db.session.commit()
    db.session.refresh(registration)
    if registration.id != None:
        user_id = registration.id
        raffle_registration = Subscribed_Raffle(user_id, raffle_id)
        db.session.add(raffle_registration)
        db.session.commit()
    return redirect('/')

@app.route("/login1",  methods=['POST', "GET"])
def login():
    form = NewUserForm()
    
    
    try:
      if request.method == 'POST':
        user = UserRaffle.query.filter_by(cpf = form.cpf.data).first()
        
        if  user != None and user.cpf == form.cpf.data :
            editform = EditForm(formdata=request.form, obj=user)
            return render_template('edit_user.html', form=editform)
        else:
            form = NewUserForm()
            form.cpf.data = form.cpf.data
            return render_template('new_user.html', form=form)
    
      return render_template('login.html', form=form)
    except Exception as e:
		   print(e)
    return render_template('login.html', form=form)


@app.route('/updateuser', methods=['POST'])
def user_update():
    user = UserRaffle.query.filter_by(cpf = request.form['cpf']).first()
    user.name = request.form['name']
    user.email = request.form['email']
    user.phone = request.form['phone']
    db.session.merge(user)
    db.session.commit()
    return redirect('/')

@app.route('/newuser', methods=['POST'])
def user_new():
    name = request.form['name']
    cpf = request.form['cpf']
    email = request.form['email']
    phone = request.form['phone']
    registration = UserRaffle(cpf, name, email, phone)
    db.session.add(registration)
    db.session.commit()
    return redirect('/')

@app.route('/doraffle/<raffle_id>', methods=['POST', 'GET'])
def do_raffle(raffle_id):
    users = []
    qtd =  ListRaffle.query.filter_by(id= raffle_id).first()
    if qtd.active:

      flash("Sorteio já realizado!")
      return redirect('/winners/' + raffle_id+ '/')
    else:
      lista_inscritos = UserRaffle.query.join(Subscribed_Raffle, UserRaffle.id==Subscribed_Raffle.user_id).filter(Subscribed_Raffle.raffle_id==raffle_id).order_by(UserRaffle.name).all()
      for user in lista_inscritos:
            users.append(user.id)
  
      winners = random.sample(users, qtd.number_of_vacancies)
      print(winners)
      for winner in winners:
        user_winner = Winners_List(winner, raffle_id, 0, ""  )
        db.session.add(user_winner)
        db.session.commit()
      qtd.active = 1 
      db.session.add(qtd)
      db.session.commit()

    return redirect('/winners/' + raffle_id+ '/')





@scholarship.template_filter('dt')
def format_datetime(value, format='medium'):
    if format == 'full':
        format="EEEE, d. MMMM y 'at' HH:mm"
    elif format == 'medium':
        format="dd/MM/y"
    return babel.dates.format_datetime(value, format)

    