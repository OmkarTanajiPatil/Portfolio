from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, URLField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, URL

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Send Message')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProjectForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired(), Length(min=2, max=200)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=2000)])
    tech_stack = StringField('Tech Stack', validators=[DataRequired(), Length(min=2, max=500)])
    github_url = URLField('GitHub URL', validators=[Optional(), URL()])
    live_url = URLField('Live URL', validators=[Optional(), URL()])
    image_url = URLField('Image URL', validators=[Optional(), URL()])
    is_completed = BooleanField('Is Completed')
    submit = SubmitField('Save Project')

class SettingsForm(FlaskForm):
    site_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    site_title = StringField('Professional Title', validators=[DataRequired(), Length(min=2, max=100)])
    about_intro = TextAreaField('About Introduction', validators=[DataRequired(), Length(min=10, max=500)])
    about_description = TextAreaField('About Description', validators=[DataRequired(), Length(min=10, max=1000)])
    technical_skills = TextAreaField('Technical Skills (comma-separated)', validators=[DataRequired()])
    contact_email = StringField('Contact Email', validators=[DataRequired(), Email()])
    contact_phone = StringField('Contact Phone', validators=[Optional()])
    social_github = URLField('GitHub URL', validators=[Optional(), URL()])
    social_linkedin = URLField('LinkedIn URL', validators=[Optional(), URL()])
    social_twitter = URLField('Twitter URL', validators=[Optional(), URL()])
    social_email = StringField('Contact Email Link', validators=[Optional(), Email()])
    submit = SubmitField('Save Settings')
