from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from .models import Event, Club, TicketType, Registration

def home(request):
    events = Event.objects.all().order_by('date_and_time')
    return render(request, 'events/home.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    ticket_types = event.ticket_types.all()
    already_registered = False
    if request.user.is_authenticated:
        already_registered = Registration.objects.filter(attendee=request.user, event_ticket__event=event).exists()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
            
        ticket_id = request.POST.get('ticket_type')
        if ticket_id:
            ticket = get_object_or_404(TicketType, pk=ticket_id)
            # Check if user already registered for this event
            if Registration.objects.filter(attendee=request.user, event_ticket__event=event).exists():
                messages.warning(request, "You are already registered for this event!")
            elif ticket.quantity_available > 0:
                Registration.objects.create(attendee=request.user, event_ticket=ticket)
                ticket.quantity_available -= 1
                ticket.save()
                messages.success(request, f"Successfully registered for {event.title}!")
                return redirect('events:my_tickets')
            else:
                messages.error(request, "Sorry, this ticket type is sold out.")
                
    return render(request, 'events/event_detail.html', {'event': event, 'ticket_types': ticket_types, 'already_registered': already_registered})

@login_required
def my_tickets(request):
    registrations = Registration.objects.filter(attendee=request.user).order_by('-registration_date')
    return render(request, 'events/my_tickets.html', {'registrations': registrations})

@login_required
def unregister(request, registration_id):
    if request.method == 'POST':
        registration = get_object_or_404(Registration, pk=registration_id, attendee=request.user)
        ticket = registration.event_ticket
        registration.delete()
        ticket.quantity_available += 1
        ticket.save()
        messages.success(request, f"Successfully unregistered from {ticket.event.title}.")
    return redirect('events:my_tickets')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome to ClubHub.")
            return redirect('events:home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
