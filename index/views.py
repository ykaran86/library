from django.shortcuts import render
from .models import Dialog
from django.http import HttpResponse, JsonResponse
from datetime import datetime
import sqlite3

def home(request):
    return render(request, 'home.html', {'home':'active'})

def dialog(request):
    if request.method == "POST":
        dialogue = request.POST.get('querybox', None)
        q1 = Dialog(query = dialogue)
        myDate = datetime.now()
        formatedDate = myDate.strftime("%b %d, %Y, %I:%M %p")
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("SELECT count(*) from book")
        x=c.fetchone()[0]
        conn.close()
        return JsonResponse({ 'dialog':dialogue, 'time':formatedDate, 'reply':x })
    else:
        return HttpResponse('Request must be POST.')
