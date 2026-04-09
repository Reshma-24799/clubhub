from django.urls import path
from . import views

app_name = 'events'
urlpatterns = [
    path('', views.home, name='home'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('unregister/<int:registration_id>/', views.unregister, name='unregister'),
    path('signup/', views.signup, name='signup'),
]
