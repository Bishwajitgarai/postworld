from flask import Blueprint,render_template,request,flash,url_for,redirect
from brokerapp.Messages.forms import SendMessage
from flask_login import current_user,login_required,logout_user
from brokerapp.models import User,Messages
from brokerapp.Messages.forms import SendMessage
from brokerapp import db
from sqlalchemy import or_,union_all,and_
import pandas as pd
from datetime import datetime
messages=Blueprint("messages",__name__)

from brokerapp.Messages.models import save_file






@login_required
@messages.route("/Messages/<int:userid>/<int:senderid>", methods=["GET",'POST'])
def message_send(userid,senderid):
    if current_user.is_authenticated:
        form=SendMessage()
        mydetails=User.query.filter_by(id=current_user.id).first()
        user_details=User.query.filter_by(id=senderid).first()
        if mydetails.id != current_user.id:
            flash("You are not authorized!! ")
            return redirect(url_for('utilities.home'))
        if user_details is None:
            flash("Invaild Recipent")
            return redirect(url_for('utilities.home'))
        title=user_details.firstname+" "+user_details.lastname
        allmessage=Messages.query.filter(and_(Messages.senderid ==senderid,Messages.userid==current_user.id)).union(Messages.query.filter(and_(Messages.senderid ==current_user.id,Messages.userid==senderid))).order_by(Messages.messageid,Messages.messagetime.desc()).all()
        # sendermessage=Messages.query.filter(and_(Messages.senderid==current_user.id,Messages.userid==senderid)).all()
        # allmessage=union_all(Messages.select().where(and_(Messages.userid==current_user.id,Messages.senderid==senderid)), Messages.select().where(and_(Messages.senderid==current_user.id,Messages.userid==senderid)))
        # .union(sendermessage).order_by(Messages.messageid,Messages.messagetime.desc()).all()
        # allmessage=Messages.query.filter(senderid in [senderid,current_user.id],userid in [current_user.id,senderid]).order_by(Messages.messageid,Messages.messagetime.desc()).all()
        # allmessage=usermessage.append(sendermessage)
        # print(usermessage)
        # print(allmessage)
        if form.validate_on_submit():
            if (form.file.data == None) and (str(form.meassage.data)==""):
                return render_template("messages.html",form=form,title=title,userid=userid,senderid=senderid,allmessage=allmessage,User=User)
            if form.file.data != None:
                filename=save_file(form.file.data)
            else:
                filename=""
            mess=Messages(filename=filename,userid=userid,senderid=senderid,messagesdata=form.meassage.data,messagetime=datetime.utcnow())
            db.session.add(mess)
            db.session.commit()
            form=SendMessage()
            return redirect(url_for('messages.message_send',userid=userid,senderid=senderid))
            # return render_template("messages.html",form=form,title=title,userid=userid,senderid=senderid,allmessage=allmessage,User=User)

        return render_template("messages.html",form=form,title=title,userid=userid,senderid=senderid,allmessage=allmessage,User=User)

        # return redirect(url_for('utilities.profile_view',userid=senderid))


    return render_template("home.html",title="Home PostWorld")

@login_required
@messages.route("/Message-Refresh/<int:userid>/<int:senderid>", methods=["GET",'POST'])
def message_refresh(userid,senderid):
    return redirect(url_for('messages.message_send',userid=userid,senderid=senderid))

@login_required
@messages.route("/allmessages", methods=["GET",'POST'])
def message_menu():
    if current_user.is_authenticated:
        send_names=Messages.query.filter(Messages.userid==current_user.id).all()
        recived_names=(Messages.query.filter(Messages.senderid ==current_user.id)).all()
        chatlist=[]
        timelist=[]
        for send in send_names:
            chatlist.append(send.senderid)
            timelist.append(send.messagetime)
        for res in recived_names:
            chatlist.append(res.userid)
            timelist.append(res.messagetime)
        data=pd.DataFrame({"Userid":chatlist,"time":timelist})
        data.sort_values(["time"],inplace=True,ascending=False)
        data.drop_duplicates(["Userid"],inplace=True)
        unique_sender=data["Userid"].to_list()
        return render_template("messagemenu.html",title="PostWorld Messages",unique_sender=unique_sender,User=User)

    return render_template("home.html",title="Home PostWorld")

