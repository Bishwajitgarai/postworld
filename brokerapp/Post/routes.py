import os
from flask import Blueprint
posts=Blueprint('posts',__name__)

from flask_login import current_user,login_required
from flask import render_template,redirect,url_for,flash,request
from brokerapp.Post.forms import Post,PostUpdate
from brokerapp.models import CreatePost,PostImages,User
from brokerapp import db
from datetime import datetime
from brokerapp.Post.models import post_save_image
from sqlalchemy import and_

@posts.route("/createpost",methods=['GET','POST'])
# @login_required
def createpost():
    if  current_user.is_authenticated:
        form=Post()
        if form.validate_on_submit():

            post=CreatePost(post_title=form.post_title.data,post_details=form.post_details.data,userid=current_user.id,post_create_date=datetime.utcnow())
            db.session.add(post)
            db.session.commit()
            for picture in form.pictures.data:
                if picture:
                    pic=post_save_image(str(current_user.id),picture)
                    image=PostImages(userid=current_user.id,images_name=pic,postid=post.postid)
                    db.session.add(image)
                    db.session.commit()

            flash("Post Published Succesfully")
            return redirect(url_for('utilities.home'))
        return render_template('createpost.html',title="Add Post",form=form)
    else:
        flash(f"To Create post Please Register or Login !")
        return redirect(url_for('users.register'))



@posts.route("/searchpost",methods=["GET",'POST'])

def searchpost(page=1):
    postpage= "home"
    page=request.args.get("page",1,type=int)
    try:
        search_data= str(request.form['search-data'])
        postpage= str(request.form['postpage'])

    except:
        search_data=request.args.get("serach",type=str)
        postpage=request.args.get("postpage",type=str)

    if search_data!="" and current_user.is_authenticated:
        if postpage=="mypost":
            posts=CreatePost.query.filter(and_(CreatePost.userid==current_user.id,CreatePost.post_details.like(f"%{search_data}%"))).order_by(CreatePost.post_create_date.desc()).paginate(per_page=5,page=page)
        else:
            posts=CreatePost.query.filter(CreatePost.post_details.like(f"%{search_data}%")).order_by(CreatePost.post_create_date.desc()).paginate(per_page=5,page=page)
        for post in posts.items:
            post.post_views=post.post_views+1
            db.session.commit()
        # print(posts.pages)
        return render_template("search.html",title="Search post",posts=posts,User=User,Images=PostImages,search_data=search_data,postpage=postpage)
    elif postpage=="mypost":
        return redirect(url_for('posts.mypost'))
    elif current_user.is_authenticated:
        return redirect(url_for('utilities.home'))

    return render_template("home.html",title="Home PostWorld")



@posts.route("/deletepost/<int:postid>/<int:userid>/<int:page>",methods=['GET','POST'])
@login_required
def delete_post(postid,userid,page):
    if userid==current_user.id:
        post=CreatePost.query.filter_by(postid=postid,userid=current_user.id).first()
        images=PostImages.query.filter_by(postid=postid,userid=current_user.id).all()
        for image in images:
            img_remove=(str(os.getcwd())+"/brokerapp"+str(image.images_name))
            # print(img_remove)
            os.remove(img_remove)
            db.session.delete(image)
        db.session.commit()
        db.session.delete(post)
        db.session.commit()
        try:
            return redirect(url_for('utilities.home', page=page))
        except:
            page=page-1
            if page==0:
                page=1
            return redirect(url_for('utilities.home', page=page))
    else:
        flash("You have no rights to delete the post")
    return redirect(url_for('utilities.home', page=page))
@posts.route("/updatepost/<int:postid>/<int:userid>/<int:page>",methods=['GET','POST'])
@login_required
def update_post(postid,userid,page):
    form=PostUpdate()

    if userid==current_user.id:
        post=CreatePost.query.filter_by(postid=postid,userid=current_user.id).first()
        images=PostImages.query.filter_by(postid=postid,userid=current_user.id).all()
        if form.validate_on_submit():
            # post=CreatePost(postid=postid,post_details=form.post_details.data,post_title=form.post_title.data,userid=current_user.id)
            for picture in form.pictures.data:
                if picture:
                    pic=post_save_image(str(current_user.id),picture)
                    image=PostImages(userid=current_user.id,images_name=pic,postid=post.postid)
                    db.session.add(image)
                    db.session.commit()
            # db.session.add(post)
            post.post_details=form.post_details.data
            post.post_title=form.post_title.data
            db.session.commit()
            flash("Post Updated Succesfully")
            images=PostImages.query.filter_by(postid=postid,userid=current_user.id).all()
            return redirect(url_for('utilities.home',page=page))
        form.post_details.data=post.post_details
        form.post_title.data=post.post_title
        return render_template('updatepost.html',title="Edit Post",form=form,images=images,userid=userid,page=page)

    return redirect(url_for('utilities.home',page=page))




@posts.route("/deleteimage/<int:imageid>/<int:userid>/<int:page>",methods=['GET','POST'])
@login_required
def delete_image(imageid,userid,page):
    images=PostImages.query.filter_by(imageid=imageid,userid=current_user.id).first()

    if images is None:
        return redirect(url_for('utilities.home',page=page))
    if userid==current_user.id:
        postid=images.postid
        img_remove=(str(os.getcwd())+"/brokerapp"+str(images.images_name))
        os.remove(img_remove)
        db.session.delete(images)
        db.session.commit()
        return redirect(url_for('posts.update_post',postid=postid, page=page,userid=userid))

    return redirect(url_for('posts.update_post',postid=images.postid, page=page,userid=userid))
@posts.route("/mypost",methods=['GET','POST'])
@login_required
def mypost():
    page=request.args.get("page",1,type=int)
    if current_user.is_authenticated:
        posts=CreatePost.query.filter_by(userid=current_user.id).order_by(CreatePost.post_create_date.desc()).paginate(per_page=5,page=page)
        # print(posts)
        return render_template('myposts.html',title="My Posts",posts=posts,User=User,Images=PostImages)
    return render_template("home.html",title="Home PostWorld")
