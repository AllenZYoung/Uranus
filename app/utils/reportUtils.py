from app.models import *


# 关于报表的工具集
# by kahsolt

def reportTeam(team):
    if not isinstance(team, Team):
        return False, '参数对象错误'

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


def reportTeams(course):
    if not isinstance(course, Course):
        return False, '参数对象错误'

    ts = []
    teams = Team.objects.filter(course=course)
    for team in teams:
        t = reportTeam(team)
        ts.append(t)
    return ts


def reportWork(workMeta):
    if not isinstance(workMeta, WorkMeta):
        return False, '参数对象错误'

    # TODO: 需要哪些信息？
    pass


def reportWorks(course):
    if not isinstance(course, Course):
        return False, '参数对象错误'

    ws = []
    workMetas = WorkMeta.objects.filter(course=course)
    teams = Team.objects.filter(course=course)
    # TODO: 需要哪些信息？
    pass


def reportGrade(user):
    if not isinstance(user, User):
        return False, '参数对象错误'
    if user.role != 'student':
        return False, '不是学生'

    pass


def reportGradeTeam(team):
    if not isinstance(team, Team):
        return False, '参数对象错误'


def reportGradeTeams(course):
    if not isinstance(course, Course):
        return False, '参数对象错误'