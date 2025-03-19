from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import UserPassesTestMixin


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class SuperuserPasswordChangeView(SuperuserRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'admin_side/change_password.html'
    success_url = '/admin-dashboard/'

urlpatterns = [
   
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
   

    path('manage-customers/', views.manage_customers, name='manage_customers'),
    path('delete-customer/<int:customer_id>/', views.delete_customer, name='delete_customer'),

    # Staff URLs
    path('manage-staff/', views.manage_staff, name='manage_staff'),
    path('add-staff/', views.add_staff, name='add_staff'),
    path('edit-staff/<int:staff_id>/', views.edit_staff, name='edit_staff'),
    path('delete-staff/<int:staff_id>/', views.delete_staff, name='delete_staff'),

    # Room URLs
    path('manage-rooms/', views.manage_rooms, name='manage_rooms'),
    path('add-room/', views.add_room, name='add_room'),
    path('edit-room/<int:room_id>/', views.edit_room, name='edit_room'),
    path('delete-room/<int:room_id>/', views.delete_room, name='delete_room'),

    # Booking URLs
    path('manage-bookings/', views.manage_bookings, name='manage_bookings'),
    path('add-booking/', views.add_booking, name='add_booking'),
    path('edit-booking/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),

    # Food Menu URLs
    path('manage-food-menu/', views.manage_food_menu, name='manage_food_menu'),
    path('add-food-item/', views.add_food_item, name='add_food_item'),
    path('edit-food-item/<int:food_id>/', views.edit_food_item, name='edit_food_item'),
    path('delete-food-item/<int:food_id>/', views.delete_food_item, name='delete_food_item'),

    # Event URLs
    path('manage-events/', views.manage_events, name='manage_events'),
    path('add-event/', views.add_event, name='add_event'),
    path('edit-event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete-event/<int:event_id>/', views.delete_event, name='delete_event'),

    # Notice URLs
    path('manage-notices/', views.manage_notices, name='manage_notices'),
    path('add-notice/', views.add_notice, name='add_notice'),
    path('edit-notice/<int:notice_id>/', views.edit_notice, name='edit_notice'),
    path('delete-notice/<int:notice_id>/', views.delete_notice, name='delete_notice'),

    path('change-password/', SuperuserPasswordChangeView.as_view(), name='change_password'),

    path('', views.home, name='home'),
    path('rooms/', views.room_list, name='room_list'),
    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),

    path('foods/', views.food_list, name='food_list'),
    path('events/', views.event_list, name='event_list'), 

    path('profile/', views.user_profile, name='profile'), 
]