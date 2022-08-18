from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

path('register/',views.register,name='register'),
path('',views.login,name='login'),
path('forgotpass/',views.forgotpass,name='forgotpass'),
path('LogOut/',views.LogOut,name='LogOut'),
path('loginpage/',views.login,name='loginpage'),
path('LoginWithOTP/',views.LoginWithOTP,name='LoginWithOTP'),
path("activate/<uidb64>/<token>/",views.activate,name="activate"),

#Student section
path('home/',views.home,name='home'),
path('about/',views.about,name='about'),
path('award/',views.award,name='award'),
path('research/',views.research,name='research'),
path('facilities/',views.facilities,name='facilities'),
path('student_search/',views.student_search,name='student_search'),
path('facilities_detail/',views.facilities_detail,name='facilities_detail'),
path('departments/',views.departments,name='departments'),
path('all_course/',views.all_course,name='all_course'),
path('seminar/',views.seminar,name='seminar'),
path('course_details/',views.course_details,name='course_details'),
path('blog/',views.blog,name='blog'),
path('blog_details/',views.blog_details,name='blog_details'),
path('contact_us/',views.contact_us,name='contact_us'),
path('event/',views.event,name='event'),
path('event_register/<slug:slug>',views.event_register,name='event_register'),
path('event_details/<slug:slug>',views.event_details,name='event_details'),
path('student_dashboard/',views.student_dashboard,name='student_dashboard'),
path('student_profile/',views.student_profile,name='student_profile'),
path('student_course/',views.student_course,name='student_course'),
path('student_exam/',views.student_exam,name='student_exam'),
path('student_class_time/',views.student_class_time,name='student_class_time'),
path('student_Profile_Edit/<int:pk>',views.student_Profile_Edit,name='student_Profile_Edit'),
path('all_trainer/',views.all_trainer,name='all_trainer'),

# Library Section
# path('library_home/', views.library_home.as_view(), name='library_home'),
path('Library_Login/', views.Library_Login, name='Library_Login'),
path('Library_Signup/', views.Library_Signup, name='Library_Signup'),
path('Library_ForgotPassword/', views.Library_ForgotPassword, name='Library_ForgotPassword'),
path('Library_ChangePassword/', views.Library_ChangePassword, name='Library_ChangePassword'),
path('search_book/', views.search_book, name='search_book'),
path('Library_Index/', views.Library_Index.as_view(), name='Library_Index'),
path('Library_Book_Media/', views.Library_Book_Media.as_view(), name='Library_Book_Media'),
path('Library_News_Event/', views.Library_News_Event, name='Library_News_Event'),
path('Library_Blog/', views.Library_Blog, name='Library_Blog'),
path('Library_Blog_Detail/', views.Library_Blog_Detail, name='Library_Blog_Detail'),
path('Library_Services/', views.Library_Services, name='Library_Services'),
path('Library_Single_Book/<int:pk>', views.Library_Single_Book.as_view(), name='Library_Single_Book'),
# path('Library_Audio_Book/<int:pk>',views.Library_Audio_Book,name='Library_Audio_Book'),
path('Library_Book_Request/', views.Library_Book_Request, name='Library_Book_Request'),


#Admin Section
path('admin_dashboard1/',views.admin_dashboard1,name='admin_dashboard1'),
path('admin_notification/',views.admin_notification.as_view(),name='admin_notification'),
path('admin_account_setting/',views.admin_account_setting,name='admin_account_setting'),
path('admin_search/',views.admin_search,name='admin_search'),
path('admin_notification_details/<int:pk>',views.admin_notification_details,name='admin_notification_details'),
path('Admin_personal_details_edit/<int:pk>',views.Admin_personal_details_edit,name='Admin_personal_details_edit'),

path('admin_all_course/',views.admin_all_course,name='admin_all_course'),
path('admin_add_course/',views.admin_add_course,name='admin_add_course'),
path('admin_course_details/<int:pk>',views.admin_course_details,name='admin_course_details'),

path('admin_all_teacher/',views.admin_all_teacher,name='admin_all_teacher'),
path('admin_add_teacher/',views.admin_add_teacher,name='admin_add_teacher'),
path('admin_teacher_details/<int:pk>',views.admin_teacher_details,name='admin_teacher_details'),

path('admin_all_student/',views.admin_all_student,name='admin_all_student'),
path('admin_add_student/',views.admin_add_student,name='admin_add_student'),
path('admin_student_details/<int:pk>',views.admin_student_details,name='admin_student_details'),

path('admin_all_librarian/',views.admin_all_librarian,name='admin_all_librarian'),
path('admin_add_librarian/',views.admin_add_librarian,name='admin_add_librarian'),
path('admin_librarian_details/<int:pk>',views.admin_librarian_details,name='admin_librarian_details'),

path('admin_all_user/',views.admin_all_user,name='admin_all_user'),
path('admin_add_librarian/',views.admin_add_librarian,name='admin_add_librarian'),
path('admin_user_details/<int:pk>',views.admin_user_details,name='admin_user_details'),

path('admin_all_contact/',views.admin_all_contact,name='admin_all_contact'),
# path('admin_add_librarian/',views.admin_add_librarian,name='admin_add_librarian'),
path('admin_contact_response/<int:pk>',views.admin_contact_response,name='admin_contact_response'),

path('admin_all_events/',views.admin_all_events,name='admin_all_events'),
path('admin_add_event/',views.admin_add_event,name='admin_add_event'),
path('admin_event_details/<int:pk>',views.admin_event_details,name='admin_event_details'),

path('admin_all_exam/',views.admin_all_exam,name='admin_all_exam'),
path('admin_add_exam/',views.admin_add_exam,name='admin_add_exam'),
path('admin_exam_details/',views.admin_exam_details,name='admin_exam_details'),
path('admin_all_groups/',views.admin_all_groups,name='admin_all_groups'),
path('admin_add_group/',views.admin_add_group,name='admin_add_group'),

path('admin_all_enquiry/',views.admin_all_enquiry,name='admin_all_enquiry'),
path('admin_course_enquiry/',views.admin_course_enquiry,name='admin_course_enquiry'),
path('admin_admission_enquiry/',views.admin_admission_enquiry,name='admin_admission_enquiry'),
path('admin_seminar_enquiry/',views.admin_seminar_enquiry,name='admin_seminar_enquiry'),
path('admin_event_enquiry/',views.admin_event_enquiry,name='admin_event_enquiry'),
path('admin_common_enquiry/',views.admin_common_enquiry,name='admin_common_enquiry'),
path('admin_view_enquiry/',views.admin_view_enquiry,name='admin_view_enquiry'),

# Teacher Section
path('teacher_dashboard/',views.teacher_dashboard,name='teacher_dashboard'),


# Librarian Section 
path('librarian_dashboard/',views.librarian_dashboard,name='librarian_dashboard'),
path('add_book/',views.add_book,name='add_book'),
path('librarian_search/',views.librarian_search,name='librarian_search'),
path('manage_book/', views.manage_book.as_view(), name='manage_book'),
path('recent_book/', views.recent_book.as_view(), name='recent_book'),
path('library_register/', views.library_register.as_view(), name='library_register'),
path('view_book/<int:pk>', views.view_book.as_view(), name='view_book'),
path('edit_book/<int:pk>', views.edit_book.as_view(), name='edit_book'),
path('delete_book/<int:pk>', views.delete_book.as_view(), name='delete_book'),
path('library_register_details/<int:pk>', views.library_register_details, name='library_register_details'),
path('book_request/', views.book_request, name='book_request'),
path('book_request_details/<int:pk>', views.book_request_details, name='book_request_details'),

]