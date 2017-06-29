# -*- coding: utf-8 -*-
from django import forms
from datetime import datetime

# define your custom forms here
from django.forms import widgets


class UploadFileForm(forms.Form):
    file = forms.FileField(label='选择附件')


class HomeworkForm(forms.Form):
    title = forms.CharField(label='作业名称')
    content = forms.CharField(label='作业内容', widget=widgets.Textarea)
    proportion = forms.FloatField(label='总分占比', min_value=0, max_value=1)
    submits = forms.IntegerField(label='最大提交次数', min_value=1)
    endTime = forms.DateField(label='截止日期', widget=widgets.SelectDateWidget)
    attachment = forms.FileField(label='上传附件', required=False,widget=widgets.FileInput)

    def set_data(self, workmeta):
        self.fields['title'].initial = workmeta.title
        self.fields['content'].initial = workmeta.content
        self.fields['proportion'].initial = workmeta.proportion
        self.fields['submits'].initial = workmeta.submits
        self.fields['endTime'].initial = workmeta.endTime

    def __init__(self, *args, **kwargs):
        super(HomeworkForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name is not 'attachment':
                field.widget.attrs['class'] = 'form-control'


# comment and score form
class CommentAndScoreForm(forms.Form):
    # post_work_meta_id = forms.IntegerField()
    # homework_id = forms.IntegerField()
    score = forms.CharField()
    review = forms.CharField()


class EditCourseForm(forms.Form):
    name = forms.CharField(label='课程名称')
    info = forms.CharField(label='课程要求/其他说明')
    syllabus = forms.CharField(label='课程大纲', widget=forms.Textarea)
    classroom = forms.CharField(label='教室')
    STATUS = (
        ('unstarted', '未开始'),
        ('ongoing', '正在进行'),
        ('ended', '已结束'),
    )
    status = forms.ChoiceField(choices=STATUS, label='课程状态')

    def set_init_data(self, course):
        self.fields['name'].initial = course.name
        self.fields['info'].initial = course.info
        self.fields['syllabus'].initial = course.syllabus
        self.fields['classroom'].initial = course.classroom
        self.fields['status'].initial = course.status

    def __init__(self, *args, **kwargs):
        super(EditCourseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
