from django.shortcuts import render
from django.http import HttpResponse
from app.system.forms  import FileForm
from app.system.utils import handle_uploaded_user
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def index(request):
    return render(request,'system/systemIndex.html')

def upload_students(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES['filefield'].name.split('.')[-1] == 'xlsx':
                try:
                    handle_uploaded_user(request,f=request.FILES['filefield'],user_role='student')
                except ObjectDoesNotExist as e:
                    error_message =""
                    return HttpResponse('error')
                return HttpResponse('success')
            else:
                error_message = '文件格式错误，请上传Excel文件（.xlsl)'
                form = FileForm()
                return HttpResponse("文件格式错误，请上传Excel文件")

        else:
            error_message = '请添加文件'
            form = FileForm()
            return render(request,'system/uploadStudents.html')
    return render(request,'system/uploadStudents.html')

def upload_teachers(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES['filefield'].name.split('.')[-1] == 'xlsx':
                try:
                    handle_uploaded_user(request,f=request.FILES['filefield'],user_role='teacher')
                except ObjectDoesNotExist as e:
                    error_message =""
                    return HttpResponse('error')
                return HttpResponse('success')
            else:
                error_message = '文件格式错误，请上传Excel文件（.xlsl)'
                form = FileForm()
                return HttpResponse("文件格式错误，请上传Excel文件")

        else:
            error_message = '请添加文件'
            form = FileForm()
            return render(request,'system/uploadTeachers.html')
    return render(request,'system/uploadTeachers.html')