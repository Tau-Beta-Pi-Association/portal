from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
import pymssql

def index(request):
    messages_to_display = messages.get_messages(request)
    return render(request, 'registration/index.html', {'messages':messages_to_display})