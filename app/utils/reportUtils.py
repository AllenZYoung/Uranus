from app.models import *
from app.utils.logUtils import *


# 关于报表的工具集
# by kahsolt


# 数据整理: {单个团队信息的字典}
def reportTeam(team):
    if not isinstance(team, Team):
        return None

    t = {
        'id': team.serialNum,
        'name': team.name,
        'status': team.get_status_display,
        'leader': None,     # 队长实体User
        'member': [],       # 队员实体列表[User]
    }
    members = Member.objects.filter(team=team)
    for member in members:
        if member.role == 'leader':
            t['leader'] = member.user.name
        else:
            t['member'].append(member.user.name)




# 数据整理: [所有团队信息字典的列表]
def reportTeams(course):
    if not isinstance(course, Course):
        return None

    ts = []
    teams = Team.objects.filter(course=course).order_by('serialNum')
    for team in teams:
        t = reportTeam(team)
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
            grade[wm.id] = w.score      # 作业ID(不是连续流水号), 或许该用Title？
        else:
            grade[wm.id] = 0
    return grade


# 数据整理: [所有团队成绩的列表]
def reportGradeTeams(course):
    if not isinstance(course, Course):
        return None

    grades = []
    teams = Team.objects.filter(course=course).order_by('serialNum')
    for t in teams:
        g = reportGradeTeam(t)
        grades.append(g)
    return grades


# 数据整理: {单个学生成绩的字典}
def reportGradeStudent(user):
    if not isinstance(user, User):
        return None
    if user.role != 'student':
        log('不是学生', 'reportUtils', LOG_LEVEL.ERROR)
        return False
    member = Member.objects.filter(user=user).first()
    if not member:
        log('未加入任何团队', 'teamutils', LOG_LEVEL.ERROR)
        return False

    ret = {
        'user': user,
        'grade': 0,
    }
    # TODO: 根据贡献度计算总分??
    return ret


# 所有学生成绩的列表
def reportGradeStudents(course):
    if not isinstance(course, Course):
        return None

    grades = []
    enrolls = Enroll.objects.filter(course=course)
    for e in enrolls:
        g = reportGradeStudent(e.user)
        grades.append(g)
    return grades
