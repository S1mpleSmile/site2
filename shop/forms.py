from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from shop.models import User


class RegistrationForm(FlaskForm):
    def validate_username(self, check_username):
        user = User.query.filter_by(username=check_username.data).first()
        if user:
            raise ValidationError('A user with this name is already registered. Please enter another name.')

    def validate_email(self, check_email):
        email = User.query.filter_by(email=check_email.data).first()
        if email:
            raise ValidationError('A user with such an email is already registered. \
                                   Please enter a different email address.')

    username = StringField(label="User Name", validators=[Length(min=3, max=25), DataRequired()])
    email = StringField(label="Email", validators=[Email(), DataRequired()])
    password = PasswordField(label="Password", validators=[Length(min=8), DataRequired()])
    confirm_password = PasswordField(label="Confirm the Password", validators=[EqualTo('password'), DataRequired()])
    btn_registration = SubmitField(label='Complete Registration')


class LoginForm(FlaskForm):
    username = StringField(label="User Name", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    btn_login = SubmitField(label='Log in')


class BuyForm(FlaskForm):
    btn_buy = SubmitField(label='Buy Product')


class SellForm(FlaskForm):
    btn_sell = SubmitField(label='Sell Product')


class EditForm(FlaskForm):
    username = StringField(label="User Name", validators=[Length(min=3, max=25), DataRequired()])
    email = StringField(label="Email", validators=[Email(), DataRequired()])
    btn_change = SubmitField('Сhange')

    def validate_username(self, check_username):
        user = User.query.filter_by(username=check_username.data).first()
        if user:
            raise ValidationError('A user with this name is already registered. Please enter another name.')

    def validate_email(self, check_email):
        email = User.query.filter_by(email=check_email.data).first()
        if email:
            raise ValidationError('A user with such an email is already registered. \
                                   Please enter a different email address.')
