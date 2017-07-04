from django.contrib.auth.decorators import login_requiredfrom django.shortcuts import render, HttpResponseRedirect,render_to_responsefrom django.http import HttpResponse from app.system.forms  import FileForm,TermForm,CourseForm,EditTermFormfrom app.system.utils import handle_uploaded_userfrom django.core.exceptions import ObjectDoesNotExistfrom  app import modelsfrom  app.utils.fileUtils import fileDownloadUrlfrom app.utils.rootsUtils import UPLOAD_ROOTfrom datetime import datetimefrom app.utils import logimport jsonimport os# Create your views here.@login_required(login_url='app:login')def index(request):    return render(request,'system/admin_term.html')@login_required(login_url='app:login')def index_course(request):    return render(request,'system/admin_course.html')@login_required(login_url='app:login')def upload_students(request):    if request.method == 'POST':        data = {}        form = FileForm(request.POST, request.FILES)        if form.is_valid():            if request.FILES['filefield'].name.split('.')[-1] == 'xlsx':                try:                    handle_uploaded_user(request,course_id=request.POST['courseId'],f=request.FILES['filefield'],user_role='student')                except ObjectDoesNotExist as e:                    data['error_message'] = '上传失败'                    return HttpResponse(json.dumps(data))                data['success'] = 'true'                data['forward_url'] = 'showStudents?id=' + request.POST['courseId']                return HttpResponse(json.dumps(data))            else:                data['error_message'] = '文件格式错误，请上传Excel文件'                return HttpResponse(json.dumps(data))        else:            data['error_message'] = '文件出错，请重新上传！'            return HttpResponse(json.dumps(data))    return HttpResponseRedirect('loadStudents')@login_required(login_url='app:login')def upload_teachers(request):    if request.method == 'POST':        data = {}        form = FileForm(request.POST, request.FILES)        if form.is_valid():            if request.FILES['filefield'].name.split('.')[-1] == 'xlsx':                try:                    handle_uploaded_user(request,course_id=request.POST['courseId'],f=request.FILES['filefield'],user_role='teacher')                except ObjectDoesNotExist as e:                    data['error_message'] = "上传失败"                except Exception as e:                    data['error_message'] = "文件内容格式不对，请重新上传！"                    return HttpResponse(json.dumps(data))                    # return HttpResponseRedirect('loadTeacher' + '?message=' + error_message)                data['success'] = 'true'                data['forward_url'] = "showTeachers?id=" + request.POST.get('courseId')                # return HttpResponseRedirect('loadTeacher'+'?message=sucess')            else:                data['error_message'] = '文件格式错误，请上传Excel文件（.xlsl)'                # return HttpResponseRedirect('loadTeacher' + '?message='+error_message)        else:            data['error_message'] = '文件出错，请重新上传！'        return HttpResponse(json.dumps(data))            # error_message = '请添加文件'            # form = FileForm()            # return HttpResponseRedirect('loadTeacher' + '?message=' + error_message)    return HttpResponseRedirect('loadTeacher')@login_required(login_url='app:login')def create_term(request):    if request.method == "POST":        form = TermForm(request.POST)        data = {}        if form.is_valid():            year = form.cleaned_data['year']            semester = form.cleaned_data['semester']            term_exists = models.Term.objects.filter(year=year, semester=semester)            if (term_exists):                form = TermForm()                data['error_message'] = '学期已存在'                # return  render(request,'system/admin_create_term.html',{'form':form,'errorMessage':error_message})            else:                models.Term.objects.create(year=year,semester=semester,startWeek=form.cleaned_data['startWeek'],endWeek=form.cleaned_data['endWeek'])                data['success'] = 'true'        else:            data['error_message'] = '数据不合法，请重新填写！'            # form = TermForm()            # return render(request, 'system/admin_create_term.html', {'form': form})        return HttpResponse(json.dumps(data))    else:        form = TermForm()        return render(request,'system/admin_create_term.html',{'form':form})@login_required(login_url='app:login')def create_course(request):    if request.method == "POST":        form = CourseForm(request.POST)        data = {}        if form.is_valid():            name = form.cleaned_data['name']            term_id = request.POST['term']            course_exists = models.Course.objects.filter(term=term_id)            startDate = form.cleaned_data['startTime']            endDate = form.cleaned_data['endTime']            print(startDate)            print(endDate)            startTime = datetime.strptime(startDate, '%Y-%m-%d')            endTime = datetime.strptime(endDate,'%Y-%m-%d')            print(startTime.date())            print(endTime.date())            if (course_exists):                data['error_message'] = '该学期课程存在'                # return render(request,'system/admin_create_course.html',{'errorMessage':error_message})            else:                if  endDate  < startDate:                    data['error_message'] = '结束时间不能早于开始时间'                    # return render(request, 'system/admin_create_course.html', {'errorMessage': error_message})                else:                    today_date = datetime.now().date()                    if today_date < startTime.date():                        status = 'unstarted'                    elif startTime.date() <= today_date and today_date <= endTime.date():                        status = 'ongoing'                    else:                        status = 'ended'                    models.Course.objects.create(                        name=name,                        term= models.Term.objects.get(id=term_id),                        classroom=form.cleaned_data['classroom'],                        credit=form.cleaned_data['credit'],                        status=status,                        startTime=form.cleaned_data['startTime'],                        endTime=form.cleaned_data['endTime'],                        #teamMeta=models.TeamMeta.objects.create()                    )                    data['success'] = 'true'                    data['forward_url'] = 'showCourse'                # return HttpResponseRedirect('/system/course'+'?message=success')        else:            # form = CourseForm()            data['error_message'] = '数据不合法，请重新填写！'            # return HttpResponseRedirect('/system/createCourse'+'?message='+error_message)        return HttpResponse(json.dumps(data))    else:        terms = models.Term.objects.all()        if(terms):            form = CourseForm()            return render(request, 'system/admin_create_course.html', {'form': form,'terms':terms})        else:            return HttpResponseRedirect('/system/createTerm')@login_required(login_url='app:login')def edit_term(request):    if request.method == 'POST':        data = {}        terms = models.Term.objects.get(id=request.POST['termId'])        form = EditTermForm(request.POST,instance=terms)        if form.is_valid():            data['success'] = 'true'            form.save()            # return HttpResponseRedirect('/system/editTerm?id='+request.POST['termId']+'&&message=success')        else:            data['error_message'] = '数据不合法，请重修填写！'            # terms = models.Term.objects.get(id=request.POST['termId'])            # form = EditTermForm(instance=terms)            # return render(request,'system/admin_edit_term.html',{'form':form})        return HttpResponse(json.dumps(data))    else:        terms = models.Term.objects.get(id=request.GET['id'])        #request.session['term']=terms        form = EditTermForm(instance=terms)        return render(request, 'system/admin_edit_term.html', {'form': form,'termId':request.GET['id']})@login_required(login_url='app:login')def edit_course(request):    if request.method == 'POST':        data = {}        course = models.Course.objects.get(id=request.POST['courseId'])        credit = request.POST.get('credit',None)        print(credit)        classroom = request.POST.get('classroom',default=None)        print(classroom)        startDate = request.POST.get('startTime',default=None)        print(startDate)        endDate = request.POST.get('endTime',default=None)        print(endDate)        if (  credit == None or classroom == None or startDate == None or endDate == None):            data['error_message'] = '数据不能为空，请重修填写！'        else:            try :                startTime = datetime.strptime(startDate, '%Y-%m-%d')                endTime = datetime.strptime(endDate, '%Y-%m-%d')                if  endDate  < startDate:                    data['error_message'] = '结束时间不能早于开始时间'                    # return render(request, 'system/admin_create_course.html', {'errorMessage': error_message})                else:                    today_date = datetime.now().date()                    if today_date < startTime.date():                        status = 'unstarted'                    elif startTime.date() <= today_date and today_date <= endTime.date():                        status = 'ongoing'                    else:                        status = 'ended'                    course.credit = credit                    course.classroom = classroom                    course.startTime = startTime                    course.endTime = endTime                    course.save()                    data['success'] = 'true'                    data['forward_url'] = 'showCourse'            except Exception as e:                data['error_message'] = '数据不合法，请重修填写！'        return HttpResponse(json.dumps(data))    else:        course = models.Course.objects.get(id=request.GET['id'])        term = course.term        return render(request, 'system/admin_edit_course.html', {'courseInfo': course,'courseId':request.GET['id'],'termInfo':term,})@login_required(login_url='app:login')def show_term(request):    terms = models.Term.objects.all()    return render(request,'system/admin_term_info.html', {'terms':terms})@login_required(login_url='app:login')def show_course(request):    courses = models.Course.objects.all()    info = list()    for course in courses:        enrolls = models.Enroll.objects.filter(course=course)        flag = False        for enroll in enrolls:            if enroll.user.role == 'student':                flag = True        course_dic = {'course':course, 'flag':flag}        info.append(course_dic)    return render(request,'system/admin_course_info.html', {'info':info})@login_required(login_url='app:login')def load_student(request):    courses = models.Course.objects.all()    info = list()    for course in courses:        enrolls = models.Enroll.objects.filter(course=course)        flag = False        for enroll in enrolls:            if enroll.user.role == 'student':                flag = True        course_dic = {'course': course, 'flag': flag}        info.append(course_dic)    form = FileForm()    url = fileDownloadUrl(os.path.join(os.path.basename(UPLOAD_ROOT),'学生.xlsx'))    return render(request, 'system/load_student.html', {'info': info, 'form': form,'url':url})@login_required(login_url='app:login')def load_teacher(request):    courses = models.Course.objects.all()    info = list()    for course in courses:        enrolls = models.Enroll.objects.filter(course=course)        flag = False        for enroll in enrolls:            if enroll.user.role == 'teacher':                flag = True        course_dic = {'course': course, 'flag': flag}        info.append(course_dic)    form = FileForm()    url = fileDownloadUrl(os.path.join(os.path.basename(UPLOAD_ROOT), '教师.xlsx'))    return render(request, 'system/load_teacher.html', {'info': info, 'form': form,'url':url})@login_required(login_url='app:login')def show_the_students(request):    course_id = request.GET['id']    enrolls = models.Enroll.objects.filter(course=course_id)    user_list = []    course = None    isReloadable = False    firstLoad = True    for enroll in enrolls:        if enroll.user.role == 'student':            user_list.append(enroll.user)    if (enrolls):        firstLoad = False        course = enrolls[0].course        if course.status == 'unstarted':            isReloadable = True    form = FileForm()    url = fileDownloadUrl(os.path.join(os.path.basename(UPLOAD_ROOT), '学生.xlsx'))    return render(request,'system/student_detail.html',{'enrolls':user_list,'isReloadable':isReloadable,'form':form,'courseId':course_id,'firstLoad':firstLoad,'url':url})@login_required(login_url='app:login')def show_the_teachers(request):    course_id = request.GET['id']    enrolls = models.Enroll.objects.filter(course=course_id)    user_list = []    course = None    isReloadable = False    firstLoad = True    for enroll in enrolls:        if enroll.user.role == 'teacher':            user_list.append(enroll.user)    if (enrolls):        firstLoad = False        course = enrolls[0].course        if course.status == 'unstarted':            isReloadable = True    form = FileForm()    url = fileDownloadUrl(os.path.join(os.path.basename(UPLOAD_ROOT), '教师.xlsx'))    return render(request, 'system/teacher_detail.html', {'enrolls':user_list,'isReloadable':isReloadable,'form':form,'courseId':course_id,'firstLoad':firstLoad,'url':url})