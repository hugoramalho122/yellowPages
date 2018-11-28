from flask import Flask, flash, render_template, url_for, redirect, session,request
from wtforms import StringField, Form, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from pprint import pprint


app = Flask(__name__)

#Secret key
app.secret_key = 'yellowpages'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@mysql:3306/YellowPages'
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#DB Models

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

class Business(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    telefone = db.Column(db.String(9), unique=True)
    morada = db.Column(db.String(100))
    cod = db.Column(db.String(12))
    freguesia=db.Column(db.String(20))


@app.route('/', methods=['GET', 'POST'])
def home():
    locations = Business.query.with_entities(Business.freguesia).distinct()

    page = request.args.get('page', 1, type=int)

    if request.method == 'POST':
        search = request.form['search']
        select = request.form['select']

        response = tmp(int(page), search, select)

        return render_template('search.html', locations=locations, business=response["business"], next_url=response["next_url"],
                               prev_url=response["prev_url"], search=request.form['search'], select=request.form['select'])

    elif request.method == 'GET' and request.args.get('page') is not None and request.args.get('search') is not None and request.args.get('select') is not None:

        response = tmp(
            page=int(request.args.get('page')),
            search=request.args.get('search'),
            select=request.args.get('select')
        )

        return render_template('search.html', locations=locations, business=response["business"],
                               next_url=response["next_url"],
                               prev_url=response["prev_url"], search=request.args.get('search'), select=request.args.get('select'))

    return render_template('search.html', locations=locations, business=None)


def tmp(page, search, select):
    business = Business.query.filter_by(nome=search, freguesia=select).paginate(per_page=2, page=page, error_out=True)
    if business.has_next:
        next_url = url_for('home', page=business.next_num, search=search, select=select)

    else:
        next_url = 'invalid'

    if business.has_prev:
        prev_url = url_for('home', page=business.prev_num, search=search, select=select)

    else:
        prev_url = 'invalid'

    return {
        "business": business,
        "next_url": next_url,
        "prev_url": prev_url

    }

@app.route('/admin', methods=['GET'])
def admin():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        user = Users.query.filter_by(username=request.form['username']).first()

        if user:
            if sha256_crypt.verify(request.form['password'], user.password):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                error = 'Credeciais Invalidas'
                return render_template('login.html', error=error)

        else:
            error = 'Utilizador Invalido'
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():

        new_user = Users(username=form.username.data, email=form.email.data, password=sha256_crypt.encrypt(str(form.password.data)))
        db.session.add(new_user)
        db.session.commit()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    page = request.args.get('page', 1, type=int)

    business = Business.query.paginate(per_page=3, page=page, error_out=True)

    if business.has_next:
        next_url = url_for('dashboard', page=business.next_num)

    else:
        next_url = 'invalid'

    if business.has_prev:
        prev_url = url_for('dashboard', page=business.prev_num)

    else:
        prev_url = 'invalid'

    form = BusinessForm(request.form)
    if request.method == 'POST' and form.validate():

        new_business = Business(nome=form.nome.data, telefone=form.telefone.data, morada=form.morada.data,cod=form.cod.data, freguesia=form.freguesia.data)
        db.session.add(new_business)
        db.session.commit()

        flash('Empresa adiciona com Sucesso ', 'success')
        return redirect(url_for('dashboard', page=1))

    return render_template('dashboard.html', form=form, business=business, next_url=next_url, prev_url=prev_url)



@app.route('/business', methods=['GET'])
def simgleItem():

    itemid = request.args.get('id', 1, type=int)
    business = Business.query.filter_by(id=itemid).first()



    return render_template('singleitem.html',business=business)













@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/delete')
@login_required
def delete():

    delete_id = request.args.get('delete', 1, type=int)
    Business.query.filter_by(id=delete_id).delete()
    db.session.commit()

    return redirect(url_for('dashboard'))


@app.route('/edit')
@login_required
def edit():

    edit_id = request.args.get('edit_id', 1, type=int)

    business = Business.query.filter_by(id=edit_id).first()

    business.nome = request.args.get('name', 2, type=str)
    business.morada = request.args.get('address', 3, type=str)
    business.cod = request.args.get('cod', 4, type=str)
    business.freguesia = request.args.get('city', 5, type=str)
    business.telefone = request.args.get('phone', 6, type=str)

    db.session.commit()

    return redirect(url_for('dashboard'))

#Form Models

class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


class BusinessForm(Form):
    nome=StringField('Nome', [validators.Length(min=4, max=50)])
    telefone = StringField('Telefone', [validators.Length(min=9, max=9)])
    morada = StringField('Morada', [validators.Length(min=4, max=100)])
    cod = StringField('Codigo Postal', [validators.Length(min=5, max=12)])
    freguesia =StringField('Freguesia', [validators.Length(min=1, max=20)])


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', debug=True)
