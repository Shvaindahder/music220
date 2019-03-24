from flask import render_template, redirect, url_for, flash, request
from app import db
from app.auth import bp
from app.auth.forms import RegistrationForm, LoginForm
from app.models import UserAccount


@bp.route('/registration')
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = UserAccount(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('auth/registration.html', title='Registration', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserAccount.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password! Try again')
            return redirect(url_for('auth.login'))
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', form=form)


@bp.route('/nav_login', methods=['GET', 'POST'])
def nav_login():
    user = UserAccount.query.filter_by(username=request.form['username']).first()
    if user is None or not user.check_password(request.form['password']):
        flash('Invalid username or password! Try again')
        return redirect(url_for('auth.login'))
    return redirect(url_for('main.index'))