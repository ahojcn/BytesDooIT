from django.urls import path

from user.views import (
    UserView,
    UserActiveView,
    UserSessionView,
    TestView,
)

urlpatterns = [
    path('', UserView.as_view()),
    path('active/', UserActiveView.as_view()),
    path('session/', UserSessionView.as_view()),

    path('test/', TestView.as_view())
]
