from django.shortcuts import render
from . import sleep

# Create your views here.

def post_list(request):
    sleepEfficiency = sleep.sleepEfficiency
    return render(request, 'blog/post_list.html', {'sleepEfficiency': sleepEfficiency})

def animation(request):
    return render(request, 'blog/animation.html', {})
