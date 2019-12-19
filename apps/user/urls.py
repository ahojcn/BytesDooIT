from django.urls import path

from user.views import UserView, UserActive

urlpatterns = [
    path('', UserView.as_view()),
    path('active/', UserActive.as_view()),
]
