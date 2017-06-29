# Author: kahsolt
# Date: 2017-06-26
# Principle: Maintain tables as least as possible!

import os

from django.db import models
from datetime import datetime


# [用户:学生/教师/教务账户]
class User(models.Model):
    username = models.CharField(unique=True, max_length=32, help_text='学号/工号')
    password = models.CharField(max_length=64)
    name = models.CharField(max_length=32, null=True, blank=True, help_text='实名')
    classID = models.CharField(max_length=16, null=True, blank=True, help_text='班号')
    ROLE = (
        ('student', '学生'),
        ('teacher', '教师'),
        ('admin', '教务'),
    )
    role = models.CharField(max_length=16, choices=ROLE, default='student')
    GENDER = (
        ('male', '男'),
        ('female', '女'),
    )
    gender = models.CharField(max_length=8, choices=GENDER, default='male')
    tel = models.CharField(max_length=16, null=True, blank=True, help_text='电话')
    email = models.EmailField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.name or self.username

# [学期]
class Term(models.Model):
    info = models.TextField(blank=True, help_text='学期说明信息')
    year = models.IntegerField(default=datetime.now().year)
    SEMESTER = (
        ('spring', '春季学期'),
        ('autumn', '秋季学期'),
    )
    semester = models.CharField(max_length=8, choices=SEMESTER, default='spring')
    startWeek = models.PositiveSmallIntegerField(null=True, blank=True, help_text='课程开始的周次')
    endWeek = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        sem = self.semester == 'spring' and '春季学期' or '秋季学期'
        return '%d年%s' %(self.year, sem)


# [团队元信息]
class TeamMeta(models.Model):
    minNum = models.PositiveSmallIntegerField(default=1)
    maxNum = models.PositiveSmallIntegerField(default=10)
    startTime = models.DateTimeField(blank=True, default=datetime.now(), help_text='允许组队的开始时间')
    endTime = models.DateTimeField(blank=True, default=datetime.now())

    def __str__(self):
        return '%d~%d人团队' %(self.minNum, self.maxNum)


# [课程]==[学期]&[团队元信息]
class Course(models.Model):
    term = models.ForeignKey(Term)            # 学期
    teamMeta = models.ForeignKey(TeamMeta, null=True, blank=True)    # 团队元信息
    name = models.CharField(max_length=64)
    info = models.TextField(null=True, blank=True, help_text='课程要求/其他说明')
    syllabus = models.TextField(null=True, blank=True, help_text='课程大纲')
    classroom = models.CharField(max_length=64, null=True, blank=True, help_text='上课地点')
    credit = models.PositiveSmallIntegerField(default=0)
    STATUS = (
        ('unstarted', '未开始'),
        ('ongoing', '正在进行'),
        ('ended', '已结束'),
    )
    status = models.CharField(max_length=16, choices=STATUS, default='unstarted')
    startTime = models.DateTimeField(blank=True, default=datetime.now())
    endTime = models.DateTimeField(blank=True, default=datetime.now())

    def __str__(self):
        return self.name


# <选课>==[课程]&[用户:学生/教师账户]
class Enroll(models.Model):
    course = models.ForeignKey(Course)
    user = models.ForeignKey(User)

    def __str__(self):
        return '%s <- %s' %(self.course.name, self.user.name or self.user.username)


# [团队]==[课程]&[用户:学生账户]
class Team(models.Model):
    course = models.ForeignKey(Course)
    serialNum = models.PositiveSmallIntegerField(help_text='每学期的课都能从1开始的编号') # 'id' is a reserved word...
    name = models.CharField(max_length=32, null=True, blank=True, help_text='可选的自定义名字')
    STATUS = (
        ('incomplete', '未完成组队'),
        ('unsubmitted', '未提交'),
        ('auditing', '待审核'),
        ('passed', '已通过'),
        ('rejected', '已驳回')
    )
    status = models.CharField(max_length=16, choices=STATUS, default='incomplete')
    info = models.TextField(help_text='通过欢迎信息/驳回理由', null=True, blank=True)

    def __str__(self):
        return '%d: %s' %(self.serialNum, self.name)

# <团队成员>==[团队]&[用户:学生账户]
class Member(models.Model):
    team = models.ForeignKey(Team)
    user = models.ForeignKey(User)
    ROLE = (
        ('leader', '队长'),
        ('member', '队员'),
    )
    role = models.CharField(max_length=16, choices=ROLE, default='member')
    contribution = models.FloatField(help_text='成员贡献度:0.4~1.2', null=True, blank=True)

    def __str__(self):
        return '%d: %s <- %s' %(self.team.serialNum, self.team.name or 'NoTeamName', self.user.name or self.user.username)


# [作业任务]~~<附件>
class WorkMeta(models.Model):
    course = models.ForeignKey(Course)
    user = models.ForeignKey(User, help_text='发布者:教师')
    title = models.CharField(max_length=128, help_text='作业标题')
    content = models.TextField(null=True, blank=True)
    proportion = models.FloatField(help_text='总分折算占比:0.0~1.0', null=True, blank=True)
    submits = models.SmallIntegerField(default=-1, help_text='可提交次数，默认-1为无限')
    startTime = models.DateTimeField(blank=True, default=datetime.now())
    endTime = models.DateTimeField(blank=True, default=datetime.now())

    def __str__(self):
        return self.title


# [作业提交]~~<附件>
class Work(models.Model):
    workMeta = models.ForeignKey(WorkMeta, help_text='作业任务元信息')
    team = models.ForeignKey(Team, help_text='提交者:团队')
    content = models.TextField(null=True, blank=True)
    review = models.TextField(help_text='教师简评', null=True, blank=True)
    score = models.FloatField(help_text='得分: 0.0~10.0', null=True, blank=True)
    time = models.DateTimeField(blank=True, auto_now_add=True)

    def __str__(self):
        return '%s <- %d: %s' %(self.workMeta.title, self.team.serialNum, self.team.name or 'NoTeamName')


# [资源文件]
class File(models.Model):
    course = models.ForeignKey(Course)
    user = models.ForeignKey(User, help_text='上传者')
    file = models.FileField(upload_to='file', help_text='文件实体，保存时为绝对路径(未重命名)')
    TYPE = (
        ('text', '文本'),
        ('document', '文档'),
        ('media', '视频'),
    )
    type = models.CharField(max_length=16, choices=TYPE, default='text')
    time = models.DateTimeField(blank=True, auto_now_add=True)

    def __str__(self):
        return os.path.split(self.file.url)


# <附件>==[作业任务|作业提交]&[资源文件]
class Attachment(models.Model):
    file = models.ForeignKey(File)
    workMeta = models.ForeignKey(WorkMeta, null=True)
    work = models.ForeignKey(Work, null=True)
    TYPE = (
        ('workmeta', '作业任务'),
        ('work', '作业提交'),
    )
    type = models.CharField(max_length=16, choices=TYPE, default='workmeta')

    def __str__(self):
        w = self.workMeta is not None and self.workMeta.title or self.work.workMeta.title
        return '%s <- %s' %(w, os.path.split(self.file.file.url))

# [签到]
class Attendance(models.Model):
    user = models.ForeignKey(User, help_text='学生')
    time = models.DateTimeField(blank=True, auto_now_add=True)

    def __str__(self):
        return self.user.name or self.user.username

# [公告]
class Notice(models.Model):
    course = models.ForeignKey(Course)
    user = models.ForeignKey(User, help_text='发布者')
    title = models.CharField(max_length=128)
    content = models.TextField()
    time = models.DateTimeField(blank=True, auto_now_add=True)

    def __str__(self):
        return self.title