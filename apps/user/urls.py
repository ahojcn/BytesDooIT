from django.urls import path

from apps.user.views import user

urlpatterns = [
    path('', user),
]
