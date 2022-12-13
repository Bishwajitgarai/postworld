from secrets import token_hex
import os
from brokerapp import createapp
app=createapp()


def save_file(file):
    random_hex=token_hex(8)
    _name,extension=os.path.split(file.filename)
    file_fn=str('file_'+random_hex+extension).replace(" ","_")
    file_path=app.root_path+'/static/files/'+file_fn
    file.save(file_path)
    return file_fn