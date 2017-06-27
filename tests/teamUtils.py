from django.db.models import Max
from app.models import *


# 发起组队
def createTeam(user, name):
    user = User(user)
    if not user:
        return False, '参数对象错误'
    if user.role != 'student':
        return False, '不是学生'
    if Member.objects.filter(user=user).count() > 0:
        return False, '已经是队长或成员'

    team = Team()
    team.course = Enroll.objects.get(user=user).course
    team.name = name
    team.status = 'incomplete'
    team.save()
    member = Member()
    member.user = user
    member.team = team
    member.role = 'leader'
    member.save()
    return True


# 解散团队
def dismissTeam(team):
    team = Team(team)
    if not team:
        return False, '参数对象错误'
    if team.status == 'passed':
        return False, '团队已通过审核'

    members = Member.objects.filter(team=team)
    for member in members:
        member.delete()
    team.delete()


# 加入团队
def joinTeam(user, team):
    user = User(user)
    team = Team(team)
    if not team or not user:
        return False, '参数对象错误'
    if team.status != 'incomplete' or user.role != 'student':
        return False, '团队已冻结/不是学生'
    if Member.objects.filter(user=user).count() > 0:
        return False, '已经是队长或成员'

    member = Member()
    member.user = user
    member.team = team
    member.role = 'member'
    member.save()
    return True


# 离开团队
def leaveTeam(user):
    user = User(user)
    if not user:
        return False, '参数对象错误'
    member = Member.objects.filter(user=user, team=team)
    if not member:
        return False, '未加入任何团队'

    member.delete()
    return True


# 转让组长
def transferLeadership(team, user):
    team = Team(team)
    user = User(user)
    if not team or not user:
        return False, '参数对象错误'
    if user.role != 'student':
        return False, '不是学生'

    Member.user.objects.filter(team=team, role='leader').update(role='member')
    Member.user.objects.filter(team=team, user=user).update(role='leader')
    return True


# 维护团队信息
def updateInfo(team, **kwargs):
    team = Team(team)
    if not team:
        return False, '参数对象错误'

    if kwargs.get('name') is not None:
        team.name = kwargs.get('name')
    if kwargs.get('info') is not None:
        team.info = kwargs.get('info')
    return True


# 完成组队：冻结join
def completeTeam(team):
    team = Team(team)
    if not team:
        return False, '参数对象错误'

    team.status = 'unsubmitted'
    team.save()
    return True


# 提交组队申请
def submitTeam(team):
    team = Team(team)
    if not team:
        return False, '参数对象错误'
    if team.status != 'unsubmitted':
        return False, '未审核且已冻结的团队才能提交申请'
    num = Member.objects.filter(team=team).count()
    if num < team.course.teamMeta.minNum or num > team.course.teamMeta.maxNum:
        return False, '不在人数限制范围'
    num = Member.user.objects.filter(gender='female')
    if num != 1:
        return False, '性别要求不合'

    team.status = 'auditing'
    team.save()
    return True


# 审核团队：通过
def auditTeamPassed(team):
    team = Team(team)
    if not team:
        return False, '参数对象错误'
    if team.status != 'auditing':
        return False, '未提交申请'

    id = 1
    if Team.objects.filter(course=team.course).count() > 0:
        id = Team.objects.filter(course=team.course).aggregate(Max('serialNum')) + 1
    team.status = 'passed'
    team.serialNum = id
    team.save()
    return True


# 审核团队：拒绝
def auditTeamRejected(team, info):
    team = Team(team)
    if not team:
        return False, '参数对象错误'
    if team.status != 'auditing':
        return False, '未提交申请'

    team.status = 'rejected'
    team.info = info
    team.save()
    return True
