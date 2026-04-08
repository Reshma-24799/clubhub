from django.db import models
from django.contrib.auth.models import User

class Club(models.Model):
    """
    The organization hosting the events.
    """
    name = models.CharField(max_length=255, help_text="E.g., Computer Science Society")
    description = models.TextField(help_text="What the club does.")
    contact_email = models.EmailField(help_text="Official club email.")
    president = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clubs_managed', help_text="Links to the student who manages the club.")
    is_approved = models.BooleanField(default=False, help_text="A campus administrator must approve the club before they can post events.")

    def __str__(self):
        return self.name

class Event(models.Model):
    """
    The actual activity being hosted.
    """
    title = models.CharField(max_length=255, help_text="E.g., Spring Hackathon 2026")
    description = models.TextField(help_text="Details about the event.")
    date_and_time = models.DateTimeField(help_text="When it happens.")
    location = models.CharField(max_length=255, help_text="Room number or address.")
    hosting_club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='events', help_text="Which club is throwing this event.")
    max_capacity = models.IntegerField(help_text="Maximum number of total attendees allowed.")

    def __str__(self):
        return f"{self.title} by {self.hosting_club.name}"

class TicketType(models.Model):
    """
    Events can have free RSVP slots, paid VIP tickets, or member-only tickets.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ticket_types', help_text="The event this ticket is for.")
    name = models.CharField(max_length=100, help_text="E.g., General Admission, Early Bird, Free RSVP.")
    price = models.DecimalField(max_digits=6, decimal_places=2, help_text="Set to 0.00 for free events.")
    quantity_available = models.IntegerField(help_text="E.g., 50 Early Bird tickets available.")

    def __str__(self):
        return f"{self.name} for {self.event.title}"

class Registration(models.Model):
    """
    The bridge connecting a Student to an Event/Ticket (The RSVP action).
    """
    attendee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations', help_text="The student who clicked RSVP.")
    event_ticket = models.ForeignKey(TicketType, on_delete=models.CASCADE, related_name='registrations', help_text="The specific ticket they claimed.")
    registration_date = models.DateTimeField(auto_now_add=True, help_text="When they signed up.")
    has_attended = models.BooleanField(default=False, help_text="Can be checked off at the door.")

    def __str__(self):
        return f"{self.attendee.username} - {self.event_ticket.name}"