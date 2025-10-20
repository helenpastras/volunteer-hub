from django.shortcuts import render

from django.http import HttpResponse


def home(request):
    # Send a simple HTML response
    return HttpResponse('<h1>Hello and Welcme to the amazing Volunteer Hub.</h1>')
