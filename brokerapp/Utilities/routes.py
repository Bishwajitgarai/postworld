from flask import Blueprint,render_template,request,flash,url_for,redirect
from flask_login import current_user,login_required
from brokerapp.models import CreatePost,User,PostImages
from brokerapp import db
utilities=Blueprint("utilities",__name__)



@utilities.route("/",methods=["GET"])
def home():
    page=request.args.get("page",1,type=int)
    if current_user.is_authenticated:
        posts=CreatePost.query.order_by(CreatePost.post_create_date.desc()).paginate(per_page=5,page=page)
        for post in posts.items:
            post.post_views=post.post_views+1
            db.session.commit()
        return render_template("home.html",title="Home PostWorld",posts=posts,User=User,Images=PostImages)
    return render_template("home.html",title="Home PostWorld")
@utilities.route('/goto_page', methods=['POST'])
def goto_page():
    page= request.form['goto-page']
    last_page=request.form['last-page']
    try:
        page=int(page)
    except:
        page=int(last_page)
    last_page=int(last_page)
    if current_user.is_authenticated:
        try:
            posts=CreatePost.query.order_by(CreatePost.post_create_date.desc()).paginate(per_page=5,page=page)
            for post in posts.items:
                post.post_views=post.post_views+1
                db.session.commit()
            return render_template("home.html",title="Home PostWorld",posts=posts,User=User,Images=PostImages)
        except:
            page=last_page
            posts=CreatePost.query.order_by(CreatePost.post_create_date.desc()).paginate(per_page=5,page=page)
            for post in posts.items:
                post.post_views=post.post_views+1
                db.session.commit()
            return render_template("home.html",title="Home PostWorld",posts=posts,User=User,Images=PostImages)
    return render_template("home.html",title="Home PostWorld")

@utilities.route('/goto_page', methods=['POST'])

@utilities.route("/about")
def about():
    return render_template('about.html',title="About")

@utilities.route("/contact_us")
def contact_us():
    return render_template('contact_us.html',title="contact us")

@utilities.route("/Profile/<int:userid>")
def profile_view(userid):
    user_details=User.query.filter_by(id=userid).first()
    if user_details is not None:
        title=user_details.firstname+" "+user_details.lastname
    else:
        title="No User Found"
        flash("No user found.")
        return redirect(url_for('utilities.home'))
    # print(user_details.id)
    return render_template('profile.html',title=title,user_details=user_details)

