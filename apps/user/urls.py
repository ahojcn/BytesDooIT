from django.urls import path

from user.views import (
    UserView,
    UserActiveView,
    UserSessionView,
)

urlpatterns = [
    path('', UserView.as_view()),
    path('active/', UserActiveView.as_view()),
    path('session/', UserSessionView.as_view()),
]
