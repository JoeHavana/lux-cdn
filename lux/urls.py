from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth.decorators import login_required

from core.newsletter import views as newsletter_views
from core.contact import views as contact_views
from .views import *

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls
from .api import api_router # Cap-34

from search import views as search_views

urlpatterns = [
    #path('', HomeView.as_view(), name="home"),
    #path('ct/<theme>/', define_color_theme, name="color-theme-selected"),

    path('cpanel/', admin.site.urls),
    path('styleguide', styleguide, name="styleguide"),
    path('styleguide/icons', icons, name="icons"),

    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    path('search/', search_views.search, name='search'),
    path('comments/', include('django_comments_xtd.urls')),

    path('api/', api_router.urls),  # Cap-34
    path('sitemap.xml', sitemap),
    path('accounts/', include('allauth.urls')),  # Delete 'accounts/'
    path('qrcodes/', include('qrcoder.urls')),

# REST-Framework URLs Customized API
	#Routers:
        #path('apis/routers/', include('core.routers')),
	#MEDICIN:
        #path('apis/medical/', include('core.medicin.api.urls', 'medicin_api')),
	# USERS:
    path('apis/account/', include('core.users.api.urls', 'account_api')),
    path('apis/gettoken/', TokenObtainPairView.as_view(), name="gettoken"),
    path('apis/refresh_token/', TokenRefreshView.as_view(), name="refresh_token"),

# Vanilla Django
    path('product/<slug>/', ItemDetail, name="product-detail"),

    path('category/', AllCategories.as_view()), # Implemented
    path('categories/', AllCategories.as_view(), name="all-categories"), # Implemented
    path('categories/<slug>/', categoryDetail, name="category-detail"), # Implemented

    path('rate/<slug>/', login_required(rating_items), name="rating-items"), # Fix this

    path('add-to-cart/<slug>/', login_required(add_to_cart), name="add-to-cart"),
    path('add-single-item-to-cart/<slug>/', login_required(add_single_item_to_cart), name="add-single-item-to-cart"), # Implemented

    path('add-directly-to-cart/<slug>/', login_required(add_directly_to_cart), name="add-directly-to-cart"), # DELETE THIS
    path('add-directly-with-ajax/', login_required(add_directly_with_ajax), name="add-directly-with-ajax"),

    path('remove-from-cart/<slug>/', login_required(remove_from_cart), name="remove-from-cart"), # Implemented
    path('remove-item-from-cart/<slug>/', login_required(remove_single_item_from_cart), name="remove-single-item-from-cart"),
    path('clean-cart/', login_required(clean), name="clean-cart"), # Implemented

    path('order-summary/', login_required(OrderSummaryView.as_view()), name="order-summary"), # Implemented
    path('checkout/', login_required(CheckoutView.as_view()), name="checkout"), # Implemented
    path('add-coupon/', login_required(AddCouponView.as_view()), name="add-coupon"),	 # Implemented
    path('request-refund/', login_required(RequestRefundView.as_view()), name="request-refund"),    # TEST THIS

    path('payment/', login_required(SelectOnePaymentOption), name="payment"),	 # Implemented
    #path('payment/stripe/', login_required(StripePaymentView.as_view()), name="stripe-payment"), 
    path('payment/stripe/', login_required(PaymentView.as_view()), name="stripe-payment"),
    #path('payment/paypal/', login_required(PaymentView.as_view()), name="paypal-payment"),    # PaypalPaymentView

    path('user-messages/', login_required(contact_views.user_messages), name="user-messages"),
    path('contact/thanks/', login_required(contact_views.contact_thank), name="user-messages-thanks"),
    path('contact/failed/', login_required(contact_views.contact_failed), name="user-messages-failed"),
# Newsletter App 
    path('newsletter-subscribe/', newsletter_views.newsletter_signup, name="newsletter_signup"),
    path('newsletter-unsubscribe/', newsletter_views.newsletter_unsubscribe, name="newsletter_unsubscribe"),
    path('newsletter-control/', login_required(newsletter_views.control_newsletter), name="control_newsletter"),
    path('newsletter-list/', login_required(newsletter_views.newsletter_list), name="newsletter_list"),
    path('newsletter/<pk>/', login_required(newsletter_views.newsletter_detail), name="newsletter_detail"),
    path('newsletter/edit/<pk>/', login_required(newsletter_views.newsletter_edit), name="newsletter_edit"),
    path('newsletter/del/<pk>/', login_required(newsletter_views.newsletter_delete), name="newsletter_delete"),

    path('test-pay/', test_pay, name="test-after-payment"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
# Django_Debug_Toolbar:
    #import debug_toolbar
    #urlpatterns = [
    #    path('__debug__/', include(debug_toolbar.urls)),
    #] + urlpatterns

# + i18n_patterns (
urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]