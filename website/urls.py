from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "website"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login_user, name='login'),
    url(r'^logout$', views.user_logout, name='logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^sell$', views.sell_trip, name='sell'),
    url(r'^trips$', views.list_trips, name='list_trips'),
    url(r'^single_trip/(?P<trip_id>[0-9]+)/$', views.single_trip, name='single_trip'),
    url(r'^trip_types$', views.list_trip_types, name='trip_types'),
    url(r'^trip_type_trips/(?P<type_id>[0-9]+)/$', views.get_trip_types, name='get_trip_types'),
    url(r'^add_payment_type$', views.add_payment_type, name='add_payment_type'),
    url(r'^user_payment_types$', views.user_payment_types, name='user_payment_types'),
    url(r'^user_trips$', views.user_trips, name='user_trips'),
    url(r'^delete_user_trip$', views.delete_user_trip, name='delete_user_trip'),
    url(r'^delete_payment_type$', views.delete_payment_type, name='delete_payment_type'),
    url(r'^add_to_cart/(?P<trip_id>[0-9]+)/$', views.add_trip_to_order, name='add_trip_to_order'),
    url(r'^cart$', views.view_cart, name='cart'),
    url(r'^checkout/(?P<order_id>[0-9]+)/$', views.complete_order_add_payment, name='checkout'),
    url(r'^order_confirmation$', views.order_confirmation, name='order_confirmation'),
    url(r'^delete_trip_from_cart$', views.delete_trip_from_cart, name='delete_trip_from_cart'),
    url(r'^final_order_view$', views.view_cancel_order, name='final_order_view'),
    url(r'^search/$', views.search, name='search'),
    url(r'^order_detail(?P<order_id>[0-9]+)/$', views.view_order_detail, name='order_detail'),
    url(r'^edit_settings$', views.update_profile, name='edit_settings'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

