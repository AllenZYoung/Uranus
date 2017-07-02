from app.utils.logUtils import log, LOG_LEVEL
from app.models import *

# 关于统计计算的工具集, 从属于reportUtils
# by kahsolt


# 团队总成绩
def sumGradeTeam(team):
    if not isinstance(team, Team):
        return None

    grade = 0
    wms = WorkMeta.objects.filter(course=team.course)
    for wm in wms:
        w = Work.objects.filter(team=team, workMeta=wm).order_by('-time').first()
        if w:
            grade += w.score or 0.0
    return grade


# 个人总成绩
def sumGradeStudent(user):
    if not isinstance(user, User):
        return None
    member = Member.objects.filter(user=user).first()
    if not member:
        log('未加入任何团队', 'statisticsUils', LOG_LEVEL.ERROR)
        return False
    contrib = member.contribution
    if not contrib:
        log('未设置个人贡献度', 'statisticsUils', LOG_LEVEL.INFO)
        return 0

    return contrib * (sumGradeTeam(member.team) or 0.0)


# 团队平均成绩
def meanGradeTeam(course):
    if not isinstance(course, Course):
        return None
    teams = Team.objects.filter(course=course)
    cnt = teams.count()
    if cnt == 0:
        return 0

    sum = 0
    for t in teams:
        sum += sumGradeTeam(t) or 0.0

    return sum / cnt


# 个人平均成绩
def meanGradeStudent(course):
    if not isinstance(course, Course):
        return None
    users = Enroll.objects.filter(course=course)
    cnt = users.count()
    if cnt == 0:
        return 0

    sum = 0
    for u in users:
        sum += sumGradeStudent(u) or 0.0

    return sum / cnt
