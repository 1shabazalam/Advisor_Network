from django.urls import path, include
from .views import LoginView, RegisterView, UserView, AddAdvisorView, AdvisorListView,BookAdvisorView, BookedListView, LogoutView
# from rest_framework import routers
from . import views

urlpatterns = [
    path('admin/advisor', AddAdvisorView.as_view()),
    path('user/register',RegisterView.as_view()),
    path('user/login',LoginView.as_view()),
    path('user/user', UserView.as_view()),
    path('user/logout', LogoutView.as_view()),
    path('user/<user_id>/advisor', AdvisorListView.as_view()),
    path('user/<user_id>/advisor/booking', BookedListView.as_view()),
    path('user/<user_id>/advisor/<advisor_id>', BookAdvisorView.as_view()),
    
]