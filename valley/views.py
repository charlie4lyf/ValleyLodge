from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from valley.forms import UserRegisterForm, UsernameLoginForm
from valley.models import Booking, Customer, Event, FoodMenu, Notice, Room, Staff
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Create User
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            # Create Profile
            Customer.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number']
            )
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'credentials/register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = UsernameLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin_dashboard')
                return redirect('home')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = UsernameLoginForm()
    return render(request, 'credentials/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('home')

#Administrator views
def is_admin_or_superuser(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@login_required
@user_passes_test(is_admin_or_superuser)
def admin_dashboard(request):
    total_customers = Customer.objects.count()
    total_bookings = Booking.objects.count()
    total_rooms = Room.objects.count()
    total_food_items = FoodMenu.objects.count()
    total_events = Event.objects.count()

    total_revenue = sum(booking.total_price for booking in Booking.objects.all())

    recent_bookings = Booking.objects.all().order_by('-id')[:5]

    context = {
        'total_customers': total_customers,
        'total_bookings': total_bookings,
        'total_rooms': total_rooms,
        'total_food_items': total_food_items,
        'total_events': total_events,
        'total_revenue': total_revenue,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'admin_side/dashboard.html', context)

@login_required
@user_passes_test(is_admin_or_superuser)
def manage_customers(request):
    query = request.GET.get('search', '')
    if query:
        # Search by username or email (from the User model)
        customers = Customer.objects.filter(
            user__username__icontains=query
        ) | Customer.objects.filter(
            user__email__icontains=query
        )
    else:
        customers = Customer.objects.all()
    return render(request, 'admin_side/manage_customers.html', {'customers': customers})

@login_required
@user_passes_test(is_admin_or_superuser)
def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    customer.delete()
    return redirect('manage_customers')

@login_required
@user_passes_test(is_admin_or_superuser)
def manage_staff(request):
    query = request.GET.get('search', '')
    if query:
        # Search by name, surname, or email
        staff = Staff.objects.filter(
            name__icontains=query
        ) | Staff.objects.filter(
            surname__icontains=query
        ) | Staff.objects.filter(
            email__icontains=query
        )
    else:
        staff = Staff.objects.all()
    return render(request, 'admin_side/manage_staff.html', {'staff': staff})

@login_required
@user_passes_test(is_admin_or_superuser)
def add_staff(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        # Create a new Staff instance
        Staff.objects.create(
            name=name,
            surname=surname,
            email=email,
            phone_number=phone_number
        )
        return redirect('manage_staff')
    return render(request, 'admin_side/add_staff.html')

@login_required
@user_passes_test(is_admin_or_superuser)
def edit_staff(request, staff_id):
    staff_member = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        staff_member.name = request.POST.get('name')
        staff_member.surname = request.POST.get('surname')
        staff_member.email = request.POST.get('email')
        staff_member.phone_number = request.POST.get('phone_number')
        staff_member.save()
        return redirect('manage_staff')
    return render(request, 'admin_side/edit_staff.html', {'staff_member': staff_member})

@login_required
@user_passes_test(is_admin_or_superuser)
def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    staff.delete()
    return redirect('manage_staff')

@login_required
@user_passes_test(is_admin_or_superuser)
def manage_rooms(request):
    query = request.GET.get('search', '')
    if query:
        # Search by room number or room type
        rooms = Room.objects.filter(
            room_name__icontains=query
        ) | Room.objects.filter(
            room_type__icontains=query
        )
    else:
        rooms = Room.objects.all()
    return render(request, 'admin_side/manage_rooms.html', {'rooms': rooms})

@login_required
@user_passes_test(is_admin_or_superuser)
def add_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        room_type = request.POST.get('room_type')
        price = request.POST.get('price')
        is_available = request.POST.get('is_available') == 'True'
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        description = request.POST.get('description')
        
        # Create a new Room instance
        Room.objects.create(
            room_name=room_name,
            room_type=room_type,
            price=price,
            is_available=is_available,
            image1=image1,
            image2=image2,
            image3=image3,
            description=description
        )
        return redirect('manage_rooms')
        
    return render(request, 'admin_side/add_room.html')

@login_required
@user_passes_test(is_admin_or_superuser)
def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        room.room_name = request.POST.get('room_name')
        room.room_type = request.POST.get('room_type')
        room.price = request.POST.get('price')
        room.is_available = request.POST.get('is_available') == 'True'
        
        if request.FILES.get('image1'):
            room.image1 = request.FILES.get('image1')
        if request.FILES.get('image2'):
            room.image2 = request.FILES.get('image2')
        if request.FILES.get('image3'):
            room.image3 = request.FILES.get('image3')
        
        room.description = request.POST.get('description')
        room.save()
        return redirect('manage_rooms')
        
    return render(request, 'admin_side/edit_room.html', {'room': room})

@login_required
@user_passes_test(is_admin_or_superuser)
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.delete()
    return redirect('manage_rooms')

@login_required
@user_passes_test(is_admin_or_superuser)
def manage_bookings(request):
    query = request.GET.get('search', '')
    if query:
        # Search by customer name, room number, or booking ID
        bookings = Booking.objects.filter(
            customer__user__username__icontains=query
        ) | Booking.objects.filter(
            room__room_name__icontains=query
        ) | Booking.objects.filter(
            id__icontains=query
        )
    else:
        bookings = Booking.objects.all()
    return render(request, 'admin_side/manage_bookings.html', {'bookings': bookings})

@login_required
@user_passes_test(is_admin_or_superuser)
def add_booking(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        room_id = request.POST.get('room')
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')
        is_approved = request.POST.get('is_approved') == 'True'
        # Create a new Booking instance
        Booking.objects.create(
            customer_id=customer_id,
            room_id=room_id,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            is_approved=is_approved
        )
        return redirect('manage_bookings')
    customers = Customer.objects.all()
    rooms = Room.objects.all()
    return render(request, 'admin_side/add_booking.html', {'customers': customers, 'rooms': rooms})

@login_required
@user_passes_test(is_admin_or_superuser)
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.customer_id = request.POST.get('customer')
        booking.room_id = request.POST.get('room')
        booking.check_in_date = request.POST.get('check_in_date')
        booking.check_out_date = request.POST.get('check_out_date')
        booking.is_approved = request.POST.get('is_approved') == 'True'
        booking.save()
        return redirect('manage_bookings')
    customers = Customer.objects.all()
    rooms = Room.objects.all()
    return render(request, 'admin_side/edit_booking.html', {'booking': booking, 'customers': customers, 'rooms': rooms})

@login_required
@user_passes_test(is_admin_or_superuser)
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    return redirect('manage_bookings')

@login_required
@user_passes_test(is_admin_or_superuser)
def manage_food_menu(request):
    query = request.GET.get('search', '')
    if query:
        # Search by food name or category
        food_items = FoodMenu.objects.filter(
            name__icontains=query
        ) | FoodMenu.objects.filter(
            category__icontains=query
        )
    else:
        food_items = FoodMenu.objects.all()
    return render(request, 'admin_side/manage_food_menu.html', {'food_items': food_items})

@login_required
@user_passes_test(is_admin_or_superuser)
def add_food_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        price = request.POST.get('price')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        description = request.POST.get('description')
        
        # Create a new FoodMenu instance
        FoodMenu.objects.create(
            name=name,
            category=category,
            price=price,
            image1=image1,
            image2=image2,
            image3=image3,
            description=description
        )
        return redirect('manage_food_menu')
        
    return render(request, 'admin_side/add_food_item.html')

@login_required
@user_passes_test(is_admin_or_superuser)
def edit_food_item(request, food_id):
    food_item = get_object_or_404(FoodMenu, id=food_id)
    if request.method == 'POST':
        food_item.name = request.POST.get('name')
        food_item.category = request.POST.get('category')
        food_item.price = request.POST.get('price')
        
        # Update images only if new files are uploaded; otherwise, keep existing images.
        if request.FILES.get('image1'):
            food_item.image1 = request.FILES.get('image1')
        if request.FILES.get('image2'):
            food_item.image2 = request.FILES.get('image2')
        if request.FILES.get('image3'):
            food_item.image3 = request.FILES.get('image3')
            
        food_item.description = request.POST.get('description')
        food_item.save()
        return redirect('manage_food_menu')
        
    return render(request, 'admin_side/edit_food_item.html', {'food_item': food_item})

@login_required
@user_passes_test(is_admin_or_superuser)
def delete_food_item(request, food_id):
    food_item = get_object_or_404(FoodMenu, id=food_id)
    food_item.delete()
    return redirect('manage_food_menu')

@login_required
@user_passes_test(is_admin_or_superuser)
def manage_events(request):
    query = request.GET.get('search', '')
    if query:
        # Search by event name or date
        events = Event.objects.filter(
            name__icontains=query
        ) | Event.objects.filter(
            date__icontains=query
        )
    else:
        events = Event.objects.all()
    return render(request, 'admin_side/manage_events.html', {'events': events})

@login_required
@user_passes_test(is_admin_or_superuser)
def add_event(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        price = request.POST.get('price')
        capacity = request.POST.get('capacity')
        description = request.POST.get('description')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        
        # Create a new Event instance
        Event.objects.create(
            name=name,
            date=date,
            price=price,
            capacity=capacity,
            description=description,
            image1=image1,
            image2=image2,
            image3=image3
        )
        return redirect('manage_events')
        
    return render(request, 'admin_side/add_event.html')

@login_required
@user_passes_test(is_admin_or_superuser)
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.name = request.POST.get('name')
        event.date = request.POST.get('date')
        event.price = request.POST.get('price')
        event.capacity = request.POST.get('capacity')
        event.description = request.POST.get('description')
        
        # Update each image only if a new file is uploaded
        if request.FILES.get('image1'):
            event.image1 = request.FILES.get('image1')
        if request.FILES.get('image2'):
            event.image2 = request.FILES.get('image2')
        if request.FILES.get('image3'):
            event.image3 = request.FILES.get('image3')
        
        event.save()
        return redirect('manage_events')
        
    return render(request, 'admin_side/edit_event.html', {'event': event})

@login_required
@user_passes_test(is_admin_or_superuser)
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect('manage_events')

@login_required
@user_passes_test(is_admin_or_superuser)
def manage_notices(request):
    query = request.GET.get('search', '')
    if query:
        # Search by title or content
        notices = Notice.objects.filter(
            title__icontains=query
        ) | Notice.objects.filter(
            content__icontains=query
        )
    else:
        notices = Notice.objects.all()
    return render(request, 'admin_side/manage_notices.html', {'notices': notices})

@login_required
@user_passes_test(is_admin_or_superuser)
def add_notice(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        expiry_date = request.POST.get('expiry_date')
        # Create a new Notice instance
        Notice.objects.create(
            title=title,
            content=content,
            expiry_date=expiry_date
        )
        return redirect('manage_notices')
    return render(request, 'admin_side/add_notice.html')

@login_required
@user_passes_test(is_admin_or_superuser)
def edit_notice(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    if request.method == 'POST':
        notice.title = request.POST.get('title')
        notice.content = request.POST.get('content')
        notice.expiry_date = request.POST.get('expiry_date')
        notice.save()
        return redirect('manage_notices')
    return render(request, 'admin_side/edit_notice.html', {'notice': notice})

@login_required
@user_passes_test(is_admin_or_superuser)
def delete_notice(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    notice.delete()
    return redirect('manage_notices')

#Customer or user views
def home(request):
    return render(request, 'user_side/home.html')

def room_list(request):
    # Fetch all rooms
    rooms = Room.objects.all()

    # Search filter
    room_type = request.GET.get('room_type', None)
    if room_type:
        rooms = rooms.filter(room_type=room_type)

    # Price range filter
    price_range = request.GET.get('price_range', None)
    if price_range:
        min_price, max_price = price_range.split('-')
        rooms = rooms.filter(price__gte=min_price, price__lte=max_price)

    # Availability filter
    is_available = request.GET.get('is_available', None)
    if is_available is not None:
        rooms = rooms.filter(is_available=is_available.lower() == 'true')

    return render(request, 'user_side/room_list.html', {'rooms': rooms})

def book_room(request, room_id):
    if request.method == 'POST':
        room = get_object_or_404(Room, id=room_id)
        customer = Customer.objects.get(user=request.user)
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')

        # Convert dates to datetime objects
        check_in = datetime.strptime(check_in_date, '%Y-%m-%d').date()
        check_out = datetime.strptime(check_out_date, '%Y-%m-%d').date()

        # Calculate number of days
        days_diff = (check_out - check_in).days
        if days_diff <= 0:
            messages.error(request, 'Invalid date range. Check-out date must be after check-in date.')
            return redirect('room_list')

        # Calculate total price
        total_price = room.price * days_diff

        # Create a new booking
        booking = Booking.objects.create(
            customer=customer,
            room=room,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            total_price=total_price
        )

        # Redirect to the booking confirmation page
        return redirect('booking_confirmation', booking_id=booking.id)

    return redirect('room_list')

def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'user_side/booking_confirmation.html', {'booking': booking})

def food_list(request):
    # Fetch all food items
    foods = FoodMenu.objects.all()

    # Optional: Add filters for category or price range
    category = request.GET.get('category', None)
    if category:
        foods = foods.filter(category=category)

    return render(request, 'user_side/food_list.html', {'foods': foods})

def event_list(request):
    # Fetch all events
    events = Event.objects.all()

    # Optional: Add filters for date or price range
    date_filter = request.GET.get('date', None)
    if date_filter:
        events = events.filter(date=date_filter)

    return render(request, 'user_side/event_list.html', {'events': events})

def user_profile(request):
    # Fetch the logged-in user's customer profile
    customer = Customer.objects.get(user=request.user)
    
    # Fetch the user's bookings
    bookings = Booking.objects.filter(customer=customer)

    # Handle password change form
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'user_side/user_profile.html', {
        'customer': customer,
        'bookings': bookings,
        'form': form,
    })

