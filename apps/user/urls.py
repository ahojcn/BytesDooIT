from django.urls import path

from user.views import UserView, UserActive, UserSession

urlpatterns = [
    path('', UserView.as_view()),
    path('active/', UserActive.as_view()),
    path('session/', UserSession.as_view()),
]
