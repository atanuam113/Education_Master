from distutils.command.upload import upload
from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse


class User(AbstractUser):
    # is_admin = models.BooleanField(default=False)
    # is_student = models.BooleanField(default=False)
    # is_trainer = models.BooleanField(default=False)
    # user_type = (
    #     ('Student':'Student'),
    #     ('Teacher':'Teacher'),        
    # )
    user_type = (
        ('None','None'),
        ('Student','Student'),
        ('Teacher','Teacher'),
        ('Admin','Admin'),
    )
    Registered_As = models.CharField(max_length=20,choices=user_type,default="")
    class Meta:
        swappable = 'AUTH_USER_MODEL'
    
class Contact_Us(models.Model):
    contactus_id = models.AutoField(primary_key=True)
    contactus_name = models.CharField(max_length=50,default="")
    contactus_phone = models.CharField(max_length=20,default="")
    contactus_email = models.CharField(max_length=100,default="")
    contactus_message = models.CharField(max_length=100,default="")

    def __str__(self):
        return self.contactus_name 

class Student_Profile(models.Model):
    Student_PK = models.AutoField(primary_key=True)
    Student_ID = models.CharField(max_length=100,default=str(Student_PK))
    Student_User_PK = models.OneToOneField(User,on_delete=models.CASCADE)
    Student_Name = models.CharField(max_length=200,default="")
    Student_Email = models.CharField(max_length=200,default="")
    Student_Phone = models.CharField(max_length=200,default="")
    Student_DOB = models.DateField()
    Student_Address = models.CharField(max_length=500,default="")
    Student_Type = (
        ('Active','Active'),
        ('Inactive','Inactive'),
        ('Hold','Hold'),
    )
    Student_Status = models.CharField(max_length=20,choices=Student_Type,default="")
    Student_Bio = models.CharField(max_length=1000,default="")
    Student_Profile_Pic = models.ImageField(upload_to = 'Edu_Master\Student',null= True,blank = True)
    Student_Github = models.CharField(max_length=200,default="")
    Student_Linkedin = models.CharField(max_length=200,default="")
    Student_Twitter = models.CharField(max_length=200,default="")

    def __str__(self):
        return self.Student_Name


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

    def __str__(self):
        return self.Event_Name
    
# class Event_Register(models.Model):
#     Event_ID = models.OneToOneField(Events,on_delete=models.CASCADE,primary_key=True)
#     Student_PK = models.OneToOneField(Student_Profile,on_delete=models.CASCADE)

#     def __str__(self):
#         return self.Student_PK