# -*- coding: utf-8 -*-
#define your utility function here
import pytz
import datetime
import os
from app import models
from django.contrib.auth.models import User
from openpyxl.reader.excel import load_workbook

def isItemRepeated(user_id):
    all_user = models.User.objects.filter(username=user_id)
    if(all_user):
        return True
    return False

def handle_uploaded_user(request, f=None, user_role='student'):
    datenow = datetime.datetime.now()
    filedate = datenow.strftime('%Y%m%d-%H%M%S')
    path = os.path.join(os.path.abspath('.'),'uploads','user')
    filepath = path + '/' + filedate + '_' + f.name
    with open(filepath, 'ab') as de:
        for chunk in f.chunks():
            de.write(chunk)
    wb = load_workbook(filepath)
    print(filepath)
    table = wb.get_sheet_by_name(wb.get_sheet_names()[0])
    user_list = []
    for i in range(2, table.max_row + 1):
        if table.cell(row=i, column=1).value is None:
            # '为空，应跳过'
            continue
        print('正在导入第' + str(i - 1) + '行...')

        user_id = table.cell(row=i,column=1).value
        #数据库已存在相同的信息，应跳过
        if isItemRepeated(user_id):
            continue
        user_sex = table.cell(row=i, column=3).value
        sex = 'male'
        if (user_sex.find('女') != -1):
            sex = 'female'
        model_user = models.User(
            username = user_id,
            password = 'Student123',
            name = table.cell(row=i,column=2).value,
            role = user_role,
            gender = sex,
            tel = table.cell(row=i, column=4).value
        )
        if(user_role=='student'):
            model_user.classID = classID = table.cell(row=i,column=5).value
        user = User.objects.create_user(username=user_id, password='Teacher123')
        user_list.append(model_user)
    models.User.objects.bulk_create(user_list)