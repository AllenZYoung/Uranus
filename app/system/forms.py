# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import SelectDateWidget,Textarea
from app import models

from django.forms import fields


# define your custom forms here

class FileForm(forms.Form):
    filefield = forms.FileField(required=True, label='请选择文件')

class TermForm(forms.Form):
    year = forms.CharField(required=True, label='学期年份', widget=forms.TextInput(attrs={'type':'number','class': 'form-control'}))
    SEMESTER_CHOICES = (
        ('spring', '春季学期'),
        ('autumn', '秋季学期'),
    )
    semester = forms.CharField(required=True, widget=forms.Select(choices=SEMESTER_CHOICES,attrs={'class': 'form-control'}), label='')
    #forms.IntegerField( required=True, label='开始周次',attrs={'class': 'form-control'},min_value=0)
    startWeek =  forms.CharField(required=True, label='开始周次',widget=forms.TextInput(attrs={'type':'number','min':'1','class':'form-control'}))
    endWeek =  forms.CharField(required=True, label='结束周次',widget=forms.TextInput(attrs={'type':'number','min':'1','class':'form-control'}))




class CourseForm(forms.Form):
    name = forms.CharField(required=True, label='课程名字', max_length=64, widget=forms.TextInput(attrs={'class': 'form-control'}))
    classroom = forms.CharField(required=True, label='教室', max_length=64, widget=forms.TextInput(attrs={'class': 'form-control'}))
    credit = forms.CharField(required=True,label='学分', widget=forms.TextInput(attrs={'class': 'form-control'}))
    startTime = forms.DateField(required=False, label='开始时间', widget=SelectDateWidget(attrs={'class':'form-control'}))
    endTime = forms.DateField(required=False, label='结束时间', widget=SelectDateWidget(attrs={'class':'form-control'}))






class EditTermForm(forms.ModelForm):
    #year = forms.CharField(required=True, label='学期年份', widget=forms.TextInput(attrs={'class': 'form-control'}))
    #semester= forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control','hidden':True}))
    #startWeek = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    #endWeek = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    def __init__(self, *args, **kwargs):
        super(EditTermForm, self).__init__(*args, **kwargs)
        self.fields['year'].widget.attrs['readonly'] = True
        self.fields['semester'].widget.attrs['readonly'] = True

    class Meta:
        model = models.Term
        fields = ['year','semester','startWeek','endWeek']
        widgets={
            'year':forms.TextInput(attrs={'type':'number','class': 'form-control'}),
            'semester':forms.TextInput(attrs={'class': 'form-control','hidden':True}),
            'startWeek':forms.TextInput(attrs={'type':'number','min':'1','class':'form-control'}),
            'endWeek':forms.TextInput(attrs={'type':'number','min':'1','class':'form-control'}),
        }


class EditCourseForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))
    classroom = forms.CharField( widget=forms.TextInput(attrs={'class': 'form-control'}))
    credit = forms.CharField(widget=forms.TextInput(attrs={'type':'number','class': 'form-control'}))
    startTime = forms.DateField(label='开始时间', widget=SelectDateWidget(attrs={'class': 'form-control'}))
    endTime = forms.DateField(label='结束时间', widget=SelectDateWidget(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(EditCourseForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.Course
        fields = ['name','term','classroom','credit','startTime','endTime']


