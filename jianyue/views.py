__author__ = 'boyang'

from django.shortcuts import render_to_response


def home(request):
    return render_to_response('index.html')


def test(request):
    return render_to_response('test.html')


def player(request):
    return render_to_response('player.html')


def door(request):
    return render_to_response('door.html')


def login(request):
    return render_to_response('login.html')


def bug(request):
    return render_to_response('bug.html')

