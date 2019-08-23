from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, RadioField, SelectField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
import re
from app.models import User

id_pattern = re.compile('^[a-zA-Z0-9_]{4,20}$')
password_pattern = re.compile('^[a-zA-Z0-9!@#$%^*+=-_]{8,}$')
password_combination_patterns = [re.compile('[a-z]'),
                                 re.compile('[A-Z]'),
                                 re.compile('[0-9]'),
                                 re.compile('[!@#$%^*+=-_]')]


def validate_password_by_kisa_rule(user_password):
    password = user_password.data
    if not password_pattern.match(password):
        raise ValidationError('Please use at least 8 characters using only allowed characters.')

    cnt = 0
    for pattern in password_combination_patterns:
        if pattern.findall(password):
            cnt += 1

    if cnt < 2:
        raise ValidationError('Please include at least two of the allowing character sets: ')

    if cnt == 2 and len(password) < 10:
        raise ValidationError('Please use a password of at least 10 characters in 2 combination.')

    if cnt >= 3 and len(password) < 8:
        raise ValidationError('Please use a password of at least 8 characters in 3 combination.')


class EditUserForm(FlaskForm):
    user_id = StringField('ID')
    user_name = StringField('Name')
    user_email = StringField('E-Mail')
    user_about_me = StringField('About Me', validators=[DataRequired()])
    user_password = PasswordField('Password', validators=[DataRequired()])
    user_repeat_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('user_password')])
    user_department = SelectField('Department', choices=[('COM', '컴퓨터공학과'), ('SWE', '소프트웨어학과'),
                                                         ('BIS', '경영학과'), ('MIS', '경영정보학과'), ('ETC', '기타')],
                                  validators=[DataRequired()])
    user_grade = SelectField('Grade', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', 'graduate')],
                             validators=[DataRequired()])

    def validate_user_password(self, user_password):
        validate_password_by_kisa_rule(user_password)


class SignInForm(FlaskForm):
    user_id = StringField('ID', validators=[DataRequired()])
    user_password = PasswordField('Password', validators=[DataRequired()])
    user_remember_me = BooleanField('Remember Me')


class SignUpForm(FlaskForm):
    user_id = StringField('ID', validators=[DataRequired()])
    user_password = PasswordField('Password', validators=[DataRequired()])
    user_repeat_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('user_password')])
    user_name = StringField('Name', validators=[DataRequired()])
    user_email = StringField('E-Mail', validators=[DataRequired(), Email()])
    user_gender = RadioField('Gender', choices=[('M', 'Men'), ('W', 'Women')], validators=[DataRequired()])
    user_department = SelectField('Department', choices=[('COM', '컴퓨터공학과'), ('SWE', '소프트웨어학과'),
                                                         ('BIS', '경영학과'), ('MIS', '경영정보학과'), ('ETC', '기타')],
                                  validators=[DataRequired()])
    user_grade = SelectField('Grade', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', 'graduate')],
                             validators=[DataRequired()])

    id_pattern = re.compile('^[a-zA-Z0-9_]{4,20}$')
    password_pattern = re.compile('^[a-zA-Z0-9!@#$%^*+=-_]{8,}$')
    password_combination_patterns = [re.compile('[a-z]'),
                                     re.compile('[A-Z]'),
                                     re.compile('[0-9]'),
                                     re.compile('[!@#$%^*+=-_]')]

    def validate_user_id(self, user_id):
        if not self.id_pattern.match(user_id.data):
            raise ValidationError('Please use a different user id.')

        user = User.query.filter_by(user_id=user_id.data).first()
        if user:
            raise ValidationError('Please use a different user id.')

    def validate_user_email(self, user_email):
        user = User.query.filter_by(user_email=user_email.data).first()
        if user:
            raise ValidationError('Please use a different email address.')

    # KISA password rule
    def validate_user_password(self, user_password):
       validate_password_by_kisa_rule(user_password)
