import tempfile
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import Contact_Us,User,Student_Profile,Events
from django.contrib import auth, messages
from Education_Master import settings
from django.core.mail import EmailMessage,send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from .forms import User_Registration_Request,User_Profile_Edit,Admin_User_Profile_Edit,Admin_Event_edit
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_text
from . token import generate_token
from Education_Master import settings
# Create your views here.

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
            else:
                messages.info(request, "Invalid username or password")
                return redirect('login')
        else:
            messages.error(request, "Your account is not activated!!")


    return render(request,'Edu_Master/login.html')

@login_required(login_url='/loginpage/')
def LogOut(request):
    logout(request)
    return redirect("login")


def forgotpass(request):
    return render(request,'Edu_Master/forgotpass.html')

@login_required(login_url='/loginpage/')
def home(request):
    cuser = request.user
    # print(cuser)
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    contextItem = {'item':userprofile}

    print(userprofile)


    return render(request,'Edu_Master/Index.html',contextItem)

@login_required(login_url='/loginpage/')
def student_dashboard(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    contextItem = {'item':userprofile}
    print(userprofile)
    return render(request,'Edu_Master/student_dashboard.html',contextItem)

@login_required(login_url='/loginpage/')
def student_profile(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    contextItem = {'item':userprofile}
    print(userprofile)
    return render(request,'Edu_Master/student_profile.html',contextItem)

@login_required(login_url='/loginpage/')
def student_course(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    contextItem = {'item':userprofile}
    print(userprofile)
    return render(request,'Edu_Master/student_course.html',contextItem)

@login_required(login_url='/loginpage/')
def student_exam(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    contextItem = {'item':userprofile}
    print(userprofile)
    return render(request,'Edu_Master/student_exam.html',contextItem)

@login_required(login_url='/loginpage/')
def student_class_time(request):
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    contextItem = {'item':userprofile}
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
    context = {'AllContext':AllContext}
    return render(request,'Edu_Master/student_Profile_Edit.html',context)

@login_required(login_url='/loginpage/')
def event_register(request,pk):
    item = Events.objects.filter(Event_ID = pk)[0]
    AllContext = []
    cuser = request.user    
    userprofile = Student_Profile.objects.filter(Student_User_PK=cuser)[0]
    print(userprofile)
    AllContext.append([item,userprofile])
    contextDict = {'AllContext':AllContext}
    # ,'loginuser':userprofile
    return render(request,'Edu_Master/event_register.html',contextDict)

@login_required(login_url='/loginpage/')
def about(request):
    return render(request,'Edu_Master/about.html')

@login_required(login_url='/loginpage/')
def award(request):
    return render(request,'Edu_Master/award.html')

@login_required(login_url='/loginpage/')
def research(request):
    return render(request,'Edu_Master/research.html')

@login_required(login_url='/loginpage/')
def facilities(request):
    return render(request,'Edu_Master/facilities.html')

@login_required(login_url='/loginpage/')
def facilities_detail(request):
    return render(request,'Edu_Master/facilities_detail.html')

@login_required(login_url='/loginpage/')
def departments(request):
    return render(request,'Edu_Master/departments.html')

@login_required(login_url='/loginpage/')
def all_course(request):
    return render(request,'Edu_Master/all_course.html')

@login_required(login_url='/loginpage/')
def seminar(request):
    return render(request,'Edu_Master/seminar.html')

@login_required(login_url='/loginpage/')
def course_details(request):
    return render(request,'Edu_Master/course_details.html')

@login_required(login_url='/loginpage/')
def blog(request):
    return render(request,'Edu_Master/blog.html')

@login_required(login_url='/loginpage/')
def blog_details(request):
    return render(request,'Edu_Master/blog_details.html')

@login_required(login_url='/loginpage/')
def event(request):
    context = Events.objects.all()
    return render(request,'Edu_Master/event.html',{'context':context})

@login_required(login_url='/loginpage/')
def event_details(request,pk):
    context = Events.objects.filter(Event_ID = pk)[0]
    print(context)
    contextDict = {'item':context}
    return render(request,'Edu_Master/event_details.html',contextDict)

@login_required(login_url='/loginpage/')
def all_trainer(request):
    return render(request,'Edu_Master/all_trainer.html')

@login_required(login_url='/loginpage/')
def contact_us(request):
    if request.method == "POST":
        c_name= request.POST.get('contactus_name','')
        c_phone= request.POST.get('contactus_phone','')
        c_email= request.POST.get('contactus_email','')
        c_message= request.POST.get('contactus_message','')
        contactus = Contact_Us(contactus_name=c_name,contactus_phone=c_phone,contactus_email=c_email,contactus_message=c_message)
        
        contactus.save()
        messages.success(request,"Your message is send successfully !")

    return render(request,'Edu_Master/contact_us.html')

#Admin section
@login_required(login_url='/loginpage/')
def admin_dashboard1(request):
    informationcount = User.objects.filter(is_active=False).count()
    diskinfo = {'informationcount':informationcount}
    return render(request,'Admin_pannel/admindashboard.html',diskinfo)


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
        uid = force_text(urlsafe_base64_decode(uidb64))
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
    return render(request,'Admin_pannel/admin_add_course.html')

@login_required(login_url='/loginpage/')
def admin_all_course(request):
    return render(request,'Admin_pannel/admin_all_course.html')

@login_required(login_url='/loginpage/')
def admin_course_details(request):
    return render(request,'Admin_pannel/admin_course_details.html')

@login_required(login_url='/loginpage/')
#Admin student
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
        profile_pic= request.POST.get('profile_pic','')
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

            # Send an Email to User For successfully Registration
            subject = "Welcome to Education_Master"
            message = "Hello " + UserAccount.first_name + "!! \n" + "Welcome to Education_Master!! \nThank you for visiting our website\n. You can login now by your userid and password\n Your UserID:" +username + "\nYour password:"+ password +" \n\nThanking You\nTeam Education_Master"
            form_email = settings.EMAIL_HOST_USER
            to_email = [UserAccount.email]
            send_mail(subject,message,form_email,to_email,fail_silently=True)
            print("Message sent")

            return redirect('admin_dashboard1')
        
        else:
            messages.error(request," Password and confirm password doesn't matched !")

    return render(request,'Admin_pannel/admin_add_student.html')

@login_required(login_url='/loginpage/')
def admin_student_details(request,pk):
    # AllContext = []
    # cuser = request.user    
    # item = Student_Profile.objects.filter(Student_User_PK=cuser)[0]            
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
    # AllContext.append([form])  
    context = {'AllContext':form}
    return render(request,'Admin_pannel/admin_student_details.html',context)

#Admin Teacher
@login_required(login_url='/loginpage/')
def admin_all_teacher(request):
    return render(request,'Admin_pannel/admin_all_teacher.html')

@login_required(login_url='/loginpage/')
def admin_add_teacher(request):
    return render(request,'Admin_pannel/admin_add_teacher.html')

@login_required(login_url='/loginpage/')
def admin_teacher_details(request):
    return render(request,'Admin_pannel/admin_teacher_details.html')


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
        EventLink = request.POST.get('EventLink','')
        EventBanner = request.FILES['EventBanner']

        context = Events(Event_Name = EventName,Event_Topic = EventTopic,Event_Short_Desc = EventSDesc,Event_Date = EventDate,Event_Time = EventTime,Event_Long_desc = EventDesc,Event_Dept = EventDept,Event_Link=EventLink,Event_Banner = EventBanner)
        context.save()
        messages.success(request,"Event is added successfully !")
        return redirect('admin_dashboard1')



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
