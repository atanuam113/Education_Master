import tempfile
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import Contact_Us, Event_Register,User,Student_Profile,Events,Course_Detail,Teacher_Profile
from django.contrib import auth, messages
from Education_Master import settings
from django.core.mail import EmailMessage,send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from .forms import *
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from . token import generate_token
from Education_Master import settings
from datetime import datetime
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

        if User.objects.filter(username = username):
            messages.error(request,"Username is already exist !")

        elif len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            
        elif User.objects.filter(email = email):
            messages.error(request,"Email is already exist !")
        
        elif password == cpassword:

            UserAccount = User.objects.create_user(username,email,password)
            UserAccount.first_name = firstname
            UserAccount.last_name = lastname
            UserAccount.is_active = False
            UserAccount.save()
            messages.success(request,"Your Account has been created succesfully!! Please check your email to get all information !")
            
            # Send an Email to User For successfully Registration
            subject = "Welcome to Education_Master"
            message = "Hello " + UserAccount.first_name + "!! \n" + "Welcome to Education_Master!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nTeam Education_Master"
            form_email = settings.EMAIL_HOST_USER
            to_email = [UserAccount.email]
            send_mail(subject,message,form_email,to_email,fail_silently=True)
            print("Message sent")
        
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
            else:
                messages.error(request, "Invalid username or password !")
                return redirect('login')
        else:
            messages.error(request, "Invalid username or passwords !")


    return render(request,'Edu_Master/login.html')

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
    contextItem = {'userprofile':userprofile}
    return render(request,'Edu_Master/Index.html',contextItem)

@login_required(login_url='/loginpage/')
def search_course(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    if request.method == "POST":
        searched_course = request.POST['search_course']        
        course_objs  = Books.objects.filter(Book_Title__contains = searched_course)
        # print(course_objs)
        context = {'userprofile':userprofile,'course_objs':course_objs}
        
    return render(request,'Edu_Master/search_course.html',context)

@login_required(login_url='/loginpage/')
def student_dashboard(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    contextItem = {'userprofile':userprofile,'item':userprofile}
    print(userprofile)
    return render(request,'Edu_Master/student_dashboard.html',contextItem)

@login_required(login_url='/loginpage/')
def student_profile(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    contextItem = {'userprofile':userprofile,'item':userprofile}
    print(userprofile)
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
    # print(userprofile)
    return render(request,'Edu_Master/student_exam.html',contextItem)

@login_required(login_url='/loginpage/')
def student_class_time(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    contextItem = {'userprofile':userprofile,'item':userprofile}
    print(userprofile)
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
    context = {'userprofile':userprofile}
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
    context = {'userprofile':userprofile}
    event_obj = Events.objects.all()
    context = {'userprofile':userprofile,'event_obj':event_obj}
    return render(request,'Edu_Master/event.html',context)

@login_required(login_url='/loginpage/')
def event_details(request,pk):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = Events.objects.filter(Event_ID = pk)[0]
    print(context)
    contextDict = {'item':context,'userprofile':userprofile}
    return render(request,'Edu_Master/event_details.html',contextDict)

@login_required(login_url='/loginpage/')
def event_register(request,pk):
    item = Events.objects.filter(Event_ID = pk)[0]    
    AllContext = []
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    print(userprofile)
    
    AllContext.append([item,userprofile])
    contextDict = {'AllContext':AllContext,'userprofile':userprofile}
    now = datetime.now()
    dt_string = now.strftime("YYYY-MM-DD HH:MM")

    if request.method =="POST":
        Student_pk = Student_Profile.objects.get(Student_User_PK=cuser)
        Eventid = Events.objects.get(Event_ID = pk)        
        if Event_Register.objects.filter(Student_PK = Student_pk,Event_ID = Eventid).exists():
            messages.error(request,"You have already registered in this events !")
        else:
            register_result = Event_Register()
            register_result.save()
            register_result.Event_ID.add(Eventid)
            register_result.Student_PK.add(Student_pk)
            userpk = register_result.pk
            
            obj = Event_Register.objects.get(pk = userpk)
            obj.Registration_Date = dt_string
            obj.save()
            messages.success(request,"You have successfully registered for this events.")
            return redirect('event')
    
    return render(request,'Edu_Master/event_register.html',contextDict)

@login_required(login_url='/loginpage/')
def all_trainer(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    return render(request,'Edu_Master/all_trainer.html',context)

@login_required(login_url='/loginpage/')
def contact_us(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    if request.method == "POST":
        c_name= request.POST.get('contactus_name','')
        c_phone= request.POST.get('contactus_phone','')
        c_email= request.POST.get('contactus_email','')
        c_message= request.POST.get('contactus_message','')
        contactus = Contact_Us(contactus_name=c_name,contactus_phone=c_phone,contactus_email=c_email,contactus_message=c_message)
        
        contactus.save()
        messages.success(request,"Your message is send successfully !")

    return render(request,'Edu_Master/contact_us.html',context)

# ------------------------------------------------Digital Library------------------------------------------------
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
                messages.error(request,"Your account is not activated yet !")
                
        # elif user_name.exists != True:
        #     messages.error(request,"No such account found. Register to access library !")
        #     return redirect('Library_Signup')
        else:
            messages.error(request,"Your userid or password is wrong !")

    return render(request,'Edu_Master/Library_Login.html')

def Library_Signup(request):
    cuser = request.user          
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    context = {'userprofile':userprofile}
    if request.method == "POST":
        Student_pk = Student_Profile.objects.get(Student_User_PK=cuser)
        user_name = Student_Profile.objects.filter(Student_User_PK=cuser).values('Student_Name')[0]['Student_Name']      
        u_name = user_name.split()[0]
        if Student_Library_Profile.objects.filter(Library_User_Profile = Student_pk).exists():
            messages.error(request,"You have already registered for the library !")
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
            send_mail(subject,message,form_email,to_email,fail_silently=True)
            messages.success(request,"You have registered successfully for library. You will get all details in your registered email shortly !")
            return redirect('Library_Login')        
    return render(request,'Edu_Master/Library_Signup.html',context)

def Library_ForgotPassword(request):
    return render(request,'Edu_Master/Library_ForgotPassword.html')

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

def search_book(request):
    if request.method == "POST":
        book_keyword = request.POST['book_keyword']
        book_objs = Books.objects.filter(Book_Title__contains = book_keyword)
        print(book_objs)
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
    
def Library_News_Event(request):
    return render(request,'Library/news-event.html')
    
def Library_Blog(request):
    return render(request,'Library/blog.html')
   
def Library_Blog_Detail(request):
    return render(request,'Library/news-event.html')

def Library_Services(request):
    return render(request,'Library/services.html')
 
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
#     print(BookPath)
#     print(Total_Page)
#     print(type(Total_Page))
#     print(Start_Page)
#     print(type(Start_Page))
#     AudioBook = Audio_Book.audiobook(BookPath,Total_Page,Start_Page)
#     return render(request,'User/AudioBook.html',{'AudioBook':AudioBook})


#------------------------------------------------Admin Section------------------------------------------------
@login_required(login_url='/loginpage/')
def admin_dashboard1(request):
    informationcount = User.objects.filter(is_active=False).count()
    diskinfo = {'informationcount':informationcount}
    return render(request,'Admin_pannel/admindashboard.html',diskinfo)

@login_required(login_url='/loginpage/')
def admin_account_setting(request):
    cuser = request.user    
    userprofile = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]
    contextItem = {'item':userprofile}
    return render(request,'Admin_pannel/admin_account_setting.html',contextItem)

def admin_search(request):
    if request.method == "POST":
        text_str = request.POST['search_keyword']
        searched_course = Course_Detail.objects.filter(Course_Name__contains = text_str)
        searched_teacher = Teacher_Profile.objects.filter(Teacher_Name__contains = text_str)
        search_student = Student_Profile.objects.filter(Student_Name__contains = text_str)
        searched_event = Events.objects.filter(Event_Name__contains = text_str)

        if searched_course:
            context = {'searched_course':searched_course}          
            print(searched_course)
        elif searched_teacher:
            context = {'searched_teacher':searched_teacher}
            print(searched_teacher)
        elif search_student:            
            context = {'search_student':search_student}
            print(search_student)
        elif searched_event:
            context = {'searched_event':searched_event}
            print(searched_event)
        else:
            context = {'text_str':text_str}
        
    return render(request,'Admin_pannel/admin_search.html',context)

def Admin_personal_details_edit(request,pk):    
    cuser = request.user    
    item = Admin_Profile.objects.filter(Admin_User_PK=cuser)[0]            
    requested_userID = Admin_Profile.objects.get(pk=pk)
    form = Admin_Personal_Details(instance=requested_userID)
    if request.method == 'POST':        
        form = Admin_Personal_Details(request.POST, request.FILES,instance = requested_userID)
        if form.is_valid():
            form.save() 
        return redirect('admin_account_setting')                    
    context = {'form':form}

    return render(request,'Admin_pannel/Admin_personal_details_edit.html',context)

class admin_notification(LoginRequiredMixin,ListView):
	model = User
	template_name = 'Admin_pannel/admin_notification.html'
	# context_object_name = 'books'
	paginate_by = 3

	def get_queryset(self):
		return User.objects.filter(is_active=False) 

# class admin_notification_details(LoginRequiredMixin,UpdateView):
#     model = User
#     form_class = admin_notification_details
#     template_name = 'Admin_pannel/admin_notification_details.html'
#     success_url = reverse_lazy('admin_notification')
#     success_message = 'Data was updated successfully'
    
@login_required(login_url='/loginpage/')
def admin_notification_details(request,pk):

    requested_userID = User.objects.get(pk=pk)
    registered_user = User.objects.filter(pk=pk)
    registered_user_email = registered_user.values('email')[0]['email']
    register_user_pk = registered_user.values('pk')
    print(registered_user_email)
    form = User_Registration_Request(instance=requested_userID)
    if request.method == 'POST':
        form = User_Registration_Request(request.POST,instance = requested_userID)
        if form.is_valid():
            form.save()            
        
        # Account Activation Email Link
        current_site = get_current_site(request)
        email_subject = "Verification Link for account activation"
        email_messege = render_to_string('Admin_pannel/email_confirm.html',
        {
       
            'name' : registered_user.values('first_name'),
            'domain': current_site.domain,
            'uid' : urlsafe_base64_encode(force_bytes(pk)),
            'token' : generate_token.make_token(requested_userID)
        })
        email = EmailMessage(
            email_subject,
            email_messege,
            settings.EMAIL_HOST_USER,
            [registered_user_email],
        )
        email.fail_silently = True
        email.send()
        return redirect('admin_notification')

    context = {'form':form}
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

    if request.method =="POST":
        Course_Name = request.POST.get('Course_Name','')
        Course_Trainer = request.POST.get('Course_Trainer','')
        Start_Date = request.POST.get('Start_Date','')
        End_Date = request.POST.get('End_Date','')
        Course_Desc = request.POST.get('Course_Desc','')
        Course_Status = request.POST.get('Course_Status','')
        CourseBanner= request.FILES['CourseBanner']
        if (Course_Detail.objects.filter(Course_Name = Course_Name)):
            messages.error(request,"This Couse Name is aleady exist")            
        else:
            course_details_result = Course_Detail(Course_Name = Course_Name,Course_Trainer = Course_Trainer,Start_Date = Start_Date,End_Date = End_Date,Course_Desc = Course_Desc,Course_Status = Course_Status,CourseBanner = CourseBanner)
            course_details_result.save()
            messages.success(request,"New Course is added successfully !")
            return redirect('admin_all_course')
    return render(request,'Admin_pannel/admin_add_course.html')

@login_required(login_url='/loginpage/')
def admin_all_course(request):
    context = Course_Detail.objects.all()
    return render(request,'Admin_pannel/admin_all_course.html',{'context':context})

@login_required(login_url='/loginpage/')
def admin_course_details(request,pk):
    return render(request,'Admin_pannel/admin_course_details.html')

#Admin student
@login_required(login_url='/loginpage/')
def admin_all_student(request):
    context = Student_Profile.objects.all()
    # print(context)
    return render(request,'Admin_pannel/admin_all_student.html',{'allstudent':context})

@login_required(login_url='/loginpage/')
def admin_add_student(request):
   
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
            messages.error(request,"Username is already exist !")

        elif len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            
        elif User.objects.filter(email = email):
            messages.error(request,"Email is already exist !")
        
        elif password == cpassword:

            UserAccount = User.objects.create_user(username,email,password)
            UserAccount.first_name = firstname
            UserAccount.last_name = lastname
            UserAccount.is_active = True
            UserAccount.save()
            messages.success(request,"You have successfully added the student !")
            
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
            send_mail(subject,message,form_email,to_email,fail_silently=True)
            print("Message sent")

            return redirect('admin_all_student')
        
        else:
            messages.error(request," Password and confirm password doesn't matched !")

    return render(request,'Admin_pannel/admin_add_student.html')

@login_required(login_url='/loginpage/')
def admin_student_details(request,pk):          
    requested_userID = Student_Profile.objects.get(pk=pk)
    editeduser = Student_Profile.objects.filter(pk=pk).values('Student_Name')[0]['Student_Name']
    print(editeduser)
    form = Admin_User_Profile_Edit(instance=requested_userID)
    if request.method == 'POST':        
        form = Admin_User_Profile_Edit(request.POST, request.FILES,instance = requested_userID)
        if form.is_valid():
            form.save() 

        messages.success(request," "+ str(editeduser) +"'s personal details is updated !")   
        return redirect('admin_all_student')               
     
    context = {'AllContext':form}
    return render(request,'Admin_pannel/admin_student_details.html',context)

#Admin Teacher
@login_required(login_url='/loginpage/')
def admin_all_teacher(request):
    context = Teacher_Profile.objects.all()            
    return render(request,'Admin_pannel/admin_all_teacher.html',{'allteacher':context})

@login_required(login_url='/loginpage/')
def admin_add_teacher(request):
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
            messages.error(request,"Username is already exist !")

        elif len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            
        elif User.objects.filter(email = email):
            messages.error(request,"Email is already exist !")
        
        elif password == cpassword:
            UserAccount = User.objects.create_user(username,email,password)
            UserAccount.first_name = firstname
            UserAccount.last_name = lastname
            UserAccount.is_active = True
            UserAccount.save()            
            
            userprofile = Teacher_Profile(Teacher_User_PK = UserAccount,Teacher_Name = Teacher_name,Teacher_Email = email,Teacher_Phone = phoneNo,Teacher_DOB = DateOfBirth,Teacher_Address = address,Teacher_Status = 'Active',Teacher_Profile_Pic = profile_pic)
            userprofile.save()
            userpk = userprofile.pk
            Teacher_ID = 'TECH' + str(userpk)
            obj = Teacher_Profile.objects.get(pk = userpk)
            obj.Teacher_ID = Teacher_ID
            obj.save()
            messages.success(request,"You have successfully added the Teacher !")

            # Send an Email to User For successfully Registration
            subject = "Welcome to Education_Master"
            message = "Hello " + UserAccount.first_name + "!! \n" + "Welcome to Education_Master!! \nThank you for visiting our website\n. You can login now by your userid and password\n Your UserID:" +username + "\nYour password:"+ password +" \n\nThanking You\nTeam Education_Master"
            form_email = settings.EMAIL_HOST_USER
            to_email = [UserAccount.email]
            send_mail(subject,message,form_email,to_email,fail_silently=True)
            print("Message sent")
            return redirect('admin_all_teacher')
        else:
            messages.error(request," Password and confirm password doesn't matched !")

    return render(request,'Admin_pannel/admin_add_teacher.html')

@login_required(login_url='/loginpage/')
def admin_teacher_details(request,pk):
    requested_userID = Teacher_Profile.objects.get(pk=pk)
    editeduser = Teacher_Profile.objects.filter(pk=pk).values('Teacher_Name')[0]['Teacher_Name']
    print(editeduser)
    form = Admin_Teacher_Profile_Edit(instance=requested_userID)
    if request.method == 'POST':        
        form = Admin_Teacher_Profile_Edit(request.POST, request.FILES,instance = requested_userID)
        if form.is_valid():
            form.save() 

        messages.success(request," "+ str(editeduser) +"'s personal details is updated !")   
        return redirect('admin_all_teacher')  
    context = {'AllContext':form}
    return render(request,'Admin_pannel/admin_teacher_details.html',context)


#Admin events
@login_required(login_url='/loginpage/')
def admin_all_events(request):
    context = Events.objects.all()
    print(context)
    return render(request,'Admin_pannel/admin_all_events.html',{'context':context})

@login_required(login_url='/loginpage/')
def admin_event_details(request,pk):
    requested_eventID = Events.objects.get(pk=pk)
    edit_event = Events.objects.filter(pk=pk).values('Event_Name')[0]['Event_Name']
    print(edit_event)
    form = Admin_Event_edit(instance=requested_eventID)
    if request.method == 'POST':        
        form = Admin_Event_edit(request.POST, request.FILES,instance = requested_eventID)
        if form.is_valid():
            form.save() 

        messages.success(request," "+ str(edit_event) +" event details is updated !")   
        return redirect('admin_all_events')               
    # AllContext.append([form])  
    context = {'AllContext':form}
    return render(request,'Admin_pannel/admin_event_details.html',context)

@login_required(login_url='/loginpage/')
def admin_add_event(request):
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
        messages.success(request,"Event is added successfully !")
        return redirect('admin_all_events')

    return render(request,'Admin_pannel/admin_add_event.html')

#Admin Exam
@login_required(login_url='/loginpage/')
def admin_all_exam(request):
    return render(request,'Admin_pannel/admin_all_exam.html')

@login_required(login_url='/loginpage/')
def admin_add_exam(request):
    return render(request,'Admin_pannel/admin_add_exam.html')

@login_required(login_url='/loginpage/')
def admin_exam_details(request):
    return render(request,'Admin_pannel/admin_exam_details.html')

@login_required(login_url='/loginpage/')
def admin_all_groups(request):
    return render(request,'Admin_pannel/admin_all_groups.html')

@login_required(login_url='/loginpage/')
def admin_add_group(request):
    return render(request,'Admin_pannel/admin_add_group.html')

#Admin Enquiry
@login_required(login_url='/loginpage/')
def admin_all_enquiry(request):
    return render(request,'Admin_pannel/admin_all_enquiry.html')

@login_required(login_url='/loginpage/')
def admin_course_enquiry(request):
    return render(request,'Admin_pannel/admin_course_enquiry.html')

@login_required(login_url='/loginpage/')
def admin_admission_enquiry(request):
    return render(request,'Admin_pannel/admin_admission_enquiry.html')

@login_required(login_url='/loginpage/')
def admin_seminar_enquiry(request):
    return render(request,'Admin_pannel/admin_seminar_enquiry.html')

@login_required(login_url='/loginpage/')
def admin_event_enquiry(request):
    return render(request,'Admin_pannel/admin_event_enquiry.html')

@login_required(login_url='/loginpage/')
def admin_common_enquiry(request):
    return render(request,'Admin_pannel/admin_common_enquiry.html')

@login_required(login_url='/loginpage/')
def admin_view_enquiry(request):
    return render(request,'Admin_pannel/admin_view_enquiry.html')

# ------------------------------------------------Librarian section------------------------------------------------
def librarian_dashboard(request):
    book = Books.objects.all().count()
    context = {'book':book}
    return render(request,'Librarian/librarian_dashboard.html',context)

# def library_register(request):
#     all_register = Student_Library_Profile.objects.filter(Student_Status='Inactive')
#     context = {'all_register':all_register}
#     return render(request,'Librarian/library_register.html',context)

class library_register(LoginRequiredMixin,ListView):
	model = Student_Library_Profile
	template_name = 'Librarian/library_register.html'
	# context_object_name = 'books'
	paginate_by = 3

	def get_queryset(self):
		return Student_Library_Profile.objects.filter(Student_Status='Inactive')

def library_register_details(request,pk):
    requested_user_obj = Student_Library_Profile.objects.get(pk=pk)
    requester_user = Student_Library_Profile.objects.filter(pk=pk).values('Library_User_Profile')[0]['Library_User_Profile']
    user_email = Student_Profile.objects.filter(pk=requester_user).values('Student_Email')[0]['Student_Email']
    user_name = Student_Profile.objects.filter(pk=requester_user).values('Student_Name')[0]['Student_Name']
    print(user_email)
    print(user_name)
    u_id = user_name.split()[0]
    form = Library_registration_Request(instance=requested_user_obj)
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
        send_mail(subject,message,form_email,to_email,fail_silently=True)
        messages.success(request," Library registration request of "+ str(user_name) +" is accepted successfully !")
        return redirect('librarian_dashboard')

    context = {'form':form}
    return render(request,'Librarian/library_register_details.html',context)


def add_book(request):
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
        messages.success(request, 'Book was uploaded successfully')
        return redirect('recent_book')
	  
    return render(request,'Librarian/add_book.html')	  

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
