from app.utils.statisticsUtils import *
import pprint

# 关于报表的工具集
# by kahsolt


# 数据整理: {单个团队信息的字典}
def reportTeam(team):
    if not isinstance(team, Team):
        return None

    t = {
        'id': team.serialNum,
        'name': team.name,
        'status': team.get_status_display(),
        'leader': None,     # 队长实体User
        'member': [],       # 队员实体列表[User]
    }
    t['member'] = list()
    members = Member.objects.filter(team=team)
    for member in members:
        if member.role == 'leader':
            t['leader'] = member
        elif member.role == 'member':
            t['member'].append(member)
    return t



# 数据整理: [所有团队信息字典的列表]
def reportTeams(course, is_ordered=True):
    if not isinstance(course, Course):
        return None

    ts = []
    if is_ordered:
        teams = Team.objects.filter(course=course).order_by('serialNum')
    else:
        teams = Team.objects.filter(course=course)
    for team in teams:
        t = reportTeam(team)
        pprint.pprint(t)
        ts.append(t)
    return ts


# 数据整理: {单个团队成绩的字典}
def reportGradeTeam(team):
    if not isinstance(team, Team):
        return None

    grade = {}
    ws = Work.objects.filter(team=team)
    for wm in WorkMeta.objects.filter(course=team.course).order_by('startTime'):
        w = ws.filter(workMeta=wm).order_by('-time').first()
        if w:
            grade[wm.id] = w.score or 0      # 作业ID(不是连续流水号), 或许该用Title？
        else:
            grade[wm.id] = 0
    return grade


# 数据整理: [某课的团队成绩报表]
def reportGradeTeams(course):
    if not isinstance(course, Course):
        return None

    grades = []
    teams = Team.objects.filter(course=course).order_by('serialNum')
    for t in teams:
        g = reportGradeTeam(t)
        grades.append(g)
    return grades


# # 数据整理: {单个学生总成绩的字典}
# def reportGradeStudent(user):
#     if not isinstance(user, User):
#         return None
#     if user.role != 'student':
#         log('不是学生', 'reportUtils', LOG_LEVEL.ERROR)
#         return False
#     member = Member.objects.filter(user=user).first()
#     if not member:
#         log('未加入任何团队', 'teamutils', LOG_LEVEL.ERROR)
#         return False
#
#     ret = {
#         'user': user,
#         'grade': sumGradeStudent(user),
#     }
#     return ret
#
#
# # 数据整理: [某课的学生成绩报表]
# def reportGradeStudents(course):
#     if not isinstance(course, Course):
#         return None
#
#     grades = []
#     enrolls = Enroll.objects.filter(course=course)
#     for e in enrolls:
#         g = reportGradeStudent(e.user)
#         grades.append(g)
#     return grades


# 数据整理: [某个作业的所有分数]
def reportGradeWorkMeta(workMeta):
    if not isinstance(workMeta, WorkMeta):
        return None

    grade = []
    teams = Team.objects.filter(course=workMeta.course)
    for t in teams:
        g = reportGradeTeam(t)
        grade.append(g)
    return grade


# 数据整理: [某课的作业成绩报表]
def reportGradeWorkMetas(course):
    if not isinstance(course, Course):
        return None

    grades = []
    wms = WorkMeta.objects.filter(course=course)
    for wm in wms:
        g = reportGradeWorkMeta(wm)
        grades.append(g)
    return grades


##
# 测试
def test():
    log('='*50)
    log('Report Utils Unit Test')

    c = Course.objects.first()
    log(reportTeams(c), 'reportTeams')
    log(reportGradeTeams(c),'reportGradeTeams')
    log(reportGradeWorkMetas(c), 'reportGradeWorkMetas')
    log(meanGradeTeam(c), 'meanGradeTeam')
    log(meanGradeStudent(c), 'meanGradeStudent')

    t = Team.objects.first()
    log(sumGradeTeam(t), 'sumGradeTeam')

    u = User.objects.filter(role='student').first()
    log(sumGradeStudent(u), 'sumGradeStudent')

    log('='*50)
