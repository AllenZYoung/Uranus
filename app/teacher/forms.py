# -*- coding: utf-8 -*-
from django import forms


# define your custom forms here
class UploadFileForm(forms.Form):
    file = forms.FileField()


#comment and score form
class CommentAndScoreForm(forms.Form):
    homework_id = forms.CharField()
    score = forms.IntegerField(help_text='score')
    comment = forms.CharField(help_text='comment')

