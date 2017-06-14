from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth.models import User
from datetime import datetime

from website.forms import UserForm, TripForm, PaymentTypeForm, OrderForm
from website.models import Trip, TripType, PaymentType, TripOpinion, Order, TripOrder, Customer, WishList
from django.db.models import Q

# standard Django view: query, template name, and a render method to render the data from the query into the template

def index(request):
    """
    Purpose: renders the index page with a list of 20 (max) trips
    Args: request -- the full HTTP request object
    Returns: rendered view of the index page, with a list of trips
    """
    all_trips = Trip.objects.all().order_by('-id')[:15]
    template_name = 'index.html'
    return render(request, template_name, {'trips': all_trips})


def register(request):
    """Handles the creation of a new user for authentication
    Method arguments:
      request -- The full HTTP request object
    """

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            #Saves customer once user created
            customer = Customer(user_id=user.id)
            customer.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        return login_user(request)

    elif request.method == 'GET':
        user_form = UserForm()
        template_name = 'register.html'
        return render(request, template_name, {'user_form': user_form})

def login_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Use the built-in authenticate method to verify
        username=request.POST['username']
        password=request.POST['password']
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, log the user in
        if authenticated_user is not None:
            login(request=request, user=authenticated_user)
            return HttpResponseRedirect('/')

        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {}, {}".format(username, password))
            return HttpResponse("Invalid login details supplied.")


    return render(request, 'login.html', {}, context)

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage. Is there a way to not hard code
    # in the URL in redirects?????
    return HttpResponseRedirect('/')

@login_required(login_url='/login')
def sell_trip(request):
    """
    Purpose: to present the user with a form to upload information about a trip to sell
    Args: request -- the full HTTP request object
    Returns: a form that lets a user upload a trip to sell
    """
    if request.method == 'GET':
        trip_form = TripForm()
        template_name = 'create.html'
        return render(request, template_name, {'trip_form': trip_form})

    elif request.method == 'POST':
        form = TripForm(request.POST, request.FILES)
        form_data = request.POST
        
        if form.is_valid():

            trip = Trip()

            trip.seller = request.user
            trip.title = form.cleaned_data['title']
            trip.description = form.cleaned_data['description']
            trip.price = form.cleaned_data['price']
            trip.quantity = form.cleaned_data['quantity']
            trip.trip_type = TripType.objects.get(pk=form_data['trip_type'])
            trip.trip_img = form.cleaned_data['trip_img']
            trip.city = form.cleaned_data['city']

            trip.save()

            return render(request, 'success.html', {})
        else:
            return HttpResponse('Failure Submitting Form')      

def list_trips(request):
    """
    Purpose: to render a view with a list of all trips
    Args: request -- the full HTTP request object
    Returns: a rendered view of a list of trips
    """
    all_trips = Trip.objects.all()
    template_name = 'list.html'
    return render(request, template_name, {'trips': all_trips})

def single_trip(request, trip_id):
    """
    Purpose: Allows user to view trip_detail view, which contains a very specific view
        for a singular trip
        For an example, visit /trip_details/1/ to see a view on the first trip created
        displaying title, description, quantity, price/unit, and "Add to order" button
    Args: trip_id: (integer): id of trip we are viewing 
    Returns: (render): a view of the request, template to use, and trip obj
    """
    if request.method == 'POST':
        wishlist = request.POST['wishlist']
        current_customer = request.user.id
        current_user = User.objects.get(pk=current_customer)
        current_trip = Trip.objects.get(pk=trip_id)

        try:
            wish_list = WishList.objects.create(trip=current_trip, customer=current_user)
        except:
            wish_list = WishList.objects.create(trip=current_trip, customer=current_user, wishlist=wishlist)

        back_to_trip = '/single_trip/' + trip_id
        return HttpResponseRedirect(back_to_trip)

    elif request.method == 'GET':
        template_name = 'single.html'
        trip = get_object_or_404(Trip, pk=trip_id)            
        return render(request, template_name, {"trip": trip})


@login_required(login_url='/login')
def user_wishlist(request):    
    """
    Purpose: Return the list of trips a user has added to their wishlist
    Args: request -- the full HTTP request object
    Returns: List of trips on the current user's wishlist
    """
    user_wishlist = WishList.objects.filter(customer = request.user)
    template_name = 'user_wishlist.html'
    return render(request, template_name, {"user_wishlist": user_wishlist})

def list_trip_types(request):
    """
    Purpose: To retrieve a list of all trips & trip_types from
    their respective tables so that a template may sort through and filter
    the results.
    Args: None
    Returns: Combines a given template with a given context dictionary and 
    returns an HttpResponse object with that rendered text.
    """
    trip_types = TripType.objects.all().order_by('-pk')

    for tt in trip_types:
        tt.num_trips = tt.trip_set.filter(trip_type=tt.id).count()
        tt.trips = tt.trip_set.filter(trip_type=tt.id).order_by('-pk')[:3]

    return render(request, 'trip_types.html', {'trip_types': trip_types})

def get_trip_types(request, type_id):
    """
    Purpose: To allow a hyperlink to a specific URL (with the parameter type_id)
    to display a trip category, and a list of trips assigned to that category
    and their trips.
    Args: type_id
    Returns: Combines a given template with a given context dictionary and 
    returns an HttpResponse object with that rendered text.
    """
    trip_types = TripType.objects.all().filter(pk=type_id)
    trips_of_type = Trip.objects.all().filter(trip_type=type_id)

    context = { 'trip_types' : trip_types, 'trips_of_type' : trips_of_type }
    
    return render(request, 'trip_type_trips.html', context )

@login_required(login_url='/login')
def profile(request): 
    """
    Purpose: to render the profile page in the browser
    Args: request -- the full HTTP request object
    Returns: renders the profile template in the browser
    """

    try:
        past_orders = Order.objects.all().filter(customer=request.user, active=0)
    except: 
        alert('There is no Order History for this customer.')
    current_user = request.user
    customer = Customer.objects.get(user_id=current_user.id)

    template_name = 'profile.html'
    return render(request, template_name, {'past_orders': past_orders, 'customer': customer})


@login_required(login_url='/login')
def add_payment_type(request):
    """
    Purpose: to present the user with a form to add a payment type to their account
    Args: request -- the full HTTP request object
    Returns: a form that lets a user add a payment type to their account
    """
    if request.method == 'GET':
        payment_type_form = PaymentTypeForm()
        template_name = 'add_payment_type.html'
        return render(request, template_name, {'payment_type_form': payment_type_form})

    elif request.method == 'POST':
        try:
            form_data = request.POST
            pmt = PaymentType(
                customer = request.user,
                payment_type_name = form_data['payment_type_name'],
                account_number = form_data['account_number'],
            )
            pmt.save()
            template_name = 'payment_type_success.html'
            return render(request, template_name, {})
        except OverflowError:
             return HttpResponse('Credit Card Number too Large')


@login_required(login_url='/login')
def user_payment_types(request):
    """
    Purpose: To retrieve a list of all payment types associated with user
    Args: request -- the full HTTP request object
    Returns: list of payment types associated with current user.
    """
    user_payment_types = PaymentType.objects.filter(customer = request.user)
    template_name = 'user_payment_types.html'
    return render(request, 'user_payment_types.html', {'user_payment_types': user_payment_types})


@login_required(login_url='/login')
def delete_payment_type(request):
    """
    Purpose: Delete a payment type from a customer's account
    Args: request --the full HTTP request object
    Returns: n/a
    """
    if request.method == 'POST':
        try:
            pmt_type_to_delete = request.POST['payment_type_id']
            pmt_type = PaymentType.objects.get(pk=pmt_type_to_delete).delete()
        except:
            user_payment_types = PaymentType.objects.filter(customer = request.user)
            return render(request, 'user_payment_types.html', {'user_payment_types': user_payment_types})

        return render(request, 'delete_payment_type.html', {'delete_payment_type': delete_payment_type})


@login_required(login_url='/login')
def user_trips(request):
    """
    Purpose: To retrieve a list of all trips for sale by a user
    Args: request -- the full HTTP request object
    Returns: list of trips sold by the current user
    """

    user_trips = Trip.objects.all().filter(seller = request.user)
    template_name = 'user_trips.html'
    return render(request, template_name, {'user_trips': user_trips})


@login_required(login_url='/login')
def delete_user_trip(request):
    """
    Purpose: Displays all of the authenticated user's trips and allows the user to delete them
    Args: request -- the full HTTP request object
    Returns: n/a 
    """

    user_trip_to_delete = request.POST['trip_id']
    sold_user_trip = TripOrder.objects.all().filter(trip=user_trip_to_delete)

    if sold_user_trip:
        return HttpResponse("You Didn't Say The Magic Word!")

    elif not sold_user_trip:
        user_trip = Trip.objects.get(pk=user_trip_to_delete).delete()
        return render(request, 'delete_user_trip.html', {'delete_user_trip': delete_user_trip})


@login_required(login_url='/login')
def add_trip_to_order(request, trip_id):
    """
    Purpose: To add a trip (by the trip id) to the TripOrder table.
    Args: trip_id - the id of the trip to be added to the cart, request --the full HTTP request object 
    Returns: Redirects user to their shopping cart after a successful add
    """
    trip_to_add = Trip.objects.get(pk=trip_id)

    try:
        customer = request.user
        new_order = Order.objects.get(customer=customer, active=1)
    except ObjectDoesNotExist:
        customer = request.user
        new_order = Order.objects.create(customer=customer, order_date=None, payment_type=None, active=1)

    if trip_to_add.quantity <= 0:
        pass
    elif trip_to_add.quantity > 0:
        add_to_TripOrder = TripOrder.objects.create(trip=trip_to_add, order=new_order)

    return HttpResponseRedirect('/cart')


@login_required(login_url='/login')
def view_cart(request):
    """
    Purpose: To view the cart of a customer's trips
    Args: request --the full HTTP request object
    Returns: A list of the trips added to a shopping cart and their total
    """
    total = 0

    try:
        customer = request.user
        order_id = Order.objects.get(customer=customer, active=1).id
    except ObjectDoesNotExist:
        customer = request.user
        order_id = Order.objects.create(customer=customer, order_date=None, payment_type=None, active=1)

    try:
        trips_in_cart = TripOrder.objects.all().filter(order=order_id)
    except:
        return render(request, 'cart.html', { 'total' : total, 'orderid' : order_id } )

    for trip in trips_in_cart:
        total += trip.trip.price

    return render(request, 'cart.html', { 'trips_in_cart' : trips_in_cart, 'total' : total, 'orderid' : order_id } )

@login_required(login_url='/login')
def complete_order_add_payment(request, order_id):
    """
    purpose: Allows user to add a payment type to their order and therefore complete and place the order
    args: request --the full HTTP request object, order_id - passed to this method from the view_cart method 
    returns: a checkout page where the user sees their order total and can select a payment type for their order
    """
    if request.method == 'POST':
        total = request.POST['total']
        adding_payment_types = PaymentType.objects.filter(customer = request.user)

        template_name = 'checkout.html'
        return render(request, template_name, { 'adding_payment_types': adding_payment_types, 'order_id' : order_id, 'total': total })

@login_required(login_url='/login')
def order_confirmation(request):
    """
    purpose: To mark an order as finished by setting the active field as 0 and writing the 
    payment type used for the order to the database.
    args: request --the full HTTP request object
    returns: renders the order confirmation table after a successful order completion
    """
    if request.method == 'POST':

        current_customer = request.user.id
        current_user = User.objects.get(pk=current_customer)

        payment_type_id = request.POST['payment_type_id']
        order_id = request.POST['order_id']

        trips_on_order = TripOrder.objects.values_list('trip', flat=True).filter(order=order_id)
        for each_trip in trips_on_order:
            tripid = Trip.objects.get(pk=each_trip)
            tripid.quantity = tripid.quantity - 1
            tripid.quantity_sold = tripid.quantity_sold + 1
            tripid.save()


        completed_order = Order.objects.get(pk=order_id)
        completed_order.payment_type = PaymentType.objects.get(pk=payment_type_id)
        completed_order.active = False
        completed_order.order_date = datetime.now()
        completed_order.save()        

        return render(request, 'order_confirmation.html' , {'trips_on_order' : trips_on_order})
        
@login_required(login_url='/login')
def delete_trip_from_cart(request):
    """
    Purpose: to remove a specific trip from the shopping cart on the browser, as well as in the Order table
    Args: request -- the full HTTP request object, trip_id - the id of the selected trip thats going to be deleted
    Returns: an updated shopping cart without the selected trip
    """

    if request.method == 'POST':
        deleted_trip = request.POST['trip_id']
        order_for_deletion = request.POST['order_id']
        the_id = request.POST['the_id']

        try:
            TripOrder.objects.get(trip=deleted_trip, order=order_for_deletion, pk=the_id).delete()
        except MultipleObjectsReturned:
            multiple_trips = TripOrder.objects.all().filter(trip=deleted_trip, order=order_for_deletion).delete()

        return HttpResponseRedirect('/cart')

@login_required(login_url='/login')
def view_cancel_order(request):
    """
    Purpose: to cancel an order and remove it from the database
    Args: request -- the full HTTP request object
    Returns: an updated Order table, without the specific order that has been cancelled
    """
    deleted_order = request.POST.get('order_id')
    Order.objects.get(id=deleted_order).delete()

    return render(request, 'final_order_view.html' , {})


def search(request):
    """
    Purpose: Search for a trip by title or location using search bar in nav.
    Args: request -- the full HTTP request object
    Returns: List of trips matching search parameters entered by user.
    """
    all_trips = Trip.objects.all().order_by("title")
    query = request.GET.get("q")
    if query:
        trips = all_trips.filter(
            Q(title__contains=query) | Q(location__contains=query)).distinct() 
        return render(request, 'query_results.html', {'search': trips})
    
    return render(request, 'query_results.html', {})



@login_required(login_url='/login')
def view_order_detail(request, order_id):
    """
    Purpose: to show the user's past orders
    Args: request -- the full HTTP request object, order_id - the id of the order 
    Returns: a view of order's details (trips on the order and total cost)
    """

    total = 0

    trips_in_cart = TripOrder.objects.all().filter(order=order_id)

    for each_item in trips_in_cart:
        total += each_item.trip.price

    template_name = 'order_detail.html'
    order = get_object_or_404(Order, pk=order_id)            
    return render(request, template_name, {"order": order, "total": total, "trips_in_cart": trips_in_cart})


@login_required(login_url='/login')
def update_profile(request):
    """
    Purpose: to update customer's profile settings
    Args: request -- the full HTTP request object, order_id - the id of the order 
    Returns: a view of customer's current profile details with option to edit and save them
    """
    if request.method == 'POST':
        customer_data = request.POST
        current_user = request.user
        current_user.first_name = customer_data['first_name']
        current_user.last_name = customer_data['last_name']
        current_user.save()
        customer = Customer.objects.get(user_id=current_user.id)
        customer.phone = customer_data['phone']
        customer.street_address = customer_data['street_address']
        customer.save()
        return HttpResponseRedirect('/profile')

    else:
        current_user = request.user
        customer = Customer.objects.get(user_id=current_user.id)
        context = {'customer': customer}
        template_name = 'edit_settings.html'
        return render(request, template_name, context)


