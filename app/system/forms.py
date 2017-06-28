# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import SelectDateWidget
from app import models


# define your custom forms here

class FileForm(forms.Form):
    filefield = forms.FileField(required=True, label='请选择文件')


class TermForm(forms.Form):
    year = forms.CharField(required=True, label='学期年份')
    SEMESTER_CHOICES = (
        ('spring', '春季学期'),
        ('autumn', '秋季学期'),
    )
    semester = forms.CharField(required=True, widget=forms.Select(choices=SEMESTER_CHOICES), label='')
    startWeek = forms.CharField(required=True, label='开始周次')
    endWeek = forms.CharField(required=True, label='结束周次')


class CourseForm(forms.Form):
    name = forms.CharField(required=True, label='课程名字', max_length=64)
    TERMS_CHOICES = []
#     terms = models.Term.objects.all()
#     if (terms):
#         for term in terms:
#             if term.semester == 'spring':
#                 TERMS_CHOICES.append((term.id, str(term.year) + ' ' + '春季学期'))
#             else:
#                 TERMS_CHOICES.append((term.id, str(term.year) + ' ' + '秋季学期'))
#         term = forms.CharField(required=True, widget=forms.Select(choices=TERMS_CHOICES))
#     classroom = forms.CharField(required=True, label='教室', max_length=64)
#     credit = forms.IntegerField(required=True, label='学分')
#     startTime = forms.DateTimeField(required=False, label='开始时间', widget=SelectDateWidget)
#     endTime = forms.DateTimeField(required=False, label='结束时间', widget=SelectDateWidget)

class EditTermForm(forms.Form):
    name = ' '

class EditCourseForm(forms.Form):
    name = ''