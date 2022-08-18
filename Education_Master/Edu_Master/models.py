from distutils.command.upload import upload
from statistics import mode
from xml.parsers.expat import model
from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse


class User(AbstractUser):
    user_type = (
        ('None','None'),
        ('Student','Student'),
        ('Teacher','Teacher'),
        ('Admin','Admin'),
        ('LibraryAdmin','LibraryAdmin'),
    )
    Registered_As = models.CharField(max_length=20,choices=user_type,default="")
    user_DOB = models.DateField(null=True)
    user_phone = models.CharField(max_length=100,default="None")
    class Meta:
        swappable = 'AUTH_USER_MODEL'

class Student_Profile(models.Model):
    Student_PK = models.AutoField(primary_key=True)
    Student_ID = models.CharField(max_length=100,default="None")
    Student_User_PK = models.OneToOneField(User,on_delete=models.CASCADE)
    Student_Name = models.CharField(max_length=200,default="")
    Student_Email = models.CharField(max_length=200,default="")
    Student_Phone = models.CharField(max_length=200,default="None")
    Student_DOB = models.DateField()
    Student_Address = models.CharField(max_length=500,default="None")
    Student_Type = (
        ('Active','Active'),
        ('Inactive','Inactive'),
        ('Hold','Hold'),
    )
    Student_Status = models.CharField(max_length=20,choices=Student_Type,default="")
    Student_Bio = models.CharField(max_length=1000,default="None")
    Student_Profile_Pic = models.ImageField(upload_to = 'Edu_Master\Student',null= True,blank = True)
    Student_Github = models.CharField(max_length=200,default="None")
    Student_Linkedin = models.CharField(max_length=200,default="None")
    Student_Twitter = models.CharField(max_length=200,default="None")

    def __str__(self):
        return self.Student_Name

class Student_Library_Profile(models.Model):
    Library_PK = models.AutoField(primary_key=True)
    Library_User_Profile = models.OneToOneField(Student_Profile,on_delete=models.CASCADE)
    Student_Type = (
        ('Active','Active'),
        ('Inactive','Inactive'),
        ('Hold','Hold'),
    )
    Student_Status = models.CharField(max_length=20,choices=Student_Type,default="")
    Library_user_ID = models.CharField(max_length=100,default="")
    Library_Password = models.CharField(max_length=50,default="")

    # def __str__(self):
    #     return self.Library_User_Profile

class Teacher_Profile(models.Model):
    Teacher_PK = models.AutoField(primary_key=True)
    Teacher_ID = models.CharField(max_length=100,default="")
    Teacher_User_PK = models.OneToOneField(User,on_delete=models.CASCADE)
    Teacher_Name = models.CharField(max_length=200,default="")
    Teacher_Email = models.CharField(max_length=200,default="")
    Teacher_Phone = models.CharField(max_length=200,default="")
    Teacher_DOB = models.DateField()
    Teacher_Address = models.CharField(max_length=500,default="")
    Teacher_Type = (
        ('Active','Active'),
        ('Inactive','Inactive'),
        ('Hold','Hold'),
    )
    Teacher_Dept = models.CharField(max_length=500,default="None")
    Teacher_Status = models.CharField(max_length=20,choices=Teacher_Type,default="")
    Teacher_Bio = models.CharField(max_length=1000,default="None")
    Teacher_Profile_Pic = models.ImageField(upload_to = 'Edu_Master\Teacher',null= True,blank = True)
    Teacher_Github = models.CharField(max_length=200,default="None")
    Teacher_Linkedin = models.CharField(max_length=200,default="None")
    Teacher_Twitter = models.CharField(max_length=200,default="None")

    def __str__(self):
        return self.Teacher_Name

class Admin_Profile(models.Model):
    Admin_PK = models.AutoField(primary_key=True)
    Admin_ID = models.CharField(max_length=100,default="")
    Admin_User_PK = models.OneToOneField(User,on_delete=models.CASCADE)
    Admin_Name = models.CharField(max_length=200,default="")
    Admin_Email = models.CharField(max_length=200,default="")
    Admin_Phone = models.CharField(max_length=200,default="")
    Admin_DOB = models.DateField()
    Admin_Address = models.CharField(max_length=500,default="")
    Admin_Type = (
        ('Active','Active'),
        ('Inactive','Inactive'),
        ('Hold','Hold'),
    )
    Admin_Status = models.CharField(max_length=20,choices=Admin_Type,default="")
    Admin_Bio = models.CharField(max_length=1000,default="None")
    Admin_Profile_Pic = models.ImageField(upload_to = 'Edu_Master\Admin',null= True,blank = True)
    Admin_Github = models.CharField(max_length=200,default="None")
    Admin_Linkedin = models.CharField(max_length=200,default="None")
    Admin_Twitter = models.CharField(max_length=200,default="None")

    def __str__(self):
        return self.Admin_Name

class Librarian_Profile(models.Model):
    Librarian_PK = models.AutoField(primary_key=True)
    Librarian_ID = models.CharField(max_length=100,default="")
    Librarian_User_PK = models.OneToOneField(User,on_delete=models.CASCADE)
    Librarian_Name = models.CharField(max_length=200,default="")
    Librarian_Email = models.CharField(max_length=200,default="")
    Librarian_Phone = models.CharField(max_length=200,default="")
    Librarian_DOB = models.DateField()
    Librarian_Address = models.CharField(max_length=500,default="")
    Librarian_Type = (
        ('Active','Active'),
        ('Inactive','Inactive'),
        ('Hold','Hold'),
    )
    Librarian_Status = models.CharField(max_length=20,choices=Librarian_Type,default="")
    Librarian_Bio = models.CharField(max_length=1000,default="None")
    Librarian_Profile_Pic = models.ImageField(upload_to = 'Edu_Master\Librarian',null= True,blank = True)
    Librarian_Github = models.CharField(max_length=200,default="None")
    Librarian_Linkedin = models.CharField(max_length=200,default="None")
    Librarian_Twitter = models.CharField(max_length=200,default="None")
    
    def __str__(self):
        return self.Librarian_Name

class Events(models.Model):
    Event_ID = models.AutoField(primary_key=True)
    Event_Name = models.CharField(max_length=200,default="")
    Event_Topic = models.CharField(max_length=500,default="")
    Event_Short_Desc = models.CharField(max_length=200,default="")
    Event_Date = models.DateField()
    Event_Time = models.TimeField()
    Event_End_Time = models.TimeField(default='00:00')
    Event_Long_desc = models.TextField(default="")
    Dept_Choice = (
        ('Java','Java'),
        ('Python','Python'),
        ('Auto Mobile','Auto Mobile')
    )
    Event_Dept = models.CharField(max_length=50,choices=Dept_Choice,default="")
    # Event_Dept_ID = models.CharField(max_length=50,default="")
    Event_Link = models.CharField(max_length=100,default="")
    Event_Banner = models.ImageField(upload_to = 'Edu_Master\Events',null = True,blank = True)
    Event_StatusChoice = (
        ('Active','Active'),
        ('InActive','InActive')        
    )
    Event_Status = models.CharField(max_length=50,choices=Event_StatusChoice,default="")
    slug = models.SlugField(null=True)

    def get_absolute_url(self):
        return reverse("event_register", kwargs={"slug": self.slug})

    def __str__(self):
        return self.Event_Name
    
class Event_Register(models.Model):
    Event_Register_ID = models.AutoField(primary_key=True)
    Event_ID = models.ManyToManyField(Events)
    Student_PK = models.ManyToManyField(Student_Profile)
    Registration_Date = models.DateTimeField(auto_now=True)
    

# Library section 
class Books(models.Model):
    Book_Id = models.AutoField(primary_key=True)
    Book_Title = models.CharField(max_length=100)
    Book_Author = models.CharField(max_length=100)
    Book_Publish_Year = models.CharField(max_length=100)
    Book_Publisher = models.CharField(max_length=200)
    Book_ISBN = models.CharField(max_length=100)
    Book_Edition = models.CharField(max_length=100,default="")
    Book_Length = models.IntegerField()
    Book_Desc = models.CharField(max_length=1000)
    Audio_Start_Page = models.PositiveSmallIntegerField(default=0)
    BOOK_CHOICES = (
        ('Science', 'Science'),
        ('Life_Style', 'Life_Style'),
        ('Comp_Science', 'Comp_Science'),
        ('Communication', 'Communication'),
        ('Medicine', 'Medicine'),
        ('Eco_Fin', 'Eco_Fin'),
    )
    Book_Category = models.CharField(choices=BOOK_CHOICES,max_length=100,default="")
    Book_Genre = models.CharField(max_length=1000,default="")
    Book_Uploaded_By = models.CharField(max_length=100, null=True, blank=True)
    Book_User_Id = models.CharField(max_length=100, null=True, blank=True)
    Book_Pdf = models.FileField(upload_to='Edu_Master\Book_PDF')
    Book_Cover = models.ImageField(upload_to='Edu_Master\Book_Cover', null=True, blank=True)

    def __str__(self):
        return self.Book_Title

    def delete(self, *args, **kwargs):
        self.Book_Pdf.delete()
        self.Book_Cover.delete()
        super().delete(*args, **kwargs) 

class Book_Request(models.Model):
    Book_Request_ID = models.AutoField(primary_key=True)
    Book_Request_Name = models.CharField(max_length=500,default="None")
    Book_Request_Author = models.CharField(max_length=200,default="None")
    Book_Request_ISBN = models.CharField(max_length=30,default="0")
    Book_Request_Date = models.DateField(null=True)
    Req_status = (
        ('Active','Active'),
        ('Inactive','Inactive'),
        ('Hold','Hold'),
    )
    Book_Request_Status = models.CharField(max_length=50,choices=Req_status,default="None")
    Book_Request_By = models.ForeignKey(Student_Profile,on_delete=models.CASCADE)

    def __str__(self):
        return self.Book_Request_Name
        
# Course section 
class Course_Detail(models.Model):
    Course_ID = models.AutoField(primary_key=True)
    Course_Name = models.CharField(max_length=100,default="")
    Start_Date = models.DateField()
    End_Date = models.DateField()
    Course_Instructor = models.ForeignKey(Teacher_Profile,on_delete=models.CASCADE,null= True,blank = True)
    Course_Desc = models.TextField(default="")
    slug = models.SlugField(null=True)
    status_type = (
        ('Active','Active'),
        ('Inactive','Inactive'),
        ('Hold','Hold'),
    )
    course_type = (
        ('Introductory','Introductory'),
        ('Intermediate','Intermediate'),
        ('Advanced','Advanced'),
    )
    Course_level = models.CharField(max_length=20,choices=course_type,default="")
    Course_Rating = models.CharField(max_length=20,default="0")
    Course_Status = models.CharField(choices=status_type,default="",max_length=100)
    Course_Skill = models.CharField(max_length=200,default="")
    CourseBanner = models.ImageField(upload_to = 'Edu_Master\Course',null=True,blank=True)

    def __str__(self):
        return self.Course_Name

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"slug": self.slug})
    
class Course_Syllabus(models.Model):
    Course_Syllabus_ID = models.AutoField(primary_key=True)
    Course_Name = models.ForeignKey(Course_Detail,on_delete=models.CASCADE)
    Module_Name = models.CharField(max_length=100,default="")
    Module_Week = models.CharField(max_length=50,default="")
    Module_Topic = models.CharField(max_length=200,default="")
    Module_Description = models.CharField(max_length=1000,default="")

    def __str__(self):
        return self.Course_Name

class Course_Module(models.Model):
    Course_Module_ID = models.AutoField(primary_key=True)
    Course_Name = models.ForeignKey(Course_Detail,on_delete=models.CASCADE)
    Module_Topic = models.CharField(max_length=200,default="")
    module_Content = models.FileField(upload_to='Edu_Master\Course_Module',)

    def __str__(self):
        return self.Course_Name

class Course_Time_Table(models.Model):
    Course_Time_Table_ID = models.AutoField(primary_key = True)
    Course_Name = models.ForeignKey(Course_Detail,on_delete=models.CASCADE)
    week_Days = (
        ('SunDay','SunDay'),
        ('MonDay','MonDay'),
        ('TuesDay','TuesDay'),
        ('WednesDay','WednesDay'),
        ('ThursDay','ThursDay'),
        ('FriDay','FriDay'),
        ('SaturDay','SaturDay'),        
    )
    Class_Day = models.CharField(max_length=100,choices=week_Days,default="")
    Class_Date = models.DateField()
    Class_Start_Time = models.TimeField()
    Class_End_Time = models.TimeField()
    Class_Topic = models.CharField(max_length=200,default="")
    Class_Link = models.CharField(max_length=200,default="")

    def __str__(self):
        return self.Course_Name

class Course_Exam_Table(models.Model):
    Exam_ID = models.AutoField(primary_key = True)
    Course_Name = models.ForeignKey(Course_Detail,on_delete=models.CASCADE)
    Exam_Name = models.CharField(max_length=200,default="")
    Exam_Date = models.DateField()
    Exam_Start_Time = models.TimeField()
    Exam_End_Time = models.TimeField()
    Exam_Link = models.CharField(max_length=300,default="")

    def __str__(self):
        return self.Course_Name


class Address_Book(models.Model):
    AB_ID = models.AutoField(primary_key=True)
    AB_Party_Id = models.CharField(max_length=50,default="None")
    AB_Party_Address = models.CharField(max_length=500,default="None")
    AB_Party_City = models.CharField(max_length=200,default="None")
    AB_Party_State = models.CharField(max_length=200,default="None")
    AB_Party_Country = models.CharField(max_length=200,default="None")
    AB_Party_Zip = models.CharField(max_length=200,default="None")


class Contact_us(models.Model):
    Contact_ID = models.AutoField(primary_key=True)
    Contact_Name = models.CharField(max_length=200,default="None")
    Contact_Email = models.EmailField(max_length=254)
    Contact_Message = models.TextField(default="None")
    Contact_Created_By = models.CharField(max_length=200,default= "None")
    Contact_Created_Date = models.DateTimeField(null = True)
    Contact_Last_Updated_Date = models.DateTimeField(null = True)
    Contact_Last_Updated_By = models.ForeignKey(Admin_Profile,on_delete=models.CASCADE,default=1)
    Contact_Effective_End_Date = models.DateTimeField(null = True)
    Contact_Version = models.CharField(default="1",max_length=20)
    Contact_Reply = models.TextField(default="None")
    Status_option = (
        ('Solved','Solved'),
        ('Pending','Pending'),
        ('Hold','Hold')
    )
    Contact_Status = models.CharField(max_length=100,choices=Status_option,default = "None")


    def __str__(self):
        return self.Contact_Name
