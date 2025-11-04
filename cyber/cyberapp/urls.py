from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('students/', views.students_list, name='students_list'),
    path('students/<str:idnumber>/', views.student_detail, name='student_detail'),
    path('payments/', views.payment_list, name='payment_list'),
    path('students/<str:idnumber>/payments/', views.student_payments, name='student_payments'),
    path('add_student/', views.add_student, name='add_student'),
    path('add_payment/', views.add_payment, name='add_payment'),
    path('delete_student/<str:idnumber>/', views.delete_student, name='delete_student'),
    path('delete_payment/<int:payment_id>/', views.delete_payment, name='delete_payment'),
    path('update_student/<str:idnumber>/', views.update_student, name='update_student'),
    path('sessions/active/', views.active_sessions, name= "active_sessions"),
    path('sessions/start/<str:idnumber>/', views.start_session, name='start_session'),
    path('sessions/end/<str:idnumber>/', views.end_session, name='end_session'),
    path('login/', views.login_view, name='login'),




    ]