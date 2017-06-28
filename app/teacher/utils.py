# -*- coding: utf-8 -*-
# define your utility function here
import os
from datetime import datetime
from openpyxl import *
from app.models import *
from django.shortcuts import get_object_or_404


def handle_uploaded_file(request,course_id,f):
    # f = request.FILES['file']
    # name = f.name
    # new_name = name.split('.', 1)[0] + '-' + datetime.now().strftime("%Y-%m-%d-%H-%M-%S").__str__() + '.' + \
    #            name.split('.', 1)[1]
    # with open(os.path.join('uploads/file/teacher/', new_name), 'wb+') as destination:
    #     for chunk in f.chunks():
    #         destination.write(chunk)
    #f=form.cleaned_data['file']
    teacher=get_object_or_404(User,username=request.user.username)
    file=File(course_id=course_id,time=datetime.now(),file=f,user=teacher)
    file.save()


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


def add_homework(homework_form, course_id, username,file):
    content = homework_form.cleaned_data['content']
    proportion = homework_form.cleaned_data['proportion']
    submits = homework_form.cleaned_data['submits']
    startTime = homework_form.cleaned_data['startTime']
    endTime = homework_form.cleaned_data['endTime']
    title=homework_form.cleaned_data['title']
    teacher = get_object_or_404(User, username=username)
    workmeta = WorkMeta(course_id=course_id, user=teacher, content=content,title=title,
                        proportion=proportion, submits=submits, startTime=startTime, endTime=endTime)
    workmeta.save()
    if file is not None:
        f=File(course_id=course_id,user=teacher,file=file,type='text',time=datetime.now())
        f.save()
        attachment = Attachment(file=f, workMeta=workmeta, type='workmeta')
        attachment.save()


# 获取一个老师往期课程的所有作业
def get_past_homeworks(username):
    teacher = get_object_or_404(User, username=username)
    enrolls = Enroll.objects.filter(user__username=teacher.username)
    homeworks = []
    present = datetime.now()
    for enroll in enrolls:
        course = enroll.course
        if course.endTime.replace(tzinfo=None) <= present:
            workmetas = WorkMeta.objects.filter(course_id=course.id)
            homeworks.extend(workmetas)
    return homeworks

#获取当前学期
def get_now_term():
    now_term = Term.objects.all().order_by('-id')[0]
    return now_term


# 获取团队成绩表的完整路径名
def get_team_score_excel_file_abspath():
    now_term = get_now_term()

    # 第一次计算出各团队得分之后保存到excel表，以便老师下载
    # 各个团队得分的excel命名规范：termYear_termsemester_team_score_list.xlsx
    file_path = os.path.join(os.path.abspath('.'), 'downloads', 'teamScores')
    file_name = '' + now_term.year + now_term.semester + 'team_score_list.xlsx'
    file = file_path + file_name
    return file


# 获取学生成绩表的excel的完整路径名
def get_stu_score_excel_file_abspath():
    now_term = get_now_term()

    # 各人得分的excel命名规范：termYear_termsemester_stu_score_list.xlsx
    file_path = os.path.join(os.path.abspath('.'), 'downloads', 'stuScores')
    file_name = '' + now_term.year + now_term.semester + 'stu_score_list.xlsx'
    file = file_path + file_name
    return file


# 保存团队得分表到excel
def create_team_score_excel(file, team_list, score_list):
    work_book = Workbook()
    ws = work_book.get_active_sheet()
    ws.cell(row=0, column=0).value = '团队id'
    ws.cell(row=0, column=1).value = '团队名称'
    ws.cell(row=0, column=2).value = '分数'

    for i in range(0,len(team_list)):
        num = i+1;
        ws.cell(row=num, column=0).value = num
        ws.cell(row=num, column=1).value = team_list[i].name
        ws.cell(row=num, column=2).value = score_list[i]
    work_book.save(filename=file)


def create_team_score_excel(file, stu_list, member_score_dict):
    work_book = Workbook()
    ws = work_book.get_active_sheet()
    ws.cell(row=0, column=0).value = '学号'
    ws.cell(row=0, column=1).value = '姓名'
    ws.cell(row=0, column=2).value = '分数'

    num = 1;
    for stu in stu_list:
        ws.cell(row=num, column=0).value = stu.username
        ws.cell(row=num, column=1).value = stu.name
        ws.cell(row=num, column=2).value = member_score_dict[stu]
        ++num
    work_book.save(filename=file)



#计算团队得分
def compute_team_score():
    now_term = get_now_term()
    team_list = get_team_list_in_now_term()
    score_list = []
    team_score = {}
    for team in team_list:
        work_list = Work.objects.filter(team=team)
        score = 0
        for work in work_list:
            score += work.score * work.workMeta.proportion
            team_score[team] = score
        score_list.append(score)
    return team_list, score_list, team_score


# 计算个人总得分 dict: key=team_member, value=score
def compute_member_score():
    x, y, team_score = compute_team_score()
    member_score = {}
    for team in team_score:
        team_member = Member.objects.filter(team=team)
        for member in team_member:
            score = team_score[team] * member.contribution
            member_score[member] = score
    return member_score



# 获取当前学期的所有team,并排序
def get_team_list_in_now_term():
    now_term = get_now_term()
    team_list = Team.objects.filter(course__term=now_term).order_by('id')
    return team_list


# 获取当前学期所有参加的学生，并按学号排序
def get_members_list_in_now_term():
    team_list = get_team_list_in_now_term()
    members_list = []
    for team in team_list:
        team_member = Member.objects.filter(team=team)
        members_list.extend(team_member)
    members_list = sorted(members_list, key=lambda x : x.username)
    return members_list


# 读取file文件
def file_iterator(file_name, chunk_size=512):
    with open(file_name) as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

