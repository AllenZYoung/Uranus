# -*- coding: utf-8 -*-
from django import forms


# define your custom forms here
class UploadFileForm(forms.Form):
    file = forms.FileField(label='选择附件')


class HomeworkForm(forms.Form):
    content = forms.CharField(label='作业内容')
    proportion = forms.FloatField(label='总分占比', min_value=0, max_value=1)
    submits = forms.IntegerField(label='最大提交次数', min_value=1)
    startTime = forms.DateTimeField(label='开始日期')
    endTime = forms.DateTimeField(label='截止日期')
    attachment = forms.FileField(label='上传附件', required=False)

    def __init__(self, content, proportion, submits, startTime, endTime):
        super().__init__()
        self.content = content
        self.proportion = proportion
        self.submits = submits
        self.startTime = startTime
        self.endTime = endTime


# comment and score form
class CommentAndScoreForm(forms.Form):
    homework_id = forms.CharField()
    score = forms.IntegerField(help_text='score')
    comment = forms.CharField(help_text='comment')
