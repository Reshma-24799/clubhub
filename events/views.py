from django.shortcuts import render
from .models import Event

def home(request):
    events = Event.objects.all().order_by('date_and_time')
    return render(request, 'events/home.html', {'events': events})