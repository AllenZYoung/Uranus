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
        self.fields['title'].initial = workmeta.title
        self.fields['content'].initial=workmeta.content
        self.fields['proportion'].initial = workmeta.proportion
        self.fields['submits'].initial = workmeta.submits
        self.fields['startTime'].initial= workmeta.startTime
        self.fields['endTime'].initial = workmeta.endTime



# comment and score form
class CommentAndScoreForm(forms.Form):
    homework_id = forms.CharField()
    score = forms.IntegerField()
    review = forms.CharField()
