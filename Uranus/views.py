from django.http import HttpResponse
from django.shortcuts import render
from app.test.sampleDB import sampleDB


def index(request):
    return HttpResponse('Uranus Project')


# Added by kahsolt
def sampleDBView(request):
    sampleDB()
    return render(request, 'test/sampleDB.html')