from asyncio.windows_events import NULL
from email.errors import MessageError
import tempfile
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import *
from django.contrib import auth, messages
from Education_Master import settings

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from .forms import *
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from . token import generate_token
from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .mailserver import send_mail_to_user

# Create your views here.

# ------------------------------------------------Authentication Section------------------------------------------------
def register(request):
    if request.method =="POST":
        
        firstname= request.POST.get('fname','')
        lastname= request.POST.get('lname','')
        email= request.POST.get('email','')
        username= request.POST.get('uname','')
        password= request.POST.get('password','')
        cpassword= request.POST.get('cpassword','')
        user_DOB= request.POST.get('user_DOB','')
        user_phone= request.POST.get('user_phone','')

        if User.objects.filter(username = username):
            messages.error(request," Username is already exist !")

        elif len(username)>20:
            messages.error(request, " Username must be under 20 charcters!!")
            
        elif User.objects.filter(email = email):
            messages.error(request," Email is already exist !")
        
        elif password == cpassword:

            UserAccount = User.objects.create_user(username,email,password)
            UserAccount.first_name = firstname
            UserAccount.last_name = lastname
            UserAccount.user_DOB = user_DOB
            UserAccount.user_phone = user_phone
            UserAccount.is_active = False
            UserAccount.Registered_As = 'None'
            UserAccount.save()
            
            # Send an Email to User For successfully Registration
            subject = "Welcome to Education_Master"
            message = "Welcome to Education_Master!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address."
            # form_email = settings.EMAIL_HOST_USER
            user_name = UserAccount.first_name
            to_email = [UserAccount.email]
            messages.success(request," Your Account has been created succesfully!! Please check your email to get all information !")
            send_mail_to_user(subject,message,to_email,user_name)
            return redirect('loginpage')
        
        else:
            messages.error(request," Password and confirm password doesn't matched !")


    return render(request,'Edu_Master/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.Registered_As=='Admin' or user.is_superuser:
                return redirect('admin_dashboard1')
            elif user.Registered_As =='Student':
                return redirect('home')		
            elif user.Registered_As =='LibraryAdmin':
                return redirect('librarian_dashboard')
            	
            elif user.Registered_As =='Teacher':
                return redirect('teacher_dashboard')
            	
            else:
                messages.error(request, " Invalid username or password !")
                return redirect('login')
        else:
            messages.error(request, " Invalid username or passwords !")

    return render(request,'Edu_Master/login.html')

def LoginWithOTP(request):
    return render(request,'Edu_Master/LoginWithOTP.html')

@login_required(login_url='/loginpage/')
def LogOut(request):
    logout(request)
    return redirect("login")

def forgotpass(request):
    return render(request,'Edu_Master/forgotpass.html')
# ------------------------------------------------Student Section------------------------------------------------
@login_required(login_url='/loginpage/')
def home(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    HighRatedCourse = Course_Detail.objects.filter(Course_Rating__gte=4.5)[:5]
    contextItem = {'userprofile':userprofile,'HighRatedCourse':HighRatedCourse}
    return render(request,'Edu_Master/Index.html',contextItem)

@login_required(login_url='/loginpage/')
def student_search(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    if request.method == "POST":
        text_str = request.POST['search_keyword']        
        searched_course = Course_Detail.objects.filter(Course_Name__contains = text_str)
        searched_event = Events.objects.filter(Event_Name__contains = text_str)

        if searched_course:
            context = {'userprofile':userprofile,'searched_course':searched_course}
        elif searched_event:
            #print(searched_event)
            context = {'userprofile':userprofile,'searched_event':searched_event}
        else:
            context = {'userprofile':userprofile,'text_str':text_str}
        
    return render(request,'Edu_Master/student_search.html',context)

@login_required(login_url='/loginpage/')
def student_dashboard(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    contextItem = {'userprofile':userprofile,'item':userprofile}
    #print(userprofile)
    return render(request,'Edu_Master/student_dashboard.html',contextItem)

@login_required(login_url='/loginpage/')
def student_profile(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    contextItem = {'userprofile':userprofile,'item':userprofile}
    #print(userprofile)
    return render(request,'Edu_Master/student_profile.html',contextItem)

@login_required(login_url='/loginpage/')
def student_course(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    # AllCourse = Course_Detail.objects.all()
    contextItem = {'userprofile':userprofile,'item':userprofile}
    return render(request,'Edu_Master/student_course.html',contextItem)

@login_required(login_url='/loginpage/')
def student_exam(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    contextItem = {'userprofile':userprofile,'item':userprofile}
    # #print(userprofile)
    return render(request,'Edu_Master/student_exam.html',contextItem)

@login_required(login_url='/loginpage/')
def student_class_time(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    contextItem = {'userprofile':userprofile,'item':userprofile}
    #print(userprofile)
    return render(request,'Edu_Master/student_class_time.html',contextItem)

@login_required(login_url='/loginpage/')
def student_Profile_Edit(request,pk):
    AllContext = []
    cuser = request.user    
    item = Student_Profile.objects.filter(Student_User_PK=cuser)[0]            
    requested_userID = Student_Profile.objects.get(pk=pk)
    form = User_Profile_Edit(instance=requested_userID)
    if request.method == 'POST':        
        form = User_Profile_Edit(request.POST, request.FILES,instance = requested_userID)
        if form.is_valid():
            form.save() 
            messages.success(request," Your personal details is updated successfully !")
        return redirect('student_dashboard')               
    AllContext.append([item,form])  
    context = {'AllContext':AllContext,'userprofile':item}
    return render(request,'Edu_Master/student_Profile_Edit.html',context)

@login_required(login_url='/loginpage/')
def about(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    return render(request,'Edu_Master/about.html',context)

@login_required(login_url='/loginpage/')
def award(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    return render(request,'Edu_Master/award.html',context)

@login_required(login_url='/loginpage/')
def research(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    return render(request,'Edu_Master/research.html',context)

@login_required(login_url='/loginpage/')
def facilities(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    return render(request,'Edu_Master/facilities.html',context)
   
@login_required(login_url='/loginpage/')
def facilities_detail(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    return render(request,'Edu_Master/facilities_detail.html',context)

@login_required(login_url='/loginpage/')
def departments(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    return render(request,'Edu_Master/departments.html',context)

@login_required(login_url='/loginpage/')
def all_course(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    allcourse = Course_Detail.objects.all().order_by('Course_ID')
    paginator = Paginator(allcourse, 2)  # 6 Course in each page
    page = request.GET.get('page')
    try:
        course_list = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        course_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        course_list = paginator.page(paginator.num_pages)


    context = {'userprofile':userprofile,'course_list':course_list,'page':page}
    return render(request,'Edu_Master/all_course.html',context)

@login_required(login_url='/loginpage/')
def seminar(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    return render(request,'Edu_Master/seminar.html',context)

@login_required(login_url='/loginpage/')
def course_details(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    return render(request,'Edu_Master/course_details.html',context)

@login_required(login_url='/loginpage/')
def blog(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    return render(request,'Edu_Master/blog.html',context)

@login_required(login_url='/loginpage/')
def blog_details(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    return render(request,'Edu_Master/blog_details.html',context)

@login_required(login_url='/loginpage/')
def event(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    event_obj = Events.objects.all().order_by('Event_ID')
    paginator = Paginator(event_obj, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)

    context = {'userprofile':userprofile,'page':page,'post_list':post_list}
    return render(request,'Edu_Master/event.html',context)

@login_required(login_url='/loginpage/')
def event_details(request,pk):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = Events.objects.filter(Event_ID = pk)[0]
    #print(context)
    contextDict = {'item':context,'userprofile':userprofile}
    return render(request,'Edu_Master/event_details.html',contextDict)

@login_required(login_url='/loginpage/')
def event_register(request,slug):
    item = Events.objects.filter(Event_ID = slug)[0]    
    AllContext = []
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    #print(userprofile)
    
    AllContext.append([item,userprofile])
    contextDict = {'AllContext':AllContext,'userprofile':userprofile}
    now = datetime.now()
    dt_string = now.strftime("YYYY-MM-DD HH:MM")

    if request.method =="POST":
        Student_pk = Student_Profile.objects.get(Student_User_PK=cuser)
        Eventid = Events.objects.get(Event_ID = slug)        
        if Event_Register.objects.filter(Student_PK = Student_pk,Event_ID = Eventid).exists():
            messages.error(request," You have already registered in this events !")
        else:
            register_result = Event_Register()
            register_result.save()
            register_result.Event_ID.add(Eventid)
            register_result.Student_PK.add(Student_pk)
            userpk = register_result.pk
            
            obj = Event_Register.objects.get(pk = userpk)
            obj.Registration_Date = dt_string
            obj.save()
            messages.success(request," You have successfully registered for this events.")
            return redirect('event')
    
    return render(request,'Edu_Master/event_register.html',contextDict)

@login_required(login_url='/loginpage/')
def all_trainer(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    objAllTrainer = Teacher_Profile.objects.all()
    context = {'userprofile':userprofile,'objAllTrainer':objAllTrainer}
    return render(request,'Edu_Master/all_trainer.html',context)

@login_required(login_url='/loginpage/')
def contact_us(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    if request.method == "POST":
        c_name= request.POST.get('Contact_Name','')
        c_email= request.POST.get('Contact_Email','')
        print(c_name)
        print(c_email)
        c_message= request.POST.get('Contact_Message','')
        contactus = Contact_us(Contact_Name=c_name,Contact_Email=c_email,Contact_Message=c_message)
        
        contactus.save()
        messages.success(request," Your message is send successfully !")

    return render(request,'Edu_Master/contact_us.html',context)

# ------------------------------------------------Digital Library------------------------------------------------
@login_required(login_url='/loginpage/')
def Library_Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_obj = Student_Library_Profile.objects.filter(Library_user_ID=username,Library_Password=password)
        # user_name = Student_Library_Profile.objects.filter(Library_user_ID=username)
        if user_obj.exists():
            user_status = Student_Library_Profile.objects.filter(Library_user_ID=username).values('Student_Status')[0]['Student_Status']
            if user_status == 'Active': 
                if str(password) == 'Education_Master@123':
                    return redirect('Library_ChangePassword')
                else:
                    return redirect('Library_Index')
            else:
                messages.error(request," Your account is not activated yet !")
                
        # elif user_name.exists != True:
        #     messages.error(request,"No such account found. Register to access library !")
        #     return redirect('Library_Signup')
        else:
            messages.error(request," Your userid or password is wrong !")

    return render(request,'Edu_Master/Library_Login.html')

@login_required(login_url='/loginpage/')
def Library_Signup(request):
    cuser = request.user          
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    if request.method == "POST":
        Student_pk = Student_Profile.objects.get(Student_User_PK=cuser)
        user_name = Student_Profile.objects.filter(Student_User_PK=cuser).values('Student_Name')[0]['Student_Name']      
        u_name = user_name.split()[0]
        if Student_Library_Profile.objects.filter(Library_User_Profile = Student_pk).exists():
            messages.error(request," You have already registered for the library !")
        else:            
            user_status = 'Inactive'
            user_id = "Education_Master_" + str(u_name)
            user_pass = "Education_Master@123"
            result = Student_Library_Profile(Library_User_Profile=Student_pk,Student_Status=user_status,Library_user_ID=user_id,Library_Password=user_pass)
            result.save()

            # Send an Email to User For successfully Registration
            subject = "Education_Master Library Registration"
            message = "Hello " + Student_pk.Student_Name + "!! \n" + "Welcome to Education_Master Library!! You will get your login credentials very soon ! \nThank you for visiting our website\n.  \n\nThanking You\nTeam Education_Master"
            form_email = settings.EMAIL_HOST_USER
            to_email = [Student_pk.Student_Email]
            # send_mail(subject,message,form_email,to_email,fail_silently=True)
            messages.success(request," You have registered successfully for library. You will get all details in your registered email shortly !")
            return redirect('Library_Login')        
    return render(request,'Edu_Master/Library_Signup.html',context)

@login_required(login_url='/loginpage/')
def Library_ForgotPassword(request):
    return render(request,'Edu_Master/Library_ForgotPassword.html')

@login_required(login_url='/loginpage/')
def Library_ChangePassword(request):
    cuser = request.user
    Student_pk = Student_Profile.objects.get(Student_User_PK=cuser)
    # user_name = Student_Library_Profile.objects.filter(Library_User_Profile=Student_pk).values('Library_user_ID')[0]['Library_user_ID']
    if request.method == "POST":
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            user_obj = Student_Library_Profile.objects.filter(Library_User_Profile=Student_pk).update(Library_Password = password)
            messages.success(request," Your library password is changed successfully !")
            return redirect('Library_Index')
        else:
            messages.error(request," Password and confirm password dosn't matched !")
    return render(request,'Edu_Master/Library_ChangePassword.html')

@login_required(login_url='/loginpage/')
def search_book(request):
    if request.method == "POST":
        book_keyword = request.POST['book_keyword']
        book_objs = Books.objects.filter(Book_Title__contains = book_keyword)
        #print(book_objs)
        context = {'book_objs':book_objs}
    return render(request,'Library/search_book.html',context)

class Library_Index(LoginRequiredMixin,ListView):
    model = Books
    template_name = 'Library/index2.html'
    extra_context={'range': range(1,5)}

class Library_Book_Media(LoginRequiredMixin,ListView):
	model = Books
	template_name = 'Library/books-media.html'
	paginate_by = 3

	def get_queryset(self):
		return Books.objects.all().order_by('Book_Id')

@login_required(login_url='/loginpage/')  
def Library_News_Event(request):
    return render(request,'Library/news-event.html')

@login_required(login_url='/loginpage/')  
def Library_Blog(request):
    return render(request,'Library/blog.html')

@login_required(login_url='/loginpage/')  
def Library_Blog_Detail(request):
    return render(request,'Library/news-event.html')

@login_required(login_url='/loginpage/')
def Library_Services(request):
    return render(request,'Library/services.html')

@login_required(login_url='/loginpage/')
def Library_Book_Request(request):
    cuser = request.user
    if request.method =="POST":
        Book_Request_Name = request.POST['Book_Name'] 
        Book_Request_Author = request.POST['Book_author'] 
        Book_Request_ISBN = request.POST['Book_ISBN']
        Book_Request_Date = datetime.now().strftime("YYYY-MM-DD")
        Student_pk = Student_Profile.objects.get(Student_User_PK=cuser)
        result = Book_Request(Book_Request_Name=Book_Request_Name,Book_Request_Author=Book_Request_Author,Book_Request_ISBN=Book_Request_ISBN,Book_Request_Date=Book_Request_Date,Book_Request_By=Student_pk)
        result.save()                
        subject = "Education_Master Library Book Request"
        message = "Your book request is sending successfully ! We will upload that book soon !"
        email_messege = render_to_string('Library/email_format.html',
        {
       
            'message':message,
            'name':Student_pk.Student_Name
        })
        
        form_email = settings.EMAIL_HOST_USER
        print(form_email)
        
        to_email = [Student_pk.Student_Email]
        # send_mail(subject,email_messege,form_email,to_email,fail_silently=True)
        messages.success(request," Your book request is sended successfully !")
        return redirect('Library_Index')

    return render(request,'Library/Library_Book_Request.html')

class Library_Single_Book(LoginRequiredMixin,DetailView):
    model = Books
    template_name = 'Library/Library_Single_Book.html'


# def Library_Audio_Book(request,pk):
#     Total_Page = Books.objects.filter(Book_Id = pk).values('Book_Length')[0]['Book_Length']
#     Start_Page = Books.objects.filter(Book_Id = pk).values('Audio_Start_Page')[0]['Audio_Start_Page']
#     Book_Pdf = Books.objects.filter(Book_Id = pk).values('Book_Pdf')[0]['Book_Pdf']
    
#     First_path = ('E:\\python project\\Edustation\\Edustation\\media\\')
#     Book_Pdf = Book_Pdf.replace('/','\\')
#     BookPath =  ("".join([First_path,Book_Pdf]))
#     #print(BookPath)
#     #print(Total_Page)
#     #print(type(Total_Page))
#     #print(Start_Page)
#     #print(type(Start_Page))
#     AudioBook = Audio_Book.audiobook(BookPath,Total_Page,Start_Page)
#     return render(request,'User/AudioBook.html',{'AudioBook':AudioBook})


#------------------------------------------------Admin Section------------------------------------------------
@login_required(login_url='/loginpage/')
def admin_dashboard1(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    # --------================ Paging for Student ================--------
    allstudent_list = Student_Profile.objects.all()
    paginator1 = Paginator(allstudent_list, 1)  # 3 Student in each page
    page = request.GET.get('page1')
    try:
        allstudent_obj = paginator1.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        allstudent_obj = paginator1.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        allstudent_obj = paginator1.page(paginator1.num_pages)

    # --------================ Paging for Teacher ================--------
    allteacher_list = Teacher_Profile.objects.all()
    paginator2 = Paginator(allteacher_list, 1)  # 3 Student in each page
    page = request.GET.get('page2')
    try:
        allteacher_obj = paginator2.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        allteacher_obj = paginator2.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        allteacher_obj = paginator2.page(paginator2.num_pages)

    # --------================ Paging for Librarian ================--------
    all_librarian_list = Librarian_Profile.objects.all()
    paginator3 = Paginator(all_librarian_list, 1)  # 3 Student in each page
    page = request.GET.get('page3')
    try:
        all_librarian_obj = paginator3.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        all_librarian_obj = paginator3.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        all_librarian_obj = paginator3.page(paginator3.num_pages)

    # --------================ Paging for Course ================--------
    allcourse_list = Course_Detail.objects.all()
    paginator4 = Paginator(allcourse_list, 3)  # 3 Course in each page
    page = request.GET.get('page4')
    try:
        allcourse_obj = paginator4.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        allcourse_obj = paginator4.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        allcourse_obj = paginator4.page(paginator4.num_pages)

    # --------================ Paging for Events ================--------
    allevents_list = Events.objects.all()
    paginator5 = Paginator(allevents_list, 3)  # 6 Course in each page
    page5 = request.GET.get('page5')
    try:
        allevents_obj = paginator5.page(page5)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        allevents_obj = paginator5.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        allevents_obj = paginator5.page(paginator5.num_pages)
    
    NoOfCourses = Course_Detail.objects.count()
    NoOfStudents = Student_Profile.objects.count()
    NoOfEvents = Event_Register.objects.count()
    NoOfTeachers = Teacher_Profile.objects.count()
    context = {'userprofile':userprofile,'allstudent_obj':allstudent_obj,'allcourse_obj':allcourse_obj,
    'allteacher_obj':allteacher_obj,'all_librarian_obj':all_librarian_obj,'allevents_obj':allevents_obj,
    'NoOfCourses':NoOfCourses,'NoOfStudents':NoOfStudents,'NoOfEvents':NoOfEvents,'NoOfTeachers':NoOfTeachers,
    'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    
    return render(request,'Admin_pannel/admindashboard.html',context)

@login_required(login_url='/loginpage/')
def admin_account_setting(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_account_setting.html',context)

@login_required(login_url='/loginpage/')
def admin_search(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    if request.method == "POST":
        text_str = request.POST['search_keyword']
        searched_course = Course_Detail.objects.filter(Course_Name__contains = text_str)
        searched_teacher = Teacher_Profile.objects.filter(Teacher_Name__contains = text_str)
        search_student = Student_Profile.objects.filter(Student_Name__contains = text_str)
        searched_event = Events.objects.filter(Event_Name__contains = text_str)
        searched_librarian = Librarian_Profile.objects.filter(Librarian_Name__contains = text_str)

        if searched_course:
            context = {'searched_course':searched_course,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}          
            #print(searched_course)
        elif searched_teacher:
            context = {'searched_teacher':searched_teacher,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
            #print(searched_teacher)
        elif search_student:            
            context = {'search_student':search_student,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
            #print(search_student)
        elif searched_event:
            context = {'searched_event':searched_event,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
            #print(searched_event)
        elif searched_librarian:
            context = {'searched_librarian':searched_librarian,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
            #print(searched_librarian)
        else:
            context = {'text_str':text_str,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
        
    return render(request,'Admin_pannel/admin_search.html',context)

@login_required(login_url='/loginpage/')
def Admin_personal_details_edit(request,pk):    
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]  
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()           
    requested_userID = Admin_Profile.objects.get(pk=pk)
    form = Admin_Personal_Details(instance=requested_userID)
    if request.method == 'POST':        
        form = Admin_Personal_Details(request.POST, request.FILES,instance = requested_userID)
        if form.is_valid():
            form.save() 
            messages.success(request,' Your Personal Details is updated successfully !')
        return redirect('admin_account_setting')                    
    context = {'userprofile':userprofile,'form':form,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}

    return render(request,'Admin_pannel/Admin_personal_details_edit.html',context)

class admin_notification(LoginRequiredMixin,ListView):
	model = User
	template_name = 'Admin_pannel/admin_notification.html'
	# context_object_name = 'books'
	paginate_by = 3

	def get_queryset(self):
		return User.objects.filter(is_active=False,Registered_As='None') 

# class admin_notification_details(LoginRequiredMixin,UpdateView):
#     model = User
#     form_class = admin_notification_details
#     template_name = 'Admin_pannel/admin_notification_details.html'
#     success_url = reverse_lazy('admin_notification')
#     success_message = 'Data was updated successfully'

@login_required(login_url='/loginpage/')   
def admin_all_contact(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0] 
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    objAllContact = Contact_us.objects.all()
    context = {'objAllContact':objAllContact,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_all_contact.html',context)

@login_required(login_url='/loginpage/')
def admin_contact_response(request,pk):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0] 
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    requested_contact_ID = Contact_us.objects.get(pk=pk)
    form = admin_contact_Reply(instance=requested_contact_ID)

    if request.method == 'POST':
        form = admin_contact_Reply(request.POST,instance=requested_contact_ID)
        if form.is_valid():
            form.save()
            now = datetime.now()
            print(now)
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S %Z")
            print(dt_string)
            updated_by = Admin_Profile.objects.get(Admin_User_PK= cuser)
            contact_name = form.cleaned_data.get('Contact_Name')
            obj_Contact = Contact_us.objects.get(pk=pk)
            obj_Contact.Contact_Last_Updated_Date = dt_string
            obj_Contact.Contact_Last_Updated_By = updated_by
            obj_Contact.Contact_Effective_End_Date = None
            obj_Contact.Contact_Status = "Solved"
            obj_Contact.save()
            # ------=========================== Email Sending Information =============================-------------------
            to_email = Contact_us.objects.filter(pk=pk).values('Contact_Email')[0]['Contact_Email']
            Contact_Name = Contact_us.objects.filter(pk=pk).values('Contact_Name')[0]['Contact_Name']
            email_Subject = "Contact Reply"
            email_message = "We have reply to your query. Please login to see our reply."
            send_mail_to_user(email_Subject,email_message,to_email,Contact_Name)
            messages.success(request," Your reply to "+ contact_name +" is sent successfully !")
            return redirect('admin_all_contact')
        else:
            messages.error(request,"Your reply is not sent successfully ! Please try again later !")
            return redirect('admin_all_contact')
    context = {'form':form,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_contact_response.html',context)   


@login_required(login_url='/loginpage/')
def admin_notification_details(request,pk):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0] 
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()   
    requested_userID = User.objects.get(pk=pk)
    registered_user = User.objects.filter(pk=pk)
    registered_user_email = registered_user.values('email')[0]['email']
    register_user_pk = registered_user.values('pk')
    form = User_Registration_Request(instance=requested_userID)
    if request.method == 'POST':
        form = User_Registration_Request(request.POST,instance = requested_userID)
        if form.is_valid():
            form.save()  
            first_name = form.cleaned_data.get('first_name') 
            last_name = form.cleaned_data.get('last_name')

            full_name = str(first_name)+' '+str(last_name)
            email = form.cleaned_data.get('email')
            user_DOB = form.cleaned_data.get('user_DOB')
            user_phone = form.cleaned_data.get('user_phone')
            user_status = "Active"
            UserAccount =  User.objects.get(pk=pk) 

            user_type = User.objects.filter(pk=pk).values('Registered_As')[0]['Registered_As']
            if(user_type == 'Student'):
                student_obj = Student_Profile(Student_User_PK = UserAccount,Student_Name = full_name,Student_Email = email,Student_Phone = user_phone,Student_DOB = user_DOB,Student_Status = user_status)
                student_obj.save()
                userpk = student_obj.pk
                Student_ID = 'STD' + str(userpk)
                obj = Student_Profile.objects.get(pk = userpk)
                obj.Student_ID = Student_ID
                obj.save()
            elif(user_type == 'Teacher'):
                Teacher_obj = Teacher_Profile(Teacher_User_PK=UserAccount,Teacher_Name = full_name,Teacher_Email = email,Teacher_Phone=user_phone,Teacher_DOB=user_DOB,Teacher_Status = user_status,Teacher_Address='None')
                Teacher_obj.save()
                teach_pk = Teacher_obj.pk
                Teacher_ID = 'TECH'+ str(teach_pk)
                obj = Teacher_Profile.objects.get(pk = teach_pk)
                obj.Teacher_ID = Teacher_ID
                obj.save()
        # Account Activation Email Link
        # current_site = get_current_site(request)
        # email_subject = "Verification Link for account activation"
        # email_messege = render_to_string('Admin_pannel/email_confirm.html',
        # {
       
        #     'name' : registered_user.values('first_name'),
        #     'domain': current_site.domain,
        #     'uid' : urlsafe_base64_encode(force_bytes(pk)),
        #     'token' : generate_token.make_token(requested_userID)
        # ,'TotalContactCount':TotalContactCount})
        # email = EmailMessage(
        #     email_subject,
        #     email_messege,
        #     settings.EMAIL_HOST_USER,
        #     [registered_user_email],
        # )
        # email.fail_silently = True
        # email.send()
        return redirect('admin_notification')

    context = {'form':form,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_notification_details.html',context)

@login_required(login_url='/loginpage/')
def activate(request, uidb64, token):    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        UserAccount = User.objects.get(pk = uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        UserAccount = None

    if UserAccount is not None and generate_token.check_token(UserAccount,token):
        UserAccount.is_active = True
        UserAccount.save()
        login(request,UserAccount)
        return redirect('')
    else:
        return render(request,'Admin_pannel/activation_failed.html')


#Admin Course
@login_required(login_url='/loginpage/')
def admin_add_course(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    if request.method =="POST":
        Course_Name = request.POST.get('Course_Name','')
        Course_Trainer = request.POST.get('Course_Trainer','')
        Start_Date = request.POST.get('Start_Date','')
        End_Date = request.POST.get('End_Date','')
        Course_Desc = request.POST.get('Course_Desc','')
        Course_Status = request.POST.get('Course_Status','')
        CourseBanner= request.FILES['CourseBanner']
        totalSyllabusRows = request.POST.get('totalSyllabusRows','')        
        totalModuleRows = request.POST.get('totalModuleRows','')        
        totalTimeTableRows = request.POST.get('totalTimeTableRows','')        
        totalExamTableRows = request.POST.get('totalExamTableRows','')
        
        if (Course_Detail.objects.filter(Course_Name = Course_Name)):
            messages.error(request," This Couse Name is aleady exist")            
        else:
            course_details_result = Course_Detail(Course_Name = Course_Name,Course_Instructor = Course_Trainer,Start_Date = Start_Date,End_Date = End_Date,Course_Desc = Course_Desc,Course_Status = Course_Status,CourseBanner = CourseBanner)
            course_details_result.save()
            for i in range(totalSyllabusRows):
                Course_Module_name = request.POST.get('','')
                Course_Week = request.POST.get('','')
                Course_Topic = request.POST.get('','')
                Course_Desc = request.POST.get('','')
            messages.success(request," New Course is added successfully !")
            return redirect('admin_all_course')
    return render(request,'Admin_pannel/admin_add_course.html',context)

@login_required(login_url='/loginpage/')
def admin_all_course(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    allcourse_obj = Course_Detail.objects.all()
    context = {'userprofile':userprofile,'allcourse_obj':allcourse_obj,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_all_course.html',context)

@login_required(login_url='/loginpage/')
def admin_course_details(request,pk):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_course_details.html',context)

#Admin student
@login_required(login_url='/loginpage/')
def admin_all_student(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    allstudent_obj = Student_Profile.objects.all()
    context = {'userprofile':userprofile,'allstudent_obj':allstudent_obj,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}    
    return render(request,'Admin_pannel/admin_all_student.html',context)

@login_required(login_url='/loginpage/')
def admin_add_student(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    if request.method =="POST":        
        firstname= request.POST.get('fname','')
        lastname= request.POST.get('lname','')
        email= request.POST.get('email','')
        username= request.POST.get('uname','')
        phoneNo= request.POST.get('phoneNo','')
        DateOfBirth= request.POST.get('dob','')
        address= request.POST.get('address','')
        profile_pic= request.FILES['profile_pic']
        password= request.POST.get('password','')
        cpassword= request.POST.get('cpassword','')
        student_name = firstname +" "+ lastname

        if User.objects.filter(username = username):
            messages.error(request," Username is already exist !")

        elif len(username)>20:
            messages.error(request, " Username must be under 20 charcters!!")
            
        elif User.objects.filter(email = email):
            messages.error(request," Email is already exist !")
        
        elif password == cpassword:

            UserAccount = User.objects.create_user(username,email,password)
            UserAccount.first_name = firstname
            UserAccount.last_name = lastname
            UserAccount.is_active = True
            UserAccount.Registered_As = 'Student'
            UserAccount.save()
            messages.success(request," You have successfully added the student !")
            
            userprofile = Student_Profile(Student_User_PK = UserAccount,Student_Name = student_name,Student_Email = email,Student_Phone = phoneNo,Student_DOB = DateOfBirth,Student_Address = address,Student_Status = 'Active',Student_Profile_Pic = profile_pic)
            userprofile.save()
            userpk = userprofile.pk
            Student_ID = 'STD' + str(userpk)
            obj = Student_Profile.objects.get(pk = userpk)
            obj.Student_ID = Student_ID
            obj.save()

            # Send an Email to User For successfully Registration
            subject = "Welcome to Education_Master"
            message = "Hello " + UserAccount.first_name + "!! \n" + "Welcome to Education_Master!! \nThank you for visiting our website\n. You can login now by your userid and password\n Your UserID:" +username + "\nYour password:"+ password +" \n\nThanking You\nTeam Education_Master"
            form_email = settings.EMAIL_HOST_USER
            to_email = [UserAccount.email]
            #send_mail(subject,message,form_email,to_email,fail_silently=True)
            #print("Message sent")

            return redirect('admin_all_student')
        
        else:
            messages.error(request," Password and confirm password doesn't matched !")

    return render(request,'Admin_pannel/admin_add_student.html',context)

@login_required(login_url='/loginpage/')
def admin_student_details(request,pk): 
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()           
    requested_userID = Student_Profile.objects.get(pk=pk)
    editeduser = Student_Profile.objects.filter(pk=pk).values('Student_Name')[0]['Student_Name']
    #print(editeduser)
    form = Admin_User_Profile_Edit(instance=requested_userID)
    if request.method == 'POST':        
        form = Admin_User_Profile_Edit(request.POST, request.FILES,instance = requested_userID)
        if form.is_valid():
            form.save() 

        messages.success(request," "+ str(editeduser) +"'s personal details is updated !")   
        return redirect('admin_all_student')               
     
    context = {'AllContext':form,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_student_details.html',context)

#Admin Teacher
@login_required(login_url='/loginpage/')
def admin_all_teacher(request):
    allteacher_obj = Teacher_Profile.objects.all()
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    context = {'userprofile':userprofile,'allteacher_obj':allteacher_obj,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}            
    return render(request,'Admin_pannel/admin_all_teacher.html',context)

@login_required(login_url='/loginpage/')
def admin_add_teacher(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    if request.method =="POST":            
        firstname= request.POST.get('fname','')
        lastname= request.POST.get('lname','')
        email= request.POST.get('email','')
        username= request.POST.get('uname','')
        phoneNo= request.POST.get('phoneNo','')
        DateOfBirth= request.POST.get('dob','')
        address= request.POST.get('address','')
        profile_pic= request.FILES['profile_pic']
        password= request.POST.get('password','')
        cpassword= request.POST.get('cpassword','')
        Teacher_name = firstname +" "+ lastname

        if User.objects.filter(username = username):
            messages.error(request," Username is already exist !")

        elif len(username)>20:
            messages.error(request, " Username must be under 20 charcters!!")
            
        elif User.objects.filter(email = email):
            messages.error(request," Email is already exist !")
        
        elif password == cpassword:
            UserAccount = User.objects.create_user(username,email,password)
            UserAccount.first_name = firstname
            UserAccount.last_name = lastname
            UserAccount.is_active = True
            UserAccount.Registered_As = 'Teacher'
            UserAccount.save()            
            
            userprofile = Teacher_Profile(Teacher_User_PK = UserAccount,Teacher_Name = Teacher_name,Teacher_Email = email,Teacher_Phone = phoneNo,Teacher_DOB = DateOfBirth,Teacher_Address = address,Teacher_Status = 'Active',Teacher_Profile_Pic = profile_pic)
            userprofile.save()
            userpk = userprofile.pk
            Teacher_ID = 'TECH' + str(userpk)
            obj = Teacher_Profile.objects.get(pk = userpk)
            obj.Teacher_ID = Teacher_ID
            obj.save()
            messages.success(request," You have successfully added the Teacher !")

            # Send an Email to User For successfully Registration
            subject = "Welcome to Education_Master"
            message = "Hello " + UserAccount.first_name + "!! \n" + "Welcome to Education_Master!! \nThank you for visiting our website\n. You can login now by your userid and password\n Your UserID:" +username + "\nYour password:"+ password +" \n\nThanking You\nTeam Education_Master"
            form_email = settings.EMAIL_HOST_USER
            to_email = [UserAccount.email]
            #send_mail(subject,message,form_email,to_email,fail_silently=True)
            #print("Message sent")
            return redirect('admin_all_teacher')
        else:
            messages.error(request," Password and confirm password doesn't matched !")

    return render(request,'Admin_pannel/admin_add_teacher.html',context)

@login_required(login_url='/loginpage/')
def admin_teacher_details(request,pk):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    requested_userID = Teacher_Profile.objects.get(pk=pk)
    editeduser = Teacher_Profile.objects.filter(pk=pk).values('Teacher_Name')[0]['Teacher_Name']
    #print(editeduser)
    form = Admin_Teacher_Profile_Edit(instance=requested_userID)
    if request.method == 'POST':        
        form = Admin_Teacher_Profile_Edit(request.POST, request.FILES,instance = requested_userID)
        if form.is_valid():
            form.save() 

        messages.success(request," "+ str(editeduser) +"'s personal details is updated !")   
        return redirect('admin_all_teacher')  
    context = {'AllContext':form,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_teacher_details.html',context)

# Admin Librarian

@login_required(login_url='/loginpage/')
def admin_all_librarian(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    all_librarian_obj = Librarian_Profile.objects.all()
    context = {'userprofile':userprofile,'all_librarian_obj':all_librarian_obj,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_all_librarian.html',context)

@login_required(login_url='/loginpage/')
def admin_add_librarian(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    if request.method =="POST":        
        firstname= request.POST.get('fname','')
        lastname= request.POST.get('lname','')
        email= request.POST.get('email','')
        username= request.POST.get('uname','')
        phoneNo= request.POST.get('phoneNo','')
        DateOfBirth= request.POST.get('dob','')
        address= request.POST.get('address','')
        profile_pic= request.FILES['profile_pic']
        password= request.POST.get('password','')
        cpassword= request.POST.get('cpassword','')
        librarian_name = firstname +" "+ lastname

        if User.objects.filter(username = username):
            messages.error(request," Username is already exist !")

        elif len(username)>20:
            messages.error(request, " Username must be under 20 charcters!!")
            
        elif User.objects.filter(email = email):
            messages.error(request," Email is already exist !")
        
        elif password == cpassword:

            UserAccount = User.objects.create_user(username,email,password)
            UserAccount.first_name = firstname
            UserAccount.last_name = lastname
            UserAccount.is_active = True
            UserAccount.Registered_As = 'LibraryAdmin'
            UserAccount.save()
            messages.success(request," You have successfully added the librarian !")
            
            userprofile = Librarian_Profile(Librarian_User_PK = UserAccount,Librarian_Name = librarian_name,Librarian_Email = email,Librarian_Phone = phoneNo,Librarian_DOB = DateOfBirth,Librarian_Address = address,Librarian_Status = 'Active',Librarian_Profile_Pic = profile_pic)
            userprofile.save()
            userpk = userprofile.pk
            Librarian_ID = 'STD' + str(userpk)
            obj = Librarian_Profile.objects.get(pk = userpk)
            obj.Librarian_ID = Librarian_ID
            obj.save()

            # Send an Email to User For successfully Registration
            subject = "Welcome to Education_Master"
            message = "Hello " + UserAccount.first_name + "!! \n" + "Welcome to Education_Master!! \nThank you for visiting our website\n. You can login now by your userid and password\n Your UserID:" +username + "\nYour password:"+ password +" \n\nThanking You\nTeam Education_Master"
            form_email = settings.EMAIL_HOST_USER
            to_email = [UserAccount.email]
            #send_mail(subject,message,form_email,to_email,fail_silently=True)
            #print("Message sent")

            return redirect('admin_all_librarian')
        
        else:
            messages.error(request," Password and confirm password doesn't matched !")
            
    return render(request,'Admin_pannel/admin_add_librarian.html',context)

@login_required(login_url='/loginpage/')
def admin_librarian_details(request,pk):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()

    requested_userID = Librarian_Profile.objects.get(pk=pk)
    editeduser = Librarian_Profile.objects.filter(pk=pk).values('Librarian_Name')[0]['Librarian_Name']
    form = Admin_Librarian_Profile_Edit(instance=requested_userID)
    if request.method == 'POST':        
        form = Admin_Librarian_Profile_Edit(request.POST, request.FILES,instance = requested_userID)
        if form.is_valid():
            form.save() 
        messages.success(request," "+ str(editeduser) +"'s personal details is updated !")   
        return redirect('admin_all_librarian')               
     
    context = {'userprofile':userprofile,'form':form,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_librarian_details.html',context)

#Admin User
@login_required(login_url='/loginpage/')
def admin_all_user(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    obj_All_User = Admin_Profile.objects.all()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'obj_All_User':obj_All_User,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_all_user.html',context)

@login_required(login_url='/loginpage/')
def admin_user_details(request,pk):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    requested_userID = Admin_Profile.objects.get(pk = pk)
    editeduser = Admin_Profile.objects.filter(pk=pk).values('Admin_Name')[0]['Admin_Name']
    form = Admin_Personal_Details(instance=requested_userID)
    if request.method == 'POST':
        form = Admin_Personal_Details(request.POST, request.FILES,instance = requested_userID)
        if form.is_valid():
            form.save()
            messages.success(request," "+ str(editeduser) + "'s personal details is updated !")
            return redirect('admin_all_user')
        else:
            messages.error(request," "+ str(editeduser) + "'s personal details is not updated !")
            return redirect('admin_all_user')
    context = {'userprofile':userprofile,'form':form,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_user_details.html',context)

#Admin events
@login_required(login_url='/loginpage/')
def admin_all_events(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    allevents_list = Events.objects.all().order_by('Event_ID')
    paginator = Paginator(allevents_list, 3)  # 6 Course in each page
    page = request.GET.get('page')
    try:
        allevents_obj = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        allevents_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        allevents_obj = paginator.page(paginator.num_pages)
    context = {'userprofile':userprofile,'allevents_obj':allevents_obj,'page':page,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_all_events.html',context)

@login_required(login_url='/loginpage/')
def admin_event_details(request,pk):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    requested_eventID = Events.objects.get(pk=pk)
    edit_event = Events.objects.filter(pk=pk).values('Event_Name')[0]['Event_Name']    
    form = Admin_Event_edit(instance=requested_eventID)
    if request.method == 'POST':        
        form = Admin_Event_edit(request.POST, request.FILES,instance = requested_eventID)
        if form.is_valid():
            form.save() 

        messages.success(request," "+ str(edit_event) +" event details is updated !")   
        return redirect('admin_all_events')               
    # AllContext.append([form])  
    context = {'AllContext':form,'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_event_details.html',context)

@login_required(login_url='/loginpage/')
def admin_add_event(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    if request.method =='POST':
        EventName=request.POST.get('EventName','')
        EventDesc = request.POST.get('EventDesc','')
        EventTopic = request.POST.get('EventTopic','')
        EventSDesc = request.POST.get('EventSDesc','')
        EventDept = request.POST.get('EventDept','')
        EventDate = request.POST.get('EventDate','')
        EventTime = request.POST.get('EventTime','')
        EventEndTime = request.POST.get('EventEndTime','')
        EventLink = request.POST.get('EventLink','')
        EventBanner = request.FILES['EventBanner']

        context = Events(Event_Name = EventName,Event_Topic = EventTopic,Event_Short_Desc = EventSDesc,Event_Date = EventDate,Event_Time = EventTime,Event_Long_desc = EventDesc,Event_Dept = EventDept,Event_End_Time =EventEndTime,Event_Link=EventLink,Event_Banner = EventBanner,Event_Status = "Active")
        context.save()
        messages.success(request," Event is added successfully !")
        return redirect('admin_all_events')

    return render(request,'Admin_pannel/admin_add_event.html',context)

#Admin Exam
@login_required(login_url='/loginpage/')
def admin_all_exam(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_all_exam.html',context)

@login_required(login_url='/loginpage/')
def admin_add_exam(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_add_exam.html',context)

@login_required(login_url='/loginpage/')
def admin_exam_details(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_exam_details.html',context)

@login_required(login_url='/loginpage/')
def admin_all_groups(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_all_groups.html',context)

@login_required(login_url='/loginpage/')
def admin_add_group(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_add_group.html',context)

#Admin Enquiry
@login_required(login_url='/loginpage/')
def admin_all_enquiry(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_all_enquiry.html',context)

@login_required(login_url='/loginpage/')
def admin_course_enquiry(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_course_enquiry.html',context)

@login_required(login_url='/loginpage/')
def admin_admission_enquiry(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_admission_enquiry.html',context)

@login_required(login_url='/loginpage/')
def admin_seminar_enquiry(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_seminar_enquiry.html',context)

@login_required(login_url='/loginpage/')
def admin_event_enquiry(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_event_enquiry.html',context)

@login_required(login_url='/loginpage/')
def admin_common_enquiry(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_common_enquiry.html',context)

@login_required(login_url='/loginpage/')
def admin_view_enquiry(request):
    cuser = request.user
    TotalContactCount = Contact_us.objects.filter(Contact_Status=('Pending')).count()    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    NoOfNewUserReg = User.objects.filter(is_active=False,Registered_As='None').count()
    context = {'userprofile':userprofile,'NoOfNewUserReg':NoOfNewUserReg,'TotalContactCount':TotalContactCount}
    return render(request,'Admin_pannel/admin_view_enquiry.html',context)

# ------------------------------------------------Teacher section------------------------------------------------
@login_required(login_url='/loginpage/')
def teacher_dashboard(request):
    cuser = request.user    
    userprofile = Teacher_Profile.objects.filter(Teacher_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    return render(request,"Teacher/teacher_dashboard.html",context)
# ------------------------------------------------Librarian section------------------------------------------------
@login_required(login_url='/loginpage/')
def librarian_dashboard(request):
    book = Books.objects.all().count()
    cuser = request.user    
    userprofile = Librarian_Profile.objects.filter(Librarian_User_PK=cuser)[0]
    Total_books = Book_Request.objects.filter(Book_Request_Status='Active').count()
    context = {'book':book,'userprofile':userprofile,'Total_books':Total_books}
    return render(request,'Librarian/librarian_dashboard.html',context)

def librarian_search(request):    
    if request.method == "POST":
        cuser = request.user    
        userprofile = Librarian_Profile.objects.filter(Librarian_User_PK=cuser)[0]
        book_keyword = request.POST['search_keyword']
        book_objs = Books.objects.filter(Book_Title__contains = book_keyword)
        Total_books = Book_Request.objects.filter(Book_Request_Status='Active').count()
        context = {'book_objs':book_objs,'userprofile':userprofile,'Total_books':Total_books}
    return render(request,'Librarian/librarian_search.html',context)

# def library_register(request):
#     all_register = Student_Library_Profile.objects.filter(Student_Status='Inactive')
#     context = {'all_register':all_register
#     return render(request,'Librarian/library_register.html',context)

class library_register(LoginRequiredMixin,ListView):
	model = Student_Library_Profile
	template_name = 'Librarian/library_register.html'
	# context_object_name = 'books'    
	paginate_by = 3

	def get_queryset(self):
		return Student_Library_Profile.objects.filter(Student_Status='Inactive')

@login_required(login_url='/loginpage/')
def library_register_details(request,pk):
    requested_user_obj = Student_Library_Profile.objects.get(pk=pk)
    requester_user = Student_Library_Profile.objects.filter(pk=pk).values('Library_User_Profile')[0]['Library_User_Profile']
    user_email = Student_Profile.objects.filter(pk=requester_user).values('Student_Email')[0]['Student_Email']
    user_name = Student_Profile.objects.filter(pk=requester_user).values('Student_Name')[0]['Student_Name']
    Total_books = Book_Request.objects.filter(Book_Request_Status='Active').count()
    #print(user_email)
    #print(user_name)
    u_id = user_name.split()[0]
    form = Library_registration_Request(instance=requested_user_obj)
    cuser = request.user    
    userprofile = Librarian_Profile.objects.filter(Librarian_User_PK=cuser)[0]
    user_id = "Education_Master_" + str(u_id)    
    user_pass = "Education_Master@123"

    if request.method == 'POST':
        form = Library_registration_Request(request.POST,instance = requested_user_obj)
        if form.is_valid():
            form.save()            
        # Send an Email to User For successfully Registration
        subject = "Education_Master Library Credentials"
        message = "Hello " + user_name + "!! \n" + "Your UserId: "+ user_id + "!! \n" + "Your Password: "+ user_pass +"\nPlease change your password as it is default system generated password.  \n\nThanking You\nTeam Education_Master"
        form_email = settings.EMAIL_HOST_USER
        to_email = [user_email]
        #send_mail(subject,message,form_email,to_email,fail_silently=True)
        messages.success(request," Library registration request of "+ str(user_name) +" is accepted successfully !")
        return redirect('librarian_dashboard')

    context = {'form':form,'userprofile':userprofile,'Total_books':Total_books}
    return render(request,'Librarian/library_register_details.html',context)

def book_request(request):
    cuser = request.user    
    userprofile = Librarian_Profile.objects.filter(Librarian_User_PK=cuser)[0]
    All_active_Book = Book_Request.objects.filter(Book_Request_Status='Active')
    Total_books = Book_Request.objects.filter(Book_Request_Status='Active').count()
    Total_books = Book_Request.objects.filter(Book_Request_Status='Active').count()
    context = {'userprofile':userprofile,'All_active_Book':All_active_Book,'Total_books':Total_books,'Total_books':Total_books}
    return render(request,'Librarian/book_request.html',context)

def book_request_details(request,pk):
    cuser = request.user    
    userprofile = Librarian_Profile.objects.filter(Librarian_User_PK=cuser)[0]
    Total_books = Book_Request.objects.filter(Book_Request_Status='Active').count()
    context = {'userprofile':userprofile,'Total_books':Total_books}
    if request.method == 'POST':
        title = request.POST['title']
        year = request.POST['year']
        Audio_book_page = request.POST['Audio_Start_Page']
        year = request.POST['year']
        author = request.POST['author']
        Audio_book_page = request.POST['Audio_Start_Page']
        username = request.user.username
        current_user = request.user
        user_id = current_user.id
        Book_Genre = request.POST['Book_Genre']
        Book_Category = request.POST['Book_Genre']
        Book_Length = request.POST['Book_Length']
        Book_Edition = request.POST['Book_Edition']
        pdf = request.FILES['pdf']
        cover = request.FILES['cover']
        desc = request.POST['desc']
        Book_ISBN = request.POST['Book_ISBN']
        publisher = request.POST['publisher']
        a = Books(Book_Title=title, Book_Author=author, Book_Publish_Year=year, Book_Publisher=publisher, Book_Desc=desc, Book_Cover=cover, Book_Pdf=pdf,Book_ISBN = Book_ISBN,Book_Edition = Book_Edition,Book_Length=Book_Length,Book_Genre=Book_Genre,Book_Category = Book_Category, Book_Uploaded_By=username,Book_User_Id = user_id,Audio_Start_Page = Audio_book_page) 
        a.save()
        Book_Request.objects.filter(Book_Request_ID=pk).update(Book_Request_Status='Inactive')
        messages.success(request, ' Book was uploaded successfully')
        return redirect('recent_book')
    return render(request,'Librarian/book_request_details.html',context)

@login_required(login_url='/loginpage/')
def add_book(request):
    cuser = request.user    
    userprofile = Librarian_Profile.objects.filter(Librarian_User_PK=cuser)[0]
    Total_books = Book_Request.objects.filter(Book_Request_Status='Active').count()
    context = {'userprofile':userprofile,'Total_books':Total_books}
    if request.method == 'POST':
        title = request.POST['title']
        year = request.POST['year']
        Audio_book_page = request.POST['Audio_Start_Page']
        year = request.POST['year']
        author = request.POST['author']
        Audio_book_page = request.POST['Audio_Start_Page']
        username = request.user.username
        current_user = request.user
        user_id = current_user.id
        Book_Genre = request.POST['Book_Genre']
        Book_Category = request.POST['Book_Genre']
        Book_Length = request.POST['Book_Length']
        Book_Edition = request.POST['Book_Edition']
        pdf = request.FILES['pdf']
        cover = request.FILES['cover']
        desc = request.POST['desc']
        Book_ISBN = request.POST['Book_ISBN']
        publisher = request.POST['publisher']
        a = Books(Book_Title=title, Book_Author=author, Book_Publish_Year=year, Book_Publisher=publisher, Book_Desc=desc, Book_Cover=cover, Book_Pdf=pdf,Book_ISBN = Book_ISBN,Book_Edition = Book_Edition,Book_Length=Book_Length,Book_Genre=Book_Genre,Book_Category = Book_Category, Book_Uploaded_By=username,Book_User_Id = user_id,Audio_Start_Page = Audio_book_page) 
        a.save()
        messages.success(request, ' Book was uploaded successfully')
        return redirect('recent_book')	
    return render(request,'Librarian/add_book.html',context)	  

class manage_book(LoginRequiredMixin,ListView):
	model = Books
	template_name = 'Librarian/manage_books.html'
	context_object_name = 'books'
	paginate_by = 3

	def get_queryset(self):
		return Books.objects.order_by('-Book_Id')

class view_book(LoginRequiredMixin,DetailView):
	model = Books
	template_name = 'Librarian/view_book.html'

class edit_book(LoginRequiredMixin,UpdateView):
	model = Books
	form_class = BookForm
	template_name = 'Librarian/edit_book.html'
	success_url = reverse_lazy('manage_book')
	success_message = 'Data was updated successfully'

class delete_book(LoginRequiredMixin,DeleteView):
	model = Books
	template_name = 'Librarian/delete_book.html'
	success_url = reverse_lazy('lmbook')
	success_message = 'Data was deleted successfully'

class recent_book(LoginRequiredMixin,ListView):
	model = Books
	template_name = 'Librarian/recent_book.html'
	paginate_by = 3

	def get_queryset(self):
		return Books.objects.all().order_by('-Book_Id')

def error_404_view(request,exception):
    return render(request,'Edu_Master/error_404_view.html')