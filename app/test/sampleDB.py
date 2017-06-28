from app.models import *
from datetime import datetime


def sampleDB():
    stu1 = User()
    stu1.username='14210000'
    stu1.password='123'
    stu1.name='学生1'
    stu1.classID='142112'
    stu1.gender='male'
    stu1.role='student'
    stu1.tel='13901020304'
    stu1.email='stu1@buaa.edu.cn'
    stu1.save()

    stu2 = User()
    stu2.username='14210001'
    stu2.password='123'
    stu2.name='学生2'
    stu2.classID='142115'
    stu2.gender='female'
    stu2.role='student'
    stu2.tel='13901020305'
    stu2.email='stu2@buaa.edu.cn'
    stu2.save()

    tec = User()
    tec.username='233'
    tec.password='123'
    tec.name='老师'
    tec.role='teacher'
    tec.tel='13901020304'
    tec.email='tec@buaa.edu.cn'
    tec.save()

    adm = User()
    adm.username='666'
    adm.password='123'
    adm.name='教务'
    adm.role='admin'
    adm.save()

    trm = Term()
    trm.info='这是2017年春季学期'
    trm.year=2017
    trm.semester='pring'
    trm.startWeek=18
    trm.endWeek=20
    trm.save()

    tmm = TeamMeta()
    tmm.minNum=6
    tmm.maxNum=8
    tmm.startTime=datetime(2017, 6, 24, 9, 0, 0)
    tmm.endTime=datetime(2017, 6, 26, 23, 59, 59)
    tmm.save()

    crs = Course()
    crs.term=trm
    crs.teamMeta=tmm
    crs.name='软件工程小学期实践'
    crs.info='简单地说这门课WiFi很糟糕，但是空调不错'
    crs.syllabus='辣鸡软件，天天开会，为时10天，两次交付'
    crs.classroom='工训3楼'
    crs.credit=2
    crs.status='ongoing'
    crs.startTime=datetime(2017, 6, 24, 14, 0, 0)
    crs.endTime=datetime(2017, 7, 4, 17, 0, 0)
    crs.save()

    enr=Enroll()
    enr.course=crs
    enr.user=stu1
    enr.save()
    enr=Enroll()
    enr.course=crs
    enr.user=stu2
    enr.save()
    enr=Enroll()
    enr.course=crs
    enr.user=tec
    enr.save()

    tem = Team()
    tem.course=crs
    tem.serialNum=1
    tem.name='Uranus'
    tem.status='passed'
    tem.info='据说要比Leviathan大……'
    tem.save()

    mem1 = Member()
    mem1.team=tem
    mem1.user=stu1
    mem1.role='leader'
    mem1.contribution=0.4
    mem1.save()
    mem2 = Member()
    mem2.team=tem
    mem2.user=stu2
    mem2.role='member'
    mem2.contribution=0.6
    mem2.save()

    wkm = WorkMeta()
    wkm.course=crs
    wkm.user=tec
    wkm.title='第一次版本发布'
    wkm.content='那么大家提交第一次版本的功能说明之类的吧'
    wkm.proportion=0.2
    wkm.submits=3
    wkm.startTime=datetime(2017, 6, 27, 9, 0, 0)
    wkm.endTime=datetime(2017, 6, 29, 13, 0, 0)
    wkm.save()

    wrk1 = Work()
    wrk1.workMeta=wkm
    wrk1.team=tem
    wrk1.content='呐，这就是我们组交的东西，看附件！'
    wrk1.review='可以，666！'
    wrk1.score=10.0
    wrk1.time=datetime.now()
    wrk1.save()
    wrk2 = Work()
    wrk2.workMeta=wkm
    wrk2.team=tem
    wrk2.content='这个作业没有附件'
    wrk2.review='什么鬼，零分！'
    wrk2.score=0.0
    wrk2.time=datetime.now()
    wrk2.save()

    fil1 = File()
    fil1.course=crs
    fil1.user=tec
    fil1.file='/uploads/file/f1.doc'
    fil1.type='document'
    fil1.time=datetime.now()
    fil1.save()
    fil2 = File()
    fil2.course=crs
    fil2.user=stu1
    fil2.file='/uploads/file/f2.txt'
    fil2.type='text'
    fil2.time=datetime.now()
    fil2.save()

    att = Attachment()
    att.file=fil1
    att.workMeta=wkm
    att.type='workmeta'
    att.save()
    att = Attachment()
    att.file=fil2
    att.work=wrk1
    att.type='work'
    att.save()
