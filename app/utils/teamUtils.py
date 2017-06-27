from django.db.models import Max
from app.models import *


# 发起组队
def createTeam(user, name):
    if not isinstance(user, User):
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
    return team, member


# 解散团队
def dismissTeam(team):
    if not isinstance(team, Team):
        return False, '参数对象错误'
    if team.status == 'passed':
        return False, '团队已通过审核'

    members = Member.objects.filter(team=team)
    for member in members:
        member.delete()
    team.delete()
    return True


# 加入团队
def joinTeam(user, team):
    if not isinstance(team, Team) or not isinstance(user, User):
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
    return member


# 离开团队
def leaveTeam(user):
    if not isinstance(user, User):
        return False, '参数对象错误'
    member = Member.objects.filter(user=user)
    if not member:
        return False, '未加入任何团队'

    member.delete()
    return True


# 转让组长
def transferLeadership(team, user):
    if not isinstance(team, Team) or not isinstance(user, User):
        return False, '参数对象错误'
    if user.role != 'student':
        return False, '不是学生'

    Member.user.objects.filter(team=team, role='leader').update(role='member')
    Member.user.objects.filter(team=team, user=user).update(role='leader')
    return True


# 维护团队信息
def updateInfo(team, **kwargs):
    if not isinstance(team, Team):
        return False, '参数对象错误'

    if kwargs.get('name') is not None:
        team.name = kwargs.get('name')
        team.save()
    if kwargs.get('info') is not None:
        team.info = kwargs.get('info')
        team.save()
    return team


# 完成组队：冻结join
def completeTeam(team):
    if not isinstance(team, Team):
        return False, '参数对象错误'

    team.status = 'unsubmitted'
    team.save()
    return team


# 提交组队申请
def submitTeam(team):
    if not isinstance(team, Team):
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
    return team


# 审核团队：通过
def auditTeamPassed(team):
    if not isinstance(team, Team):
        return False, '参数对象错误'
    if team.status != 'auditing':
        return False, '未提交申请'

    id = 1
    if Team.objects.filter(course=team.course).count() > 0:
        id = Team.objects.filter(course=team.course).aggregate(Max('serialNum')) + 1
    team.status = 'passed'
    team.serialNum = id
    team.save()
    return team


# 审核团队：拒绝
def auditTeamRejected(team, info):
    if not isinstance(team, Team):
        return False, '参数对象错误'
    if team.status != 'auditing':
        return False, '未提交申请'

    team.status = 'rejected'
    team.info = info
    team.save()
    return team


# 设置队员贡献值
def setContribution(user, contribution):
    def validateContribution(c):
        # Method 1:
        return c >= 0.4 and c <= 1.2
        # Method 2:
        # C = [0.4, 0.6, 0.8, 1.0, 1.2]
        # return c in C

    if not isinstance(user, User):
        return False, '参数对象错误'
    if user.role != 'student':
        return False, '不是学生'
    if not validateContribution(contribution):
        return False, '设定的个人贡献比例不在值范围'

    course = Enroll.objects.filter(user=user)
    team = TeamMeta.objects.filter(course=course)
    members = Member.objects.filter(team=team)
    maxContrib = members.count()
    curContrib = 0
    for member in members:
        curContrib += (member.contribution is None) and 0 or member.contribution
    if curContrib + contribution > maxContrib:
        return False, '团队总贡献度超额'
    Member.objects.filter(user=user).update(contribution=contribution)
    return curContrib + contribution