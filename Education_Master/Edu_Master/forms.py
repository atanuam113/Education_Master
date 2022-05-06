from operator import mod
from pyexpat import model
from attr import fields
from django.contrib.auth.forms import UserCreationForm
from Edu_Master.models import *
from django import forms
from django.forms import ModelForm

class User_Registration_Request(forms.ModelForm):
    class Meta:
        model = User      
        fields = ('first_name','last_name','email','username','Registered_As')

class User_Profile_Edit(forms.ModelForm):
    class Meta:
        model = Student_Profile      
        fields = ('Student_Bio','Student_Phone','Student_Address','Student_Github','Student_Linkedin','Student_Twitter','Student_Profile_Pic')


class Admin_User_Profile_Edit(forms.ModelForm):
    class Meta:
        model = Student_Profile      
        fields = ('Student_Bio','Student_Phone','Student_Address','Student_Github','Student_Linkedin','Student_Twitter','Student_Status','Student_Profile_Pic')

class Admin_Teacher_Profile_Edit(forms.ModelForm):
    class Meta:
        model = Teacher_Profile      
        fields = ('Teacher_Bio','Teacher_Phone','Teacher_Address','Teacher_Github','Teacher_Linkedin','Teacher_Twitter','Teacher_Status','Teacher_Profile_Pic')

class Admin_Personal_Details(forms.ModelForm):
    class Meta:
        model = Admin_Profile
        fields = ('Admin_Bio','Admin_Phone','Admin_Address','Admin_Github','Admin_Linkedin','Admin_Twitter','Admin_Status','Admin_Profile_Pic')

class Admin_Event_edit(forms.ModelForm):
    class Meta:
        model = Events
        fields= ('Event_Name','Event_Topic','Event_Short_Desc','Event_Date','Event_Time','Event_End_Time','Event_Long_desc','Event_Dept','Event_Link','Event_Banner','Event_Status')

class User_Event_Register(forms.ModelForm):
    class Meta:
        model = Event_Register
        fields = ('Event_ID','Student_PK')

class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ('Book_Title', 'Book_Author', 'Book_Publisher', 'Book_Publish_Year','Book_ISBN','Book_Edition','Book_Length','Audio_Start_Page','Book_Category', 'Book_Desc','Book_Cover','Book_Pdf')        

class Library_registration_Request(forms.ModelForm):
    class Meta:
        model = Student_Library_Profile
        fields = ('Library_user_ID','Student_Status')