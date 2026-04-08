from django.contrib import admin
from .models import Club, Event, TicketType, Registration

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'hosting_club', 'date_and_time', 'location', 'max_capacity')
    list_filter = ('hosting_club', 'date_and_time')
    search_fields = ('title', 'location')

@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'price', 'quantity_available')
    list_filter = ('event',)

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('attendee', 'event_ticket', 'registration_date', 'has_attended')
    list_filter = ('has_attended', 'event_ticket__event')
    search_fields = ('attendee__username',)