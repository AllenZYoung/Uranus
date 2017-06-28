from random import Random, choice
import random

from app.models import *
from datetime import datetime

def sampleDB():
    trm = choice(Term.objects.filter(year=2017, semester='autumn'))

    # TeamMeta
    tmm = TeamMeta(
        minNum=6,
        maxNum=8,
        startTime=datetime(2017, 6, 24, 9, 0, 0),
        endTime=datetime(2017, 6, 26, 23, 59, 59)
    )
    try:
        tmm.save()
    except:
        pass

    # Course
    crs = Course(
        term=trm,
        teamMeta=tmm,
        name='软件工程小学期实践',
        info='简单地说这门课WiFi很糟糕，但是空调不错',
        syllabus='辣鸡软件，天天开会，为时10天，两次交付',
        classroom='工训3楼',
        credit=2,
        status='ongoing',
        startTime=datetime(2017, 6, 24, 14, 0, 0),
        endTime=datetime(2017, 7, 4, 17, 0, 0)
    )
    try:
        crs.save()
    except:
        pass

    # Enroll
    for stu in User.objects.filter(role='student'):
        enr = Enroll(
            user=stu,
            course=crs,
        )
        try:
            enr.save()
        except:
            pass
    for tec in User.objects.filter(role='teacher'):
        enr = Enroll(
            user=tec,
            course=crs,
        )
        try:
            enr.save()
        except:
            pass

    # Team
    for i in range(1,11):
        S=[
            'incomplete',
            'unsubmitted',
            'auditing',
            'passed',
            'rejected'
        ]
        tem = Team(
            course=crs,
            serialNum=i,
            name=random_str(8),
            status=choice(S),
            info=random_str(32)
        )
        try:
            tem.save()
        except:
            pass

    # Member
    for team in Team.objects.filter():
        for i in range(7):
            mem = Member(
                team=team,
                user=choice(User.objects.filter()),
                role='member',
                contribution=random.random()*0.8 + 0.4
            )
            try:
                mem.save()
            except:
                pass

    # WorkMeta
    wkm = WorkMeta(
        course=crs,
        user=tec,
        title='第一次版本发布',
        content='那么大家提交第一次版本的功能说明之类的吧',
        proportion=0.2,
        submits=3,
        startTime=datetime(2017, 6, 27, 9, 0, 0),
        endTime=datetime(2017, 6, 29, 13, 0, 0)
    )
    try:
        wkm.save()
    except:
        pass

    # Work
    for i in range(5):
        wrk = Work(
            workMeta=wkm,
            team=choice(Team.objects.filter()),
            content=random_str(64),
            review=random_str(32),
            score=random.random()*10.0,
            time=datetime.now()
        )
        try:
            wrk.save()
        except:
            pass

    # File
    fil1 = File()
    fil1.course=crs
    fil1.user=choice(User.objects.filter(role='teacher'))
    fil1.file='/uploads/file/f1.doc'
    fil1.type='document'
    fil1.time=datetime.now()
    try:
        fil1.save()
    except:
        pass
    fil2 = File()
    fil2.course=crs
    fil2.user=choice(User.objects.filter(role='student'))
    fil2.file='/uploads/file/f2.txt'
    fil2.type='text'
    fil2.time=datetime.now()
    try:
        fil2.save()
    except:
        pass

    att = Attachment()
    att.file=fil1
    att.workMeta=wkm
    att.type='workmeta'
    att.save()
    att = Attachment()
    att.file=fil2
    att.work=choice(Work.objects.filter())
    att.type='work'
    try:
        att.save()
    except:
        pass

# Func Tool
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str
