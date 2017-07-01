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
        'leader': None,     # 队长实体User
        'member': [],       # 队员实体列表[User]
    }
    members = Member.objects.filter(team=team)
    for member in members:
        if member.role == 'leader':
            t['leader'] = member
        else:
            t['member'].append(members)
    return t


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

    for wm in WorkMeta.objects.filter(course=team.course).order_by('startTime'):
        pass


# 数据整理: [所有团队成绩的列表]
def reportGradeTeams(course):
    if not isinstance(course, Course):
        return None

    ws = []
    workMetas = WorkMeta.objects.filter(course=course)
    teams = Team.objects.filter(course=course)
    # TODO: 需要哪些信息？
    pass


# 数据整理: {单个学生成绩的字典}
def reportGradeStudent(user):
    if not isinstance(user, User):
        return None
    if user.role != 'student':
        log('不是学生', 'reportUtils', LOG_LEVEL.ERROR)
        return False

    pass

# 所有学生成绩的列表
def reportGradeStudents(course):
    if not isinstance(course, Course):
        return None


    pass
