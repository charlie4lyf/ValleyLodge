from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12)

    def __str__(self):
        return self.user.username
    
class Staff(models.Model):
    name = models.CharField(max_length=15)
    surname = models.CharField(max_length=15)
    email = models.EmailField(max_length=25, unique=True)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Room(models.Model):
    ROOM_TYPES = [
        ('Standard', 'Standard'),
        ('Deluxe', 'Deluxe'),
        ('Suite', 'Suite'),
    ]
    room_name = models.CharField(max_length=25, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    image1 = models.ImageField(upload_to='iamges/room_images/', null=True, blank=True)
    image2 = models.ImageField(upload_to='images/room_images/', null=True, blank=True)
    image3 = models.ImageField(upload_to='images/room_images/', null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.room_name} - {self.room_type}"
    

class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    is_approved = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.customer.user.username} - {self.room.room_name}"


class FoodMenu(models.Model):
    CATEGORIES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snacks', 'Snacks'),
    ]
    name = models.CharField(max_length=25)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image1 = models.ImageField(upload_to='images/food_images/', null=True, blank=True)
    image2 = models.ImageField(upload_to='images/food_images/', null=True, blank=True)
    image3 = models.ImageField(upload_to='images/food_images/', null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Event(models.Model):
    name = models.CharField(max_length=25)
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()
    description = models.TextField()
    image1 = models.ImageField(upload_to='images/event_images/', null=True, blank=True)
    image2 = models.ImageField(upload_to='images/event_images/', null=True, blank=True)
    image3 = models.ImageField(upload_to='images/event_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Notice(models.Model):
    title = models.CharField(max_length=25)
    content = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()

    def __str__(self):
        return self.title