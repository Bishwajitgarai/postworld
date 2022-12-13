from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,DateField,TextAreaField,MultipleFileField,SelectField
from wtforms.validators import DataRequired,Length
from flask_login import current_user
from brokerapp.models import User
from flask_wtf.file import FileField,FileAllowed



class Post(FlaskForm):
    post_title=SelectField("Select Category",choices=["Caption","People","Buisness","Animals","Plants","Scene","Material","Education","Others"])
    post_details=TextAreaField("Post Details",render_kw={"placeholder": "Post Description","style": "width: 98%; height: 120px"},validators=[DataRequired()])
    # post_views=IntegerField("Post Views",render_kw={"placeholder": "Post Views"})
    post_create_date=DateField("post_create_date")
    # post_update_date=DateField("post_update_date",validators=[DataRequired()])
    pictures=MultipleFileField("Upload Photos Here",validators=[FileAllowed(["jpg","jpeg","png","jfif"])])#,render_kw={"multiple":True}
    submit=SubmitField("Post")


class PostUpdate(FlaskForm):
    post_title=SelectField("Select Category",choices=["Caption","People","Buisness","Animals","Plants","Scene","Material","Education","Others"])
    post_details=TextAreaField("Post Details",render_kw={"placeholder": "Post Description","style": "width: 98%; height: 120px"},validators=[DataRequired()])
    # post_views=IntegerField("Post Views",render_kw={"placeholder": "Post Views"})
    # post_update_date=DateField("post_update_date")
    # post_update_date=DateField("post_update_date",validators=[DataRequired()])
    pictures=MultipleFileField("Upload Photos Here",validators=[FileAllowed(["jpg","jpeg","png","jfif"])])#,render_kw={"multiple":True}
    submit=SubmitField("Update Post")

