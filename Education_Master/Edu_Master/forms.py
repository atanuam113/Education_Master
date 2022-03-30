from attr import fields
from django.contrib.auth.forms import UserCreationForm
from Edu_Master.models import User,Student_Profile,Events
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

class Admin_Event_edit(forms.ModelForm):
    class Meta:
        model = Events
        fields= ('Event_Name','Event_Topic','Event_Short_Desc','Event_Date','Event_Time','Event_End_Time','Event_Long_desc','Event_Dept','Event_Link','Event_Banner','Event_Status')