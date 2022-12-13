
from secrets import token_hex
import os
from PIL import Image
from brokerapp import createapp
app=createapp()



def post_save_image(userid,image):
    # print(image.filename)
    pic=Image.open(image)
    random_hex=token_hex(8)
    _name,extension=os.path.split(image.filename)
    picture_fn=str('Post_pic-'+userid+"-"+random_hex+extension).replace(" ","_")
    picture_path=app.root_path+'/static/images/'+picture_fn
    # image.save(picture_path)
    pic.save(picture_path)
    return '/static/images/'+picture_fn