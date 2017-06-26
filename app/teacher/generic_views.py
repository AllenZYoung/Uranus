from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from app.models import *


# define your custom generic views here

class CourseUpdate(UpdateView):
    model = Course
    fields = ['name', 'info', 'syllabus', 'classroom']
    template_name_suffix = '_edit_form'

    def get_object(self, queryset=None):
        return get_object_or_404(Course, pk=self.request.GET.get('pk'))
