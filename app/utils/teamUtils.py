from django.db.models import Max
from app.models import *
from app.utils.logUtils import log, LOG_LEVEL


# 关于团队管理的工具集
# by kahsolt


# 发起组队
def createTeam(user, name):
    if not isinstance(user, User):
        return None
    if user.role != 'student':
        log('不是学生', 'teamutils', LOG_LEVEL.ERROR)
        return False
    if Member.objects.filter(user=user).count() > 0:
        log('已经是队长或成员', 'teamutils', LOG_LEVEL.ERROR)
        return False

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
        return None
    if team.status == 'passed':
        log('团队已通过审核', 'teamutils', LOG_LEVEL.ERROR)
        return False

    members = Member.objects.filter(team=team)
    for member in members:
        member.delete()
    team.delete()
    return True


# 加入团队
def joinTeam(user, team):
    if not isinstance(team, Team) or not isinstance(user, User):
        return None
    if team.status != 'incomplete' or user.role != 'student':
        log('团队已冻结/不是学生', 'teamutils', LOG_LEVEL.ERROR)
        return False
    if Member.objects.filter(user=user).count() > 0:
        log('已经是队长或成员', 'teamutils', LOG_LEVEL.ERROR)
        return False

    member = Member()
    member.user = user
    member.team = team
    member.role = 'newMoe'
    member.save()
    return member


# 离开团队
def leaveTeam(user):
    if not isinstance(user, User):
        return None
    member = Member.objects.filter(user=user)
    if not member:
        log('未加入任何团队', 'teamutils', LOG_LEVEL.ERROR)
        return False

    member.delete()
    return True


# 转让组长
def transferLeadership(team, user):
    if not isinstance(team, Team) or not isinstance(user, User):
        return None
    if user.role != 'student':
        log('不是学生', 'teamutils', LOG_LEVEL.ERROR)
        return False

    Member.objects.filter(team=team, role='leader').update(role='member')
    Member.objects.filter(team=team, user=user).update(role='leader')
    return True


# 维护团队信息
def updateInfo(team, **kwargs):
    if not isinstance(team, Team):
        return None

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
        return None

    team.status = 'unsubmitted'
    team.save()
    return team


# 提交组队申请
def submitTeam(team):
    if not isinstance(team, Team):
        return None
    if team.status != 'unsubmitted':
        log('未审核且已冻结的团队才能提交申请', 'teamutils', LOG_LEVEL.ERROR)
        return False
    num = Member.objects.filter(team=team).count()
    if num < team.course.teamMeta.minNum or num > team.course.teamMeta.maxNum:
        log('不在人数限制范围', 'teamutils', LOG_LEVEL.ERROR)
        return False
    num = Member.user.objects.filter(gender='female')
    if num != 1:
        log('性别要求不合', 'teamutils', LOG_LEVEL.ERROR)
        return False

    team.status = 'auditing'
    team.save()
    return team


# 审核队员：通过
def auditMemberPassed(user):
    if not isinstance(user, User):
        return None
    member = Member.objects.filter(user=user).first()
    if not member:
        log('未加入任何团队', 'teamutils', LOG_LEVEL.ERROR)
        return False
    if not member.role == 'newMoe':
        log('不是新人', 'teamutils', LOG_LEVEL.ERROR)
        return False

    member.role = 'member'
    member.save()
    return member


# 审核队员：拒绝
def auditMemberRejected(user):
    return leaveTeam(user)


# 审核团队：通过
def auditTeamPassed(team):
    if not isinstance(team, Team):
        return None
    if team.status != 'auditing':
        log('未提交申请', 'teamutils', LOG_LEVEL.ERROR)
        return False

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
        return None
    if team.status != 'auditing':
        log('未提交申请', 'teamutils', LOG_LEVEL.ERROR)
        return False

    team.status = 'rejected'
    team.info = info
    team.save()
    return team


# 设置队员贡献值
def setContribution(user, contribution):
    def validateContribution(c):
        # Method 1:
        return c >= 0.4 and c <= 1.6
        # Method 2:
        # C = [0.4, 0.6, 0.8, 1.0, 1.2]
        # return c in C

    if not isinstance(user, User):
        return None
    if not validateContribution(contribution):
        log('设定的个人贡献比例不在值范围', 'teamutils', LOG_LEVEL.ERROR)
        return False

    enroll = Enroll.objects.filter(user=user).first()
    team = Team.objects.filter(course=enroll.course).first()
    members = Member.objects.filter(team=team)
    maxContrib = members.count()
    curContrib = 0
    curContrib += contribution
    if curContrib > maxContrib:
        log('团队总贡献度超额', 'teamutils', LOG_LEVEL.ERROR)
        return False

    Member.objects.filter(user=user).update(contribution=contribution)
    log('setContribution OK', 'teamutils', LOG_LEVEL.INFO)
    return curContrib + contribution

# 按照团队角色对团队成员进行排序，newMoe > leader > member
def sort_team_members(member_list):
    newMoe = []
    leader = []
    member = []
    for _member in member_list:
        if _member.role == 'newMoe':
            newMoe.append(_member)
        elif _member.role == 'leader':
            leader.append(_member)
        else:
            member.append(_member)
    newMoe.extend(leader)
    newMoe.extend(member)
    return newMoe