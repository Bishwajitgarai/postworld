from flask import url_for
import smtplib
from brokerapp.User.forms import User
from brokerapp import createapp
app=createapp()




def send_email(User_id):
    token=User.get_rest_token(User_id)
    # print(token)
    msg=url_for('users.resetpassword',token=token,_external=True)
    subject="PostWorld : passworld rest link."
    message=f"The Password rest link is {msg} \n Please do not share with others. It is vaild for 15 minutes."
    full_msg = 'Subject: {}\n\n{}'.format(subject, message)
    user=User.query.filter_by(id=User_id.id).first()
    user_email=user.email
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login("official.postworld@gmail.com", "tyvmsfkgctgcsgem")

    # sending the mail
    s.sendmail("official.postworld@gmail.com", user_email, full_msg)

    # terminating the session
    s.quit()
    print("Message Sucessfully Send")
