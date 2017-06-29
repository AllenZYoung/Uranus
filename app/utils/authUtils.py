from app.models import *

# 关于身份确认的工具集
# by kahsolt


# 枚举：获取用户角色
def getUserRole(user):
    if not isinstance(user, User):
        return False, '参数对象错误'

    return user.role


# 判断：是教务
def isSystem(user):
    if not isinstance(user, User):
        return False, '参数对象错误'

    return user.role == 'admin'


# 判断：是老师
def isTeacher(user):
    if not isinstance(user, User):
        return False, '参数对象错误'

    return user.role == 'teacher'


# 判断：是学生
def isStudent(user):
    if not isinstance(user, User):
        return False, '参数对象错误'

    return user.role == 'student'


# 判断：是队长
def isTeamLeader(user):
    if not isinstance(user, User):
        return False, '参数对象错误'
    if user.role != 'student':
        return False, '不是学生'
    if not Member.objects.filter(user=user).count() > 0:
        return False, '未加入团队'

    memberships = Member.objects.filter(user=user).first()
    return memberships.role == 'leader'


# 判断：是普通队员
def isTeamMember(user):
    if not isinstance(user, User):
        return False, '参数对象错误'
    if user.role != 'student':
        return False, '不是学生'
    if not Member.objects.filter(user=user).count() > 0:
        return False, '未加入团队'

    memberships = Member.objects.filter(user=user).first()
    return memberships.role == 'member'


# 判断：在指定的团队中
def isMemberOf(user, team):
    if not isinstance(user, User) or not isinstance(team, Team):
        return False, '参数对象错误'
    if user.role != 'student':
        return False, '不是学生'

    return Member.objects.filter(user=user, team=team).count() > 0


# 判断：参与了指定的课程
def isEnrolledIn(user, course):
    if not isinstance(user, User) or not isinstance(course, Course):
        return False, '参数对象错误'
    if user.role != 'student' and user.role != 'teacher':
        return False, '不是学生/老师'

    return Enroll.objects.filter(user=user, course=course).count() > 0
