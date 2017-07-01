from app.models import *
from app.utils.logUtils import *

# 关于身份确认的工具集
# by kahsolt


# 枚举：获取用户角色
def getUserRole(user):
    if not isinstance(user, User):
        return None

    return user.role


# 判断：是教务
def isSystem(user):
    if not isinstance(user, User):
        return None
    return user.role == 'admin'


# 判断：是老师
def isTeacher(user):
    if not isinstance(user, User):
        return None
    return user.role == 'teacher'


# 判断：是学生
def isStudent(user):
    if not isinstance(user, User):
        return None
    return user.role == 'student'


# 判断：是队长
def isTeamLeader(user):
    if not isinstance(user, User):
        return None
    if user.role != 'student':
        log('不是学生', 'authUtils', LOG_LEVEL.ERROR)
        return False
    if not Member.objects.filter(user=user).count() > 0:
        log('未加入团队', 'authUtils', LOG_LEVEL.ERROR)
        return False

    memberships = Member.objects.filter(user=user).first()
    return memberships.role == 'leader'


# 判断：是普通队员
def isTeamMember(user):
    if not isinstance(user, User):
        return None
    if user.role != 'student':
        log('不是学生', 'authUtils', LOG_LEVEL.ERROR)
        return False
    if not Member.objects.filter(user=user).count() > 0:
        log('未加入团队', 'authUtils', LOG_LEVEL.ERROR)
        return False

    memberships = Member.objects.filter(user=user).first()
    return memberships.role == 'member'


# 判断：在指定的团队中
def isMemberOf(user, team):
    if not isinstance(user, User) or not isinstance(team, Team):
        return None
    if user.role != 'student':
        log('不是学生', 'authUtils', LOG_LEVEL.ERROR)
        return False

    return Member.objects.filter(user=user, team=team).count() > 0


# 判断：参与了指定的课程
def isEnrolledIn(user, course):
    if not isinstance(user, User) or not isinstance(course, Course):
        return None
    if user.role != 'student' and user.role != 'teacher':
        log('不是学生/老师', 'authUtils', LOG_LEVEL.ERROR)
        return False

    return Enroll.objects.filter(user=user, course=course).count() > 0


# 判断: 某个团队通过了老师审核
def isTeamAudited(team):
    if not isinstance(team, Team):
        return None

    return team.status == 'passed'


# 判断: 所有队员通过了团长审核
def isMembersAudited(team):
    if not isinstance(team, Team):
        return None

    members = Member.objects.filter(team=team)
    for m in members:
        if m.role == 'newMoe':
            return False
    return True