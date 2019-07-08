from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SelectField,RadioField,SubmitField
from wtforms.validators import Required

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about yourself.',validators = [Required()])
    submit = SubmitField('Submit')

class BlogForm(FlaskForm):
    title = StringField('title', validators = [Required()])
    description = TextAreaField('description', validators = [Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[Required()])
    submit = SubmitField('Submit') 