from django.test import client, TestCase
from website.models import *
from website.views import *
from django.urls import reverse

class ProductDetailViewTest(TestCase):
    """
    Purpose: Verify that when a trip is created that the Product Detail view has the correct trip with the trip's title, description, price and quantity in the response context 
    Args: (integer) trip pk
    Returns: Pass/Fail based on successful/unsuccessful assertion
    """

    def setUp(self):

        self.user = User.objects.create_user(
            username = "mducharme",
            email = "meg@meg.com",
            password = "abcd1234",
            first_name = "Meg",
            last_name = "Ducharme"
        )

        self.trip_type = ProductType.objects.create(trip_type_name="Test")

        self.trip = Trip.objects.create(
            seller = self.user,
            trip_type = self.trip_type,
            title = "emoji stickers",
            description = "yay!",
            price = 1.99,
            quantity = 500
        )

        self.client.login(
            username = "mducharme",
            password = "abcd1234"
        )


    def test_trip_detail_view_shows_correct_trip(self):
        response = self.client.get(reverse('website:single_trip', args=([self.trip.pk])))
        self.assertEqual(response.context['trip'].title, 'emoji stickers')


    def test_product_detail_view_shows_trip_details(self):
        response = self.client.get(reverse('website:single_trip', args=([self.trip.pk])))
        self.assertContains(response, "emoji stickers")
        self.assertContains(response, "yay!")
        self.assertContains(response, "1.99")
        self.assertContains(response, "500")


class TripTypeViewTest(TestCase):
    """
    Purpose: Verify that when a specific trip type is chosen, only trips in that type are displayed.
    Args: (integer) product_type pk
    Returns: Pass/Fail based on successful/unsuccessful assertion
    """

    def setUp(self):

        self.user = User.objects.create_user(
            username = "mscott",
            email = "mike@dm.com",
            password = "1111",
            first_name = "Michael",
            last_name = "Scott"
        )

        self.trip_type1 = TripType.objects.create(trip_type_name="TestType1")
        self.trip_type2 = TripType.objects.create(trip_type_name="TestType2")

        self.product = Trip.objects.create(
            seller = self.user,
            trip_type = self.trip_type1,
            title = "Hot Air Balloon Trip Around the World",
            description = "See the world from a hot air balloon.",
            price = 1115.99,
            quantity = 12
        )

        self.trip = Trip.objects.create(
            seller = self.user,
            trip_type = self.trip_type1,
            title = "Journey To The Center Of The Earth",
            description = "It's gonna get really hot down there.",
            price = 10.99,
            quantity = 3
        )

        self.trip = Trip.objects.create(
            seller = self.user,
            trip_type = self.trip_type2,
            title = "Journey To the Fridge",
            description = "Shouldn't show",
            price = 1.99,
            quantity = 1
        )


        self.client.login(
            username = "mscott",
            password = "1111"
        )

    def test_trip_type_trips_view(self):
        response = self.client.get(reverse('website:get_trip_types', args=([self.trip_type1.pk])))  
        self.assertQuerysetEqual(response.context['trips_of_type'], ["<Trip: Hot Air Balloon Trip Around the World>", "<Trip: Journey To The Center Of The Earthd>"],ordered=False)

class PaymentTypesViewTest(TestCase):
    """
    Purpose: Verifies that the Payment Types view for a customer has all of the payment types in the request context
    Args: HTTP request
    Returns: Pass/Fail based on successful/unsuccessful assertion
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username = "mducharme",
            email = "meg@meg.com",
            password = "abcd1234",
            first_name = "Meg",
            last_name = "Ducharme"
        )

        self.payment_type = PaymentType.objects.create(
            payment_type_name = "Visa",
            account_number = 1234123412341234,
            customer = self.user
        )

        self.payment_type = PaymentType.objects.create(
            payment_type_name = "MasterCard",
            account_number = 5678567856785678,
            customer = self.user
        )

        self.payment_type = PaymentType.objects.create(
            payment_type_name = "AMEX",
            account_number = 1010101010101010,
            customer = self.user
        )

        self.client.login(
            username = "mducharme",
            password = "abcd1234"
        )


    def test_payment_type_view_shows_payment_types(self):
        response = self.client.get(reverse('website:user_payment_types'))
        self.assertQuerysetEqual   (response.context["user_payment_types"], ["<PaymentType: AMEX>", "<PaymentType: MasterCard>", "<PaymentType: Visa>"])



class TripsInCartViewTest(TestCase):
    """
    Purpose: Verify that when trips are added to an order that the Order Summary view has those trips in the response context
    Args: (integer) trip pk
    Returns: Pass/Fail based on successful/unsuccessful assertion
    """
        
    def test_trips_show_in_cart(self):
        
        self.user = User.objects.create_user(
            username = "mducharme",
            email = "meg@meg.com",
            password = "abcd1234",
            first_name = "Meg",
            last_name = "Ducharme"
        )

        self.customer = Customer.objects.create(
            phone = 1234567890,
            user = self.user
        )

        self.trip_type = TripType.objects.create(trip_type_name="TestProdType")

        
        self.trip_1 = Trip.objects.create(
            seller = self.user,
            trip_type = self.trip_type,
            title = "emoji stickers",
            description = "yay!",
            price = 1.99,
            quantity = 500
        )


        self.trip_2 = Trip.objects.create(
            seller = self.user,
            trip_type = self.trip_type,
            title = "Keys",
            description = "They're keys",
            price = 3.00,
            quantity = 100
        )


        self.trip_3 = Trip.objects.create(
            seller = self.user,
            trip_type = self.trip_type,
            title = "Magic Wand",
            description = "oh oh it's magic",
            price = 5.99,
            quantity = 12
        )

        self.payment_type = PaymentType.objects.create(
            payment_type_name = "MasterCard",
            account_number = 5678567856785678,
            customer = self.user
        )

        self.order = Order.objects.create(
            customer = self.user,
        )


        self.trip_order_1 = Triprder.objects.create(
            trip = self.trip_1,
            order = self.order
        )

        self.trip_order_2 = TripOrder.objects.create(
            trip = self.trip_2,
            order = self.order
        )


        self.trip_order_3 = TripOrder.objects.create(
            trip = self.trip_3,
            order = self.order
        )

        self.client.login(
            username = "mducharme",
            password = "abcd1234"
        )


        response = self.client.get(reverse('website:cart'))

        self.assertQuerysetEqual   (response.context["trips_in_cart"], ["<TripOrder: emoji stickers>", "<TripOrder: Keys>", "<TripOrder: Magic Wand>"])



class OrderHistoryViewTest(TestCase):
    """
    Purpose: to test that the order history is showing orders that correspond with the authenticated user  
    Args: extends the TestCase 
    Returns: Pass/Fail based on successful/unsuccessful assertion
    """

    def setUp(self):

        self.user = User.objects.create_user(
            username = "jnelson",
            email = "jordo@jordo.com",
            password = "abcd1234",
            first_name = "Jordan",
            last_name = "Nelson"
        )

        self.customer = Customer.objects.create(
            phone = 1234567890,
            user = self.user
        )

        self.trip_type = TripType.objects.create(trip_type_name="TestProdType")

        self.trip = Trip.objects.create(
            seller = self.user,
            trip_type = self.trip_type,
            title = "Beard Comb",
            description = "Finest Facial Comb in the Land",
            price = "5.25",
            quantity = "500"
        )

        self.order = Order.objects.create(
            customer = self.user,
        )

        self.trip_order_1 = TripOrder.objects.create(
            trip = self.trip,
            order = self.order
        )

    def test_order_history_view(self):
        response = self.client.get(reverse('website:order_detail', args=([self.trip.pk])))
        print('The response: ', response)
        self.assertContains(response, "Beard Comb")
        self.assertContains(response, "5.25")
