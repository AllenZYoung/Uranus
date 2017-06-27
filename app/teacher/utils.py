# -*- coding: utf-8 -*-
# define your utility function here
import os
from datetime import datetime


# todo save file into database according to the user
def handle_uploaded_file(request):
    f = request.FILES['file']
    name = f.name
    new_name = name.split('.', 1)[0] + '-' + datetime.now().strftime("%Y-%m-%d-%H-%M-%S").__str__() + '.' + \
               name.split('.', 1)[1]
    with open(os.path.join('uploads/file/teacher/', new_name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
