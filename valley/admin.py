from django.contrib import admin
from .models import Customer, Staff, Room, Booking, FoodMenu, Event, Notice

admin.site.register(Customer)
admin.site.register(Staff)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(FoodMenu)
admin.site.register(Event)
admin.site.register(Notice)