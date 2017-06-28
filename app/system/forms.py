# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import SelectDateWidget,Textarea
from app import models

from django.forms import fields


# define your custom forms here

class FileForm(forms.Form):
    # filefield = forms.FileField(required=True, label='请选择文件')
    pass


class TermForm(forms.Form):
    # year = forms.CharField(required=True, label='学期年份')
    # SEMESTER_CHOICES = (
    #     ('spring', '春季学期'),
    #     ('autumn', '秋季学期'),
    # )
    # semester = forms.CharField(required=True, widget=forms.Select(choices=SEMESTER_CHOICES), label='')
    # startWeek = forms.CharField(required=True, label='开始周次')
    # endWeek = forms.CharField(required=True, label='结束周次')
    pass


class CourseForm(forms.Form):
    name = forms.CharField(required=True, label='课程名字', max_length=64)
    classroom = forms.CharField(required=True, label='教室', max_length=64)
    credit = forms.IntegerField(required=True, label='学分')
    startTime = forms.DateTimeField(required=False, label='开始时间', widget=SelectDateWidget)
    endTime = forms.DateTimeField(required=False, label='结束时间', widget=SelectDateWidget)






class EditTermForm(forms.ModelForm):
    startWeek = forms.CharField(label='课程开始周次')
    info = forms.CharField(label='说明信息',required=False)
    def __init__(self, *args, **kwargs):
        super(EditTermForm, self).__init__(*args, **kwargs)
        self.fields['year'].widget.attrs['readonly'] = True
        self.fields['semester'].widget.attrs['readonly'] = True
        self.fields['startWeek'].is_hiden= True
        self.fields['endWeek'].label='课程结束周次'



    class Meta:
        model = models.Term
        fields = ['year','semester','startWeek','endWeek','info']
        widgets = {
            'semester': forms.TextInput(),
            'startWeek':forms.TextInput(),
        }


class EditCourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditCourseForm, self).__init__(*args, **kwargs)
    class Meta:
        model = models.Course
        fields = ['name','term','classroom','credit','status','startTime','endTime']
