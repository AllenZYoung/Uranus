from django.urls import reverse
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from app.models import *
import app.teacher.views as views


# define your custom generic views here

# class CourseUpdate(UpdateView):
#     model = Course
#     fields = ['name', 'info', 'syllabus', 'classroom']
#     template_name = 'teacher/course_edit_form.html'
#
#     def get_object(self, queryset=None):
#         return get_object_or_404(Course, id=self.request.GET.get('course_id'))
#
#     def get_success_url(self):
#         return '/teacher/course_info?course_id='+self.request.GET.get('course_id')
