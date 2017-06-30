from app.models import *
from app.utils.logUtils import *

# 关于公告牌的工具集
# by kahsolt


def listNotice(course):
    if not isinstance(course, Course):
        return None

    notices = Notice.objects.filter(course=course).order_by('-time')
    return notices


def addNotice(title, content, user):
    if not isinstance(user, User):
        return None
    if title == '' or title is None or content == '' or content is None:
        log('标题/内容不能为空', 'noticeUtils', LOG_LEVEL.ERROR)
        return False

    notice = Notice()
    notice.title = title
    notice.content = content
    notice.user = user
    notice.save()
    return notice


def updateNotice(notice, **kwargs):
    if not isinstance(notice, Notice):
        return None

    if kwargs.get('title') is not None:
        notice.title = kwargs.get('title')
        notice.save()
    if kwargs.get('content') is not None:
        notice.content = kwargs.get('content')
        notice.save()
    return notice


def deleteNotice(notice):
    if not isinstance(notice, Notice):
        return None

    notice.delete()
    return True