from django.shortcuts import render, HttpResponse


from .models import User


def user(request):
    obj = User.objects.filter(id=1)

    print(obj)

    return HttpResponse('1')
