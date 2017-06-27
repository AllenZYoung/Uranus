# -*- coding: utf-8 -*-
# define your utility function here
import os
from datetime import datetime
from openpyxl import *
from app.models import *


# todo save file into database according to the user
def handle_uploaded_file(request):
    f = request.FILES['file']
    name = f.name
    new_name = name.split('.', 1)[0] + '-' + datetime.now().strftime("%Y-%m-%d-%H-%M-%S").__str__() + '.' + \
               name.split('.', 1)[1]
    with open(os.path.join('uploads/file/teacher/', new_name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def import_student_for_course(request):
    course_id = request.POST.get('course_id', None)
    f = request.FILES['file']
    name = f.name
    suffix = name.split('.', 1)[1]
    if suffix == 'xls' or suffix == 'xlsx':
        path = os.path.join('uploads/file/teacher/', name)
        with open(path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        wb = load_workbook(filename=path)
        sheet = wb.active
        ids = []
        for i in range(2, 10000):
            if sheet['A' + str(i)] is None:
                break
            else:
                ids.append(sheet['A' + str(i)])
        students_to_course(ids, course_id)
        os.remove(path)
        return 'import students for course success'
    else:
        return 'upload file must be a xls or xlsx excel'


def students_to_course(students_id, course_id):
    User.objects.filter(role='student', course_id=course_id).delete()
    course = Course.objects.get(id=course_id)
    for id in students_id:
        student = User.objects.get(username=id)
        enroll = Enroll(course=course, user=student)
        enroll.save()
