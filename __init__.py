import os
from flask import Flask, session, render_template, request, redirect, url_for
from sqlalchemy import Column, Integer, String, DateTime, CHAR, ForeignKey
from app.security import hash_password, check_password, generate_token, validate_token
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{os.getenv("USER")}:{os.getenv("PASSWORD")}@{os.getenv("HOST")}:{os.getenv("PORT")}/{os.getenv("DB")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'
db = SQLAlchemy(app)


class EventDB(db.Model):
    __tablename__ = "evento"
    id = Column("id", Integer, primary_key=True)
    nombre = Column("nombre", String(20), nullable=False)
    fecha = Column("fecha", DateTime, nullable=False, unique=True)
    lugar = Column("lugar", String(50), nullable=False)
    modalidad = Column("modalidad", CHAR(2), nullable=False)
    user_id = Column("user_id", Integer, ForeignKey("usuario.id"))

    def __init__(self, nombre, fecha, lugar, modalidad, user_id):
        self.nombre = nombre
        self.fecha = fecha
        self.lugar = lugar
        self.modalidad = modalidad
        self.user_id = user_id


class UserDB(db.Model):

    __tablename__ = "usuario"
    id = Column("id", db.Integer, primary_key=True, autoincrement=True)
    nombre = Column("nombre", db.String(255), nullable=False)
    email = Column("email", db.String(255), nullable=False, unique=True)
    contrasena = Column("contrasena", db.String(255), nullable=False)

    def __init__(self, nombre, email, contrasena):
        self.nombre = nombre
        self.email = email
        self.contrasena = contrasena


def save_events(events):
    for event in events:
        event = EventDB(nombre=event.nombre, fecha=event.fecha,
                        lugar=event.lugar, modalidad=event.modalidad, user_id=event.user_id)
        db.session.add(event)
        db.session.commit()


def get_events(user_id):
    events = EventDB.query.filter_by(user_id=user_id).order_by(EventDB.fecha.desc()).all()
    return events


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

notification = False


@app.route('/',  methods=['GET'])
def index():
    token = session.get('token_log')
    if request.method == 'GET':
        if not validate_token(token):
            return redirect(url_for('login'))
        email = validate_token(token).get('email')
        user_id = UserDB.query.filter_by(email=email).first().id
        events = get_events(user_id)
        notf = False
        global notification
        if notification is True:
            notf = notification
        if events:
            return render_template('events.html', events=events, notification=notf, message='Evento creado exitosamente')
        else:
            return render_template('blank.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_email = request.form['email']
        found_user = UserDB.query.filter_by(email=user_email).first()
        if found_user:
            return render_template('register.html', message = 'Usuario ya registrado')
        nombre, email, contrasena = request.form['nombre'], request.form['email'], request.form['contrasena']
        hash_pswd = hash_password(contrasena)
        user = UserDB(
            nombre=nombre, email=email, contrasena=hash_pswd)
        db.session.add(user)
        db.session.commit()
        return render_template('register.html', message = 'Registro exitoso')
    elif request.method == 'GET':
        token = session.get('token_log')
        if type(token) is not bool:
            vt = validate_token(token)
            if type(vt) is not bool:
                return redirect(url_for('index'))
        return render_template('register.html', message = 'Ingresa tus datos')
    


@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    token = session.get('token_log')
    global notification
    notification = False

    if request.method == 'POST':

        if type(validate_token(token)) is not bool:
            event_already_exists = EventDB.query.all()
            email = validate_token(token).get('email')
            nombre, fecha, lugar, modalidad = request.form['nombre'], request.form[
                'fecha'], request.form['lugar'], request.form['modalidad']
            user_id = UserDB.query.filter_by(email=email).first().id
            event = EventDB(nombre=nombre, fecha=fecha, lugar=lugar,
                            modalidad=modalidad, user_id=user_id)
            db.session.add(event)
            db.session.commit()
            notification = True
            return redirect(url_for('index'))
    return render_template('create_event.html', mensaje='Ingresa los datos del evento', event=None)


@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    token = session.get('token_log')
    vt = validate_token(token)
    if type(vt) is not bool:
        email = vt.get('email')
        user_id = UserDB.query.filter_by(email=email).first().id
        events = get_events(user_id)
        event = events[event_id]
        if request.method == 'POST':
            event.nombre = request.form['nombre']
            event.fecha = request.form['fecha']
            event.lugar = request.form['lugar']
            event.modalidad = request.form['modalidad']
            db.session.delete(event)
            db.session.add(event)
            db.session.commit()
            global notification
            notification = True
            return render_template('events.html', events=events, notification=notification, message='Evento modificado exitosamente')
        return render_template('edit_event.html', event=event, event_id=event_id)
    return redirect(url_for('index'))


@app.route('/delete_event/<int:event_id>')
def delete_event(event_id):

    token = session.get('token_log')
    if type(token) is not bool:
        vt = validate_token(token)
        if type(vt) is not bool:
            email = vt.get('email')
            user_id = UserDB.query.filter_by(email=email).first().id
            events = get_events(user_id)
            if events:
                event = events[event_id]
                events.remove(event)
                db.session.delete(event)
                db.session.commit()
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('token_log', None)
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = request.form['email']
        password = request.form['contrasena']
        usuario_bd = UserDB.query.filter_by(email=user_email).first()
        if not usuario_bd:
            return redirect(url_for('login'))
        hash_pswd = usuario_bd.contrasena.encode('utf-8')
        if check_password(password, hash_pswd):
            global token_log
            token = generate_token(usuario_bd.nombre, usuario_bd.email)
            session['token_log'] = token
        return redirect(url_for('index'))
    elif request.method == 'GET':
        token = session.get('token_log')
        if type(token) is not bool:
            vt = validate_token(token)
            if type(vt) is not bool:
                return redirect(url_for('index'))
        return render_template('login.html')
