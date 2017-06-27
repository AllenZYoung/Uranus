from app.models import *


def reportTeam(team):
    if team is None:
        return
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
    if course is None:
        return
    ts = []
    teams = Team.objects.filter(course=course)
    for team in teams:
        t = reportTeam(team)
        ts.append(t)
    return ts


def reportWork(workMeta):
    # TODO: 需要哪些信息？
    pass


def reportWorks(course):
    ws = []
    workMetas = WorkMeta.objects.filter(course=course)
    teams = Team.objects.filter(course=course)
    # TODO: 需要哪些信息？
    pass


def reportGrade(user):
    if user is None or user.role != 'student':
        print('[Report]: user role must be "student"')
        return
    pass


def reportGradeTeam(team):
    if team is None:
        return


def reportGradeTeams(course):
    if course is None:
        return
