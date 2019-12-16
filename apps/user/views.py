from django.shortcuts import render, HttpResponse

# Create your views here.

from .models import User


def user(request):
    obj = User.objects.filter(id=1)
    print(obj[0].avatar_path)

    return HttpResponse('1')
