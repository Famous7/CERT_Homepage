from app import app, login, models
from werkzeug.security import generate_password_hash
from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, login_required, current_user, logout_user
import dbHelper
from app.forms import SignInForm, SignUpForm, EditUserForm, ChangePasswordForm
from datetime import datetime


@login.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


@app.route('/')
def index():
    return render_template('index.html', posts=[])


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


@app.route('/user/<user_id>')
@login_required
def user(user_id):
    user = models.User.query.filter_by(user_id=user_id).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]

    return render_template('user.html', user=user, posts=posts)


@app.route('/edit_user', methods=['GET', 'POST'])
@login_required
def edit_user():
    form = EditUserForm()
    if form.validate_on_submit():
        current_user.user_about_me = form.user_about_me.data
        current_user.user_name = form.user_name.data
        current_user.user_email = form.user_email.data
        current_user.user_password = generate_password_hash(form.user_password.data)
        current_user.user_department = form.user_department.data
        current_user.user_grade = form.user_grade.data

        try:
            with dbHelper.get_session() as session:
                session.commit()

        except Exception as e:
            abort(500)

        flash('Your changes have been saved.')
        return redirect(url_for('user', user_id=current_user.user_id))

    form.user_id.data = current_user.user_id or ''
    form.user_email.data = current_user.user_email
    form.user_name.data = current_user.user_name
    form.user_about_me.data = current_user.user_about_me
    form.user_department.data = current_user.user_department
    form.user_grade.data = str(current_user.user_grade)

    return render_template('edit_user.html', form=form)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.set_user_pw(form.user_password_new.data)

        try:
            with dbHelper.get_session() as session:
                session.commit()

        except Exception as e:
            abort(500)

        flash('Your changes have been saved.')
        return redirect(url_for('user', user_id=current_user.user_id))

    return render_template('edit_password.html', form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.user_last_seen = datetime.utcnow()

        try:
            with dbHelper.get_session() as session:
                session.commit()

        except Exception as e:
            abort(500)
