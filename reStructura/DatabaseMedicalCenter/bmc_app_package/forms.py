from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, DecimalField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange
from decimal import Decimal

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    role = SelectField('Role', choices=[
        ('business_owner', 'Business Owner'),
        ('investor', 'Investor'),
        ('admin', 'Administrator')
    ], validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class BusinessModelForm(FlaskForm):
    business_name = StringField('Business Name', validators=[DataRequired(), Length(min=2, max=255)])
    industry = StringField('Industry', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Create Business Model')

class ComponentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=255)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=1000)])
    amount = DecimalField('Amount', validators=[Optional(), NumberRange(min=0)], default=Decimal('0'))
    component_type = HiddenField('Component Type')
    submit = SubmitField('Add Component')
