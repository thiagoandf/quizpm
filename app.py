# -*-coding: utf-8 -*-

from flask import Flask, g, redirect, url_for, request, flash
from flask.templating import render_template
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from werkzeug.security import check_password_hash

from database import db
from database import User

from forms import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lucas@lixo'

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/cadastro')
def cadastro():
    return 'oi'


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    if form.validate_on_submit():
        user_id = request.form['user_id']
        password = request.form['password']
        registered_user = User.query.filter_by(id=user_id).first()
        if registered_user is None:
            # flash('Username does not exist', 'error')
            return redirect(url_for('login'))
        elif not check_password_hash(registered_user.password, password):
            # flash('Invalid password', 'error')
            return redirect(url_for('login'))
        login_user(registered_user)
        flash('Logged in successfully')
        return redirect(url_for('home'))
    else:
        return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
