from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.projecthomepage, name='projecthomepage'),
    path('printpagecall/', views.printpagecall, name='printpagecall'),
    path('printpagelogic/', views.printpagelogic, name='printpagelogic'),
    path('exceptionpagecall/', views.exceptionpagecall, name='exceptionpagecall'),
    path('exceptionpagelogic/', views.exceptionpagelogic, name='exceptionpagelogic'),
    path('randompagecall/', views.randompagecall, name='randompagecall'),
    path('randomlogic/', views.randomlogic, name='randomlogic'),
    path('calculatorpagecall/', views.calculatorpagecall, name='calculatorpagecall'),
    path('calculatorlogic/', views.calculatorlogic, name='calculatorlogic'),
    path('datetimepagecall/', views.datetimepagecall, name='datetimepagecall'),
    path('datetimepagelogic/', views.datetimepagelogic, name='datetimepagelogic'),
    path('add_task/', views.add_task, name='add_task'),
    path('<int:pk>/delete/', views.delete_task, name='delete_task'),
    path('register/', views.UserRegisterPageCall, name='UserRegisterPageCall'),
    path('register/submit/', views.UserRegisterLogic, name='UserRegisterLogic'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.user_login, name='login'),
    path('add_post/', views.add_post, name='add_post'),
    path('<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('facultyhomepage/', views.facultyhomepage, name='facultyhomepage'),
    path('studenthomepage/', views.studenthomepage, name='studenthomepage'),
    path('add_details/', views.add_student, name='add_details'),
    path('show_details/', views.student_list, name='show_details'),
    path('post_marks/', views.student_list, name='post_marks'),
]
