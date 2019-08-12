from app import app, login, models
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
import dbHelper
from app.forms import SignInForm, SignUpForm


@login.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/protected')
@login_required
def protected():
    return 'Logged in as : ' + current_user.user_name


@app.route('/signOut')
def sign_out():
    logout_user()
    return redirect(url_for('index'))


@app.route('/signIn', methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = SignInForm(request.form)

    if form.validate_on_submit():
        user = models.User.query.filter_by(user_id=form.user_id.data).first()
        if not user or not user.check_user_pw(form.user_password.data):
            flash('Invalid User ID or Password.')
            return redirect(url_for('sign_in'))

        login_user(user, remember=form.user_remember_me.data)
        return redirect(url_for('index'))

    return render_template('signIn.html', form=form)


@app.route('/signUp', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm(request.form)

    if form.validate_on_submit():
        user = models.User(user_id=form.user_id.data, user_pw=form.user_password.data,
                           user_email=form.user_email.data, user_name=form.user_name.data,
                           user_department=form.user_department.data,
                           user_gender=form.user_gender.data, user_grade=form.user_grade.data)

        try:
            with dbHelper.get_session() as session:
                session.add(user)

        except Exception as e:
            return render_template('signUp.html', error=str(e))

        return redirect(url_for('index'))

    return render_template('signUp.html', form=form)
