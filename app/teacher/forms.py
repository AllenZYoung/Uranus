# -*- coding: utf-8 -*-
from django import forms
from datetime import datetime


# define your custom forms here
from django.forms import widgets


class UploadFileForm(forms.Form):
    file = forms.FileField(label='选择附件')


class HomeworkForm(forms.Form):
    title = forms.CharField(label='作业名称')
    content = forms.CharField(label='作业内容',widget=widgets.Textarea)
    proportion = forms.FloatField(label='总分占比', min_value=0, max_value=1)
    submits = forms.IntegerField(label='最大提交次数', min_value=1)
    startTime = forms.DateField(label='开始日期',widget=widgets.SelectDateWidget)
    endTime = forms.DateField(label='截止日期',widget=widgets.SelectDateWidget)
    attachment = forms.FileField(label='上传附件', required=False)


    def set_data(self,workmeta):
        self.content = workmeta.content
        self.proportion = workmeta.proportion
        self.submits = workmeta.submits
        self.startTime = workmeta.startTime
        self.endTime = workmeta.endTime
    # def __init__(self, content='', proportion=0.1, submits=3, startTime=datetime.now(), endTime=datetime.now()):
    #     super().__init__()
    #     self.content = content
    #     self.proportion = proportion
    #     self.submits = submits
    #     self.startTime = startTime
    #     self.endTime = endTime


# comment and score form
class CommentAndScoreForm(forms.Form):
    homework_id = forms.CharField()
    score = forms.IntegerField(help_text='score')
    comment = forms.CharField(help_text='comment')
