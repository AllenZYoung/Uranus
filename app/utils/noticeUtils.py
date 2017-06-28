from app.models import *


def listNotice(course):
    course = Course(course)
    if not course:
        return False, '参数对象错误'

    notices = Notice.objects.filter(course=course).order_by('-time')
    return notices


def addNotice(title, content, user):
    user = User(user)
    if not user:
        return False, '参数对象错误'
    if title == '' or title is None or content == '' or content is None:
        return False, '标题/内容不能为空'

    notice = Notice()
    notice.title = title
    notice.content = content
    notice.user = user
    notice.save()
    return notice


def updateNotice(notice, **kwargs):
    if not isinstance(notice, Notice):
        return False, '参数对象错误'

    if kwargs.get('title') is not None:
        notice.title = kwargs.get('title')
        notice.save()
    if kwargs.get('content') is not None:
        notice.content = kwargs.get('content')
        notice.save()
    return notice


def deleteNotice(notice):
    if not isinstance(notice, Notice):
        return False, '参数对象错误'

    notice.delete()
    return True