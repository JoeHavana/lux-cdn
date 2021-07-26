import random
import string
import stripe
import time
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.db.models import Q
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail, EmailMultiAlternatives
from datetime import date, datetime
from core.store.models import *
from core.store.forms import * 
from core.site_settings.models import Brand
from core.streams.choices import *
from home.models import *

stripe.api_key = settings.STRIPE_SECRET_KEY # STRIPE_TEST_KEY

year = date.today().year
today = date.today()
"""
 Next bunch of functions aren't in JustDjango
def file_not_found_404(request, exception):
	return render(request, "hendle404.html")

def define_color_theme(request, theme):
	request.session['color_theme'] = theme
	return redirect('home')
 Last bunch of functions aren't in JustDjango
"""

def test_pay(request):
	return render(request, 'pages/after_pay.html')

# In JustDjango
def create_ref_code():
	return ''.join(random.choices(string.ascii_lowercase + string.digits, k=30))

def create_affiliation_code():
	return ''.join(random.choices(string.ascii_lowercase + string.digits, k=40))

# In JustDjango
def is_valid_form(values):
	valid = True
	for field in values:
		if field == "":
			valid = False
	return valid

def styleguide(request):
	return render(request, 'styleguide/styleguide.html')

def icons(request):
	return render(request, 'styleguide/icons.html')


# Now ew user the 'get_context_data' in home/models.py 
class HomeView(View):


	def get(self, *args, **kwargs):

		#custom_home = CustomHomePage.objects.last()
		items = Item.objects.all()
		#carousels = Carousel.objects.all()
		navbarcategories = ItemCategory.objects.filter(will_be_recomended=True).order_by('priority').all()
		#faqs = FAQ.objects.all()
		#seo_text = TextRichContent.objects.all()
		if 'color_theme' in self.request.session:
			get_color_theme = self.request.session.get('color_theme')
			context = {
				'seo_text':seo_text,
				'faqs':faqs,
				'custom_home':custom_home,
				'carousels':carousels,
				'items':items,
				'year':year,
				'navbarcategories':navbarcategories,
				'countcatgnav':navbarcategories.count(),
				'favorit_color_theme':get_color_theme,
			}
			return render(self.request, 'home/home_page.html', context)
		else:
			context = {
				'items':items,
				'year':year,
				'navbarcategories':navbarcategories,
				'countcatgnav':navbarcategories.count()
			}
			return render(self.request, 'home/home_page.html', context)


	def post(self, *args, **kwargs):

		if self.request.method == 'POST':
			carousels = Carousel.objects.all()
			navbarcategories = Category.objects.filter(will_be_shown_as_recomendation=True).order_by('order_to_display').all()
			form = self.request.POST['navbar_filter']
			try:
				search_by = (
					Q(title__icontains=form)|
					Q(category__category_name__icontains=form)|
					Q(category__category_description__icontains=form)|
					Q(real_price__icontains=form)|
					Q(tag_relationship__tag_name__icontains=form)|
					Q(short_description__icontains=form)|
					Q(description__icontains=form)|
					Q(label__icontains=form)
				)
				returned_search_results = Item.objects.filter(search_by, is_available=True).distinct()
				if 'color_theme' in self.request.session:
					get_color_theme = self.request.session.get('color_theme')
					context = {
						'seo_text':seo_text,
						'faqs':faqs,
						'items': Item.objects.all(),
						'year':year,
						'favorit_color_theme':get_color_theme,
						'returned_search_results':returned_search_results,
						'navbarcategories':navbarcategories,
						'countcatgnav':navbarcategories.count(),
					}
					return render(self.request, 'home/home_page.html', context)
				elif 'color_theme' not in self.request.session:
					context = {
						'seo_text':seo_text,
						'faqs':faqs,
						'items': Item.objects.all(),
						'returned_search_results':returned_search_results,
						'year':year,
						'navbarcategories':navbarcategories,
						'countcatgnav':navbarcategories.count(),
					}
					return render(self.request, 'home/home_page.html', context)
				elif not returned_search_results:
					navbarcategories =  Category.objects.filter(will_be_shown_as_recomendation=True).order_by('order_to_display').all()
					countcatgnav = navbarcategories.count()
					context = {
						'seo_text':seo_text,
						'faqs':faqs,
						'items': Item.objects.all(),
						'carousels': Carousel.objects.all(),
						'navbarcategories':navbarcategories,
						'countcatgnav':countcatgnav,
						'favorit_color_theme':self.request.session.get('color_theme'),

						'timer': '',
						'message':"Sorry, it doesn't match with any of the categories.",
						'position': 'center',
						'icon': 'warning', #success, warning, info, question
						'confirmButtonText': 'OK',
					}
					return render(self.request, 'home/home_page.html', context)
			except:
				navbarcategories =  Category.objects.filter(will_be_shown_as_recomendation=True).order_by('order_to_display').all()
				countcatgnav = navbarcategories.count()
				context = {
					'seo_text':seo_text,
					'faqs':faqs,
					'items': Item.objects.all(),
					'carousels': Carousel.objects.all(),
					'navbarcategories':navbarcategories,
					'countcatgnav':countcatgnav,
					'favorit_color_theme':self.request.session.get('color_theme'),

					'timer': '',
					'message':"Sorry, we had some problems.",
					'position': 'center',
					'icon': 'warning', #success, warning, info, question
					'confirmButtonText': 'OK',
				}
				return render(self.request, 'home/home_page.html', context)
				#messages.info(self.request, f"Sorry, {form} doesn't match with any of the categories.")
				#return render(self.request, 'home/home_page.html')

######  Next code works with app store ####

# In JustDjango
def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)

# For ItemCategory List
class AllCategories(View):

	def get(self, *args, **kwargs):

		categories = ItemCategory.objects.filter(will_be_recomended=True).order_by('priority')
		context = {
			'categories':categories,
		}
		return render(self.request, 'store/item_categories/list_categories.html', context)

	def post(self, *args, **kwargs):

		if self.request.method == 'POST':
			form = self.request.POST['filter_by_categories']
			search_catg_by = (
				Q(category_name__icontains=form)|
				Q(category_description__icontains=form)|
				Q(tags_related__icontains=form)
			)
			categories = ItemCategory.objects.filter(search_catg_by).distinct()
			if categories.exists():
				context = {
					'categories':categories,
				}
				return render(self.request, 'store/item_categories/list_categories.html', context)
			else:
				messages.info(self.request, f"Sorry, '{form}' doesn't match with any of the categories.")
				return render(self.request, 'store/item_categories/list_categories.html')


def categoryDetail(request, slug):
	context = {
		"items_related":Item.objects.filter(Q(categories__slug=slug) & Q(is_available=True)).distinct(),
		"slug":f"{slug.replace('-',' ')}",
	}
	return render(request, 'store/item_categories/category_detail.html', context)

@login_required
def rating_items(request, slug):
	if request.method == 'POST':
		form = request.POST['rate_item']
		comment = request.POST['message']
		rate = float(form)
		item = get_object_or_404(Item, slug=slug)
		item_to_rate = Item.objects.filter(slug=slug)

		updadet_rating = float(item.real_rating_by_users) + float(rate)
		updadet_rated_by = float(item.rated_by) + 1
		if item.rated_by == 0:
			item_to_rate.update(real_rating_by_users=float(updadet_rating), rated_by=1, real_rate_average=float(updadet_rating))
			return redirect("product-detail", slug=slug)
		else:
			real_avg = float(item.real_rating_by_users) / float(item.rated_by)
			item_to_rate.update(real_rating_by_users=float(updadet_rating), rated_by=updadet_rated_by, real_rate_average=float(real_avg))
			return redirect("product-detail", slug=slug)

	else:
		return redirect("product-detail", slug=slug)
		

def ItemDetail(request, slug):
	if request.user.is_authenticated:
		item = Item.objects.get(slug=slug)
		try:
			order_in_cart = OrderItem.objects.get(user=request.user, item__slug=slug)
			if order_in_cart:
				messages.info(request, f'"{item.title}" is already in your cart.')
				return redirect('order-summary')

		except:
			if 'color_theme' in request.session:
				get_color_theme = request.session.get('color_theme')
				context = {
					'item':item,
					'favorit_color_theme':get_color_theme,
				}
				return render(request, 'pages/product-page.html', context)
			else:
				try:
					video = item.video_trailer.url
					context = {
						'item':item,
						'video': video
					}
					return render(request, 'pages/product-page.html', context)
					
				except Exception as e:
					context = {
						'item':item,
						'video': item.main_picture_of_presentation
					}
					return render(request, 'pages/product-page.html', context)
	else:
		item = Item.objects.get(slug=slug)
		context = {
			'item':item,
			'video':item.video_trailer.url,
		}
		return render(request, 'pages/product-page.html', context)


class OrderSummaryView(LoginRequiredMixin, View):

	def get(self, *args, **kwargs):

		try: # evalua si tienes un cart creado.
			order = Order.objects.get(user=self.request.user, ordered=False)
			order_item = OrderItem.objects.filter(user=self.request.user, ordered=False)

			if order and order_item:	# Buscas tus orders en tu cart
				# Dont use color theme
				if 'color_theme' in self.request.session:
					get_color_theme = self.request.session.get('color_theme')
					context = {
						'object':order,
						'favorit_color_theme':get_color_theme,
					}
					return render(self.request, 'pages/order_summary.html', context)	# store:order_summary
				else:
					context = {
						'object':order
					}
					return render(self.request, 'pages/order_summary.html', context)	# store:order_summary

			else:
				# Si tienes un cart creado, pero está vacio
				messages.info(self.request, "You don't have items in your cart")
				return render(self.request, 'pages/order_summary.html')


		except ObjectDoesNotExist: # Si aun no tienes un cart creado.
			if 'color_theme' in self.request.session:
				get_color_theme = self.request.session.get('color_theme')
				messages.info(self.request, "You do not have an active order.")
				return render(self.request, 'pages/order_summary.html')
			else:
				# 
				messages.info(self.request, "You do not have an active order.")
				return render(self.request, 'pages/order_summary.html')


class CheckoutView(View):

	def get(self, *args, **kwargs):
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			form = CheckoutForm()
			context = {
				'form':form,
				'couponForm':CouponForm(),
				'order':order,	
				'DISPLAY_COUPON_FORM':True,
				'discount_coupon':True
			}

			shipping_address_qs = Address.objects.filter(user=self.request.user, address_type='S', default=True)
			if shipping_address_qs.exists():
				context.update({
					'default_shipping_address':shipping_address_qs[0]
				})

			billing_address_qs = Address.objects.filter(user=self.request.user, address_type='B', default=True)
			if billing_address_qs.exists():
				context.update({
					'default_billing_address':billing_address_qs[0]
				})

			return render(self.request, 'pages/checkout-page.html', context)

		except ObjectDoesNotExist:
			messages.info(self.request, "You do not have an active order.")
			return redirect('/')


	def post(self, *args, **kwargs):
		form = CheckoutForm(self.request.POST or None)
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			if form.is_valid():

				use_default_shipping = form.cleaned_data.get('use_default_shipping')
				if use_default_shipping:
					address_qs = Address.objects.filter(user=self.request.user, address_type='S', default=True)
					if address_qs.exists():
						shipping_address = address_qs[0]
						order.shipping_address = shipping_address
						order.save()
					else:
						messages.info(self.request, "No default shipping address available")
						return redirect("checkout")
				else:
					street_shipping_address = form.cleaned_data.get('shipping_address')
					shipping_city_address = form.cleaned_data.get('shipping_city_address')
					shipping_country = form.cleaned_data.get('shipping_country')
					shipping_zipfield = form.cleaned_data.get('shipping_zipfield')

					if is_valid_form([ street_shipping_address, shipping_city_address, shipping_country, shipping_zipfield ]):
						shipping_address = Address(
							user = self.request.user,
							street_address = street_shipping_address,
							city_address = shipping_city_address,
							country = shipping_country,
							zipfield = shipping_zipfield,
							address_type = 'S'
						)
						shipping_address.save()

						order.shipping_address = shipping_address
						order.save()

						set_default_shipping = form.cleaned_data.get('set_default_shipping')
						if set_default_shipping:
							shipping_address.default = True
							shipping_address.save()

					else:
						messages.info(self.request, "You have to fill all the required fields.")
						return redirect('checkout')


				use_default_billing = form.cleaned_data.get('use_default_billing')
				same_billing_address = form.cleaned_data.get('same_billing_address')

				if same_billing_address:
					billing_address = shipping_address
					billing_address.pk = None
					billing_address.save()
					billing_address.address_type = 'B'
					billing_address.save()
					order.billing_address = billing_address
					order.save()

				elif use_default_billing:
					address_qs = Address.objects.filter(user=self.request.user, address_type='B', default=True)
					if address_qs.exists():
						billing_address = address_qs[0]
						order.billing_address = billing_address
						order.save()
					else:
						messages.info(self.request, "No default billing address available")
						redirect("checkout")
				else:
					street_billing_address = form.cleaned_data.get('billing_address')
					billing_city_address = form.cleaned_data.get('billing_city_address')
					billing_country = form.cleaned_data.get('billing_country')
					billing_zipfield = form.cleaned_data.get('billing_zipfield')

					if is_valid_form([ street_billing_address, billing_city_address, billing_country, billing_zipfield ]):
						billing_address = Address(
							user = self.request.user,
							street_address = street_billing_address,
							city_address = billing_city_address,
							country = billing_country,
							zipfield = billing_zipfield,
							address_type = 'B'
						)
						billing_address.save()

						order.billing_address = billing_address
						order.save()

						set_default_billing = form.cleaned_data.get('set_default_billing')
						if set_default_billing:
							billing_address.default = True
							billing_address.save()
							
					else:
						messages.info(self.request, "You have to fill all the required fields.")
						#return redirect('checkout')


				payment_options = form.cleaned_data.get('payment_options')

				if payment_options == 'S':
					return redirect('stripe-payment')
					#return render(self.request, 'stripe-payment.html', {'was_legal':True})
				elif payment_options == 'P':
					return redirect('paypal-payment')
					#return render(self.request, 'paypal-payment.html', {'was_legal':True})
				else:
					messages.info(self.request, f"Invalid payment option selected.")
					return redirect('checkout')

			else:
				messages.warning(self.request, "Failed checkout. Invalid Form. Please, Fill all fields out.")
				return redirect("checkout")

		except ObjectDoesNotExist:
			messages.info(self.request, "You do not have an active order.")
			return redirect('order-summary')


@login_required
def SelectOnePaymentOption(request):
		return render(request, "pages/payment.html")

@login_required
def get_coupon(request, code):
	try:
		coupon = Coupon.objects.get(code=code, disable=False)
		return coupon

	except ObjectDoesNotExist:
		messages.info(request, "This coupon does not exist.")
		return redirect('checkout')
	

class AddCouponView(View):
	def post(self, *args, **kwargs):
		try:
			if self.request.method == 'POST':
				form = CouponForm(self.request.POST or None)
				if form.is_valid():
					try:
						code = form.cleaned_data.get('code')
						order = Order.objects.get(user=self.request.user, ordered=False)
						order.coupon = get_coupon(self.request, code)
						if order.coupon.last_date_of_the_coupon_live == today:
							# TODO: with timedelta() check the coupon timelife
							order.coupon.disable=True
							order.coupon.save()
							messages.warning(self.request, "Sorry, this coupon is out of date.")
							return redirect('checkout')
						else:
							order.save()
							messages.info(self.request, "Coupon added successfully.")
							return redirect('checkout') #funnel:thanks

					except ObjectDoesNotExist:
						messages.info(self.request, "You have not an active order.")
						return redirect('checkout')
			else:
				messages.info(self.request, "Method not allowed.")
				return redirect('checkout')

		except ObjectDoesNotExist:
			messages.info(request, "This coupon does not exist.")
			return redirect('checkout')


class RequestRefundView(View):
	def get(self, *args, **kwargs):
		context = {
			'form':RefundForm()
		}
		return render(self.request, 'pages/request-refund.html', context)

	@method_decorator(login_required)
	def post(self, *args, **kwargs):
		form = RefundForm(self.request.POST)
		if form.is_valid():
			ref_code = form.cleaned_data.get('ref_code')
			message = form.cleaned_data.get('message')
			email = form.cleaned_data.get('email')

			try:
				order = Order.objects,get(ref_code=ref_code)
				order.refund_requested = True
				order.save()

				refund = Refund()
				refund.order = order
				refund.reason = message
				refund.email = email
				refund.save()

				messages.info(self.request, f'Your request have been received.')
				return redirect('request-refund')

			except Exception as e:
				messages.info(self.request, f'Order "{ref_code}" does not exists.')
				return redirect('request-refund')
		else:
			messages.info(self.request, f'Invalid. Please, try again.')
			return redirect('request-refund')

# DELETE
class StripeView(View): #DELETE
	def get(self, *args, **kwargs):
		try:
			order = Order.objects.filter(user=self.request.user, ordered=False)
			try:
				if order.exists(): # and order.billing_address:	# For digital products, remove billing address
					context = { 
						'order':order,
						'DISPLAY_COUPON_FORM':False,
						'STRIPE_PUBLIC_KEY' : settings.STRIPE_PUBLIC_KEY
					}
					return render(self.request, 'pages/stripe-payment.html', context)
				else:
					messages.warning(self.request, "You have not added a billing address.")
					return redirect('checkout')
			except Exception as e:
				messages.warning(self.request, f"Sorry, something have been wrong. \n Error: {e}")
				return redirect('checkout')
		except:
			messages.warning(self.request, "You do not have an active order.")
			return redirect('checkout')

	def post(self, *args, **kwargs):
		order = Order.objects.get(user=self.request.user, ordered=False)
		token = self.request.POST.get('stripeToken')
		amount = order.get_total() * 100 # This value is in cents
		# save = form.cleaned_data.get('save')
		# if save:  (WATCH THE JUSTDJANGO VIDEO 10 min: 4:44)
		# allows to fetch cards
		if not userprofile.stripe_customer_id:
			customer = stripe.Customer.create(
				email = self.request.user.email,
				source = token,
			)

		# Stripe Handling Errors
		try:
			charge = stripe.Charge.create(
				amount=amount,
				currency='usd',
				source=token, # obtained with Stripe.js
				description=self.request.user.email,
			)
		
			# Create the Payment
			payment = Payment()
			payment.stripe_chrage_id = charge['id']
			payment.user = self.request.user
			payment.amount = order.get_total()
			payment.save()

			# Assign the payment to the order
			order_items = order.items.all()
			order_items.update(ordered=True)
			for item in order_items:
				item.save()

			ref_code_from_function = create_ref_code()
			orderID = order.pk
			order.ordered = True
			order.payment = payment
			order.ref_code = f'{orderID}{ref_code_from_function}'
			order.save()

			return redirect('download_page.html') #funnel:thanks-page

		except stripe.error.CardError as e:
			# Since it's a decline, stripe.error.CardError will be caught
			body = e.json_body
			err = body.get('error', {})
			messages.info(self.request, f'{err.get(message)}')
			return redirect('/')

			print('Status is: %s' % e.http_status)
			print('Type is: %s' % e.error.type)
			print('Code is: %s' % e.error.code)
			# param is '' in this case
			print('Param is: %s' % e.error.param)
			print('Message is: %s' % e.error.message)
		except stripe.error.RateLimitError as e:
			# Too many requests made to the API too quickly
			messages.info(self.request, f'Stripe is procesing too many requests to quickly. Please, wate some minutes and try again.')
			return redirect('/')
		except stripe.error.InvalidRequestError as e:
			# Invalid parameters were supplied to Stripe's API
			messages.info(self.request, f'Invalid parameters were supplied.')
			return redirect('/')
		except stripe.error.AuthenticationError as e:
			# Authentication with Stripe's API failed
			# (maybe you changed API keys recently)
			messages.info(self.request, f'Authentication with Stripe failed.')
			return redirect('/')
		except stripe.error.APIConnectionError as e:
			# Network communication with Stripe failed
			messages.info(self.request, f'Stripe is having some problems to connect with the Network in this moment.')
			return redirect('/')
		except stripe.error.StripeError as e:
			# Display a very generic error to the user, and maybe send
			# yourself an email
			messages.info(self.request, f'Sorry, something went wrong. You were not cherged. Contact us to help you.')
			return redirect('/')
		except Exception as e:
			# Send an email to ourselves
			messages.info(self.request, f'A serious error occuurred. We have been notified.')
			return redirect('/')


class PaymentView(View):

	def get(self, *args, **kwargs):
		order = Order.objects.get(user=self.request.user, ordered=False)
		if order.billing_address:
			context = {
				'order': order,
				'DISPLAY_COUPON_FORM': False,
				'STRIPE_PUBLIC_KEY' : settings.STRIPE_PUBLIC_KEY
			}
			userprofile = self.request.user.userprofile
			if userprofile.one_click_purchasing:
				# fetch the users card list
				cards = stripe.Customer.list_sources(
					userprofile.stripe_customer_id,
					limit=3,
					object='card'
				)
				card_list = cards['data']
				if len(card_list) > 0:
					# update the context with the default card
					context.update({
						'card': card_list[0]
					})
			return render(self.request, "pages/stripe-payment.html", context)
		else:
			messages.warning(
				self.request, "You have not added a billing address")
			return redirect("checkout")
	
	def post(self, *args, **kwargs):
		order = Order.objects.get(user=self.request.user, ordered=False)
		form = PaymentForm(self.request.POST)
		userprofile = UserProfile.objects.get(user=self.request.user)
		if form.is_valid():
			token = form.cleaned_data.get('stripeToken')
			save = form.cleaned_data.get('save')
			use_default = form.cleaned_data.get('use_default')

			if save:
				if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
					customer = stripe.Customer.retrieve(
						userprofile.stripe_customer_id)
					customer.sources.create(source=token)

				else:
					customer = stripe.Customer.create(
						email=self.request.user.email,
					)
					customer.sources.create(source=token)
					userprofile.stripe_customer_id = customer['id']
					userprofile.one_click_purchasing = True
					userprofile.save()

			amount = int(order.get_total() * 100)

			try:
				if use_default or save:
					# charge the customer because we cannot charge the token more than once
					charge = stripe.Charge.create(
						amount=amount,  # cents
						currency="usd",
						customer=userprofile.stripe_customer_id
					)
				else:
					# charge once off on the token
					charge = stripe.Charge.create(
						amount=amount,  # cents
						currency="usd",
						source=token
					)

				# create the payment
				payment = Payment()
				payment.stripe_charge_id = charge['id']
				payment.user = self.request.user
				payment.amount = order.get_total()
				payment.save()

				# assign the payment to the order
				order_items = order.items.all()
				order_items.update(ordered=True)
				for item in order_items:
					item.save()

				order.ordered = True
				order.payment = payment
				order.ref_code = create_ref_code()
				order.save()

				messages.success(self.request, "Your order was successful!")
				return redirect("/")

			except stripe.error.CardError as e:
				body = e.json_body
				err = body.get('error', {})
				messages.warning(self.request, f"{err.get('message')}")
				return redirect("/")

			except stripe.error.RateLimitError as e:
				# Too many requests made to the API too quickly
				messages.warning(self.request, "Rate limit error")
				return redirect("/")

			except stripe.error.InvalidRequestError as e:
				# Invalid parameters were supplied to Stripe's API
				print(e)
				messages.warning(self.request, "Invalid parameters")
				return redirect("/")

			except stripe.error.AuthenticationError as e:
				# Authentication with Stripe's API failed
				# (maybe you changed API keys recently)
				messages.warning(self.request, "Authentication with Stripe failed")
				return redirect("/")

			except stripe.error.APIConnectionError as e:
				# Network communication with Stripe failed
				messages.warning(self.request, "Network error")
				return redirect("/")

			except stripe.error.StripeError as e:
				# Display a very generic error to the user, and maybe send
				# yourself an email
				messages.warning(
					self.request, "Something went wrong. You were not charged. Please try again.")
				return redirect("/")

			except Exception as e:
				# send an email to ourselves
				messages.warning(
					self.request, "A serious error occurred. We have been notifed.")
				return redirect("/")

		messages.warning(self.request, "Invalid data received")
		return redirect("/payment/stripe/")


#  ADD & REMOVE from cart 
@login_required
def add_to_cart(request, slug): # I added slug argument
	item = get_object_or_404(Item, slug=slug) # Change pk to slug in JustDjango
	quantity = request.POST['quantity']
	item_discount_stock = Item.objects.filter(slug=slug)

	# Send an email to the owner of the websit adverting that there are less than 10 items in the stock for this particular Item
	if item.quantity_in_stock <= 9:
		pass


	if item.quantity_in_stock >= int(quantity):
		new_quantity = int(item.quantity_in_stock) - int(quantity)
		new_smart_quantity = int(item.smart_quantity_stock_to_display) - int(quantity)
		item_discount_stock.update(quantity_in_stock=new_quantity, smart_quantity_stock_to_display=new_smart_quantity)
		if item.smart_quantity_stock_to_display <=5:
			increment_smart_quantity = 150
			item_discount_stock.update(smart_quantity_stock_to_display=increment_smart_quantity)

		order_item, created = OrderItem.objects.get_or_create(
			item = item,
			user = request.user,
			quantity = quantity,
			ordered = False
		)
		item_discount_stock = Item.objects.filter(slug=slug)
		if item.quantity_in_stock >= int(quantity):
			new_quantity = int(item.quantity_in_stock) - int(quantity)
			item_discount_stock.update(quantity_in_stock=new_quantity)

		order_qs = Order.objects.filter(user=request.user, ordered=False)

		if order_qs.exists():
			order = order_qs[0]
			# Ceck if the Order Item is in the order
			if order.items.filter(item__slug=item.slug).exists():
				order_item.quantity = quantity # +=1
				order_item.ordered = True
				messages.info(request, f'Added {quantity} new items of "{order_item.item.title}" to your cart.')
				return redirect("product-detail", slug=slug)

			else:
				order.items.add(order_item)
				navbarcategories =  Category.objects.filter(will_be_shown_as_recomendation=True).order_by('order_to_display').all()
				countcatgnav = navbarcategories.count()
				context = {
					'items': Item.objects.all(),
					'carousels': Carousel.objects.all(),
					'navbarcategories':navbarcategories,
					'countcatgnav':countcatgnav,
					'favorit_color_theme': request.session.get('color_theme'),

					'timer': '2500',
					'message':f'{quantity} item added to your cart.',
					'position': 'center',
					'icon': 'success', #success, warning, info, question
					'confirmButtonText': 'OK',
				}
				return render(request, 'home/home_page.html', context)
				#messages.info(request, f'{quantity} item added to your cart.')
				#return redirect("/", slug=slug)

		else:
			ordered_date = timezone.now()
			order = Order.objects.create( user=request.user, ordered_date=ordered_date )
			order.items.add(order_item)
			messages.info(request, f'{quantity} item added to your cart.')
			return redirect("/", slug=slug)

	# If quantity to discount to Item > quantity_in_stock
	else:
		messages.info(request, f'The quantity {quantity} you are trying to buy is higher that ower stock. We only have {item.quantity_in_stock}')
		return redirect("product-detail", slug=slug)

@login_required
def add_directly_with_ajax(request):

	if request.POST.get('action') == 'post':

		product_id = int(request.POST.get('productid'))

		item = get_object_or_404(Item, id=product_id) # Change pk to slug in JustDjango

		order_item, created = OrderItem.objects.get_or_create(item = item, user = request.user, ordered = False)
		order_qs = Order.objects.filter(user=request.user, ordered=False)

		if order_qs.exists():
			order = order_qs[0]
			# Check if the OrderItem is in the order
			if order.items.filter(item__slug=item.slug).exists():

				# Reduces 1 item from Stock if the user add a new item in 'order-summary'
				if item.quantity_in_stock >= 1:
					new_quantity = int(item.quantity_in_stock) - 1
					item_to_update = Item.objects.filter(id=product_id)
					item_to_update.update(quantity_in_stock=new_quantity)

					# Al tocar el boton, si la cantidad en stock es <= que la seleccionada para ser alertados
					if new_quantity <= item.alert_minimal_stock:
						subject = f'ALERT: Minimal Quantity in the Stock for "{item}"'
						body = f'There are "{new_quantity}" items in stock, for the item "{item}", in the "APP STORE".'
						from_email = 'may@mail.com' #settings.EMAIL_HOST_USER
						for email in EmailsToAlertMinimalStock.objects.all():
							send_mail(subject=subject, from_email=from_email, recipient_list=[email.email], message=body, fail_silently=False)
						
					
				else:
					# Al tocar el boton, si ya no queda en stock
					# TODO: send a message to the owner alerting that exists 0 products is Stock
					subject = f'ALERT: 0 items in the Stock for "{item}"'
					body = f'0 items in stock, for the item "{item}", in the "APP STORE".'
					from_email = 'may@mail.com' #settings.EMAIL_HOST_USER
					for email in EmailsToAlertMinimalStock.objects.all():
						send_mail(subject=subject, from_email=from_email, recipient_list=[email.email], message=body, fail_silently=False)
					
					data = {}
					try:
						qs = Order.objects.filter(user=request.user, ordered=False)
						if qs.exists():
							qty = qs[0].items.count()
							data['qty'] = qty
							data['title'] = f'We are so sorry. But we do not have more of this item in stock.'
							data['confirmButtonText'] = 'OK'
							return JsonResponse(data)
						else:
							pass
					except:
						data['title'] = f'We are so sorry. But we do not have more of this item in stock.'
						data['confirmButtonText'] = 'OK'
						return JsonResponse(data)

				# Cada vez que tocas el boton mientras haya en stock
				# Add 1 more of this specific item in my Ordered Items. (If you already have this Item in your cart)
				order_item.quantity += 1
				order_item.save()
				data = {}
				try:
					qs = Order.objects.filter(user=request.user, ordered=False)
					if qs.exists():
						qty = qs[0].items.count()
						data['qty'] = qty
						data['title'] = f'Added a new item to your cart.'
						data['timer'] = '2500'
						data['confirmButtonText'] = '<i class="fas fa-thumbs-up"></i>'
						return JsonResponse(data)
					else:
						pass
				except:
					data['title'] = f'Added a new item to your cart.'
					data['timer'] = '2500'
					data['confirmButtonText'] = '<i class="fas fa-thumbs-up"></i>'
					return JsonResponse(data)

			else:
				# Te añade items a tu carrito si sa existe.
				# If you don't have this Item in your Cart, (and will be added for the first time)
				if item.quantity_in_stock >= 1:
					# Reduces 1 item from Stock if the user add a new item in 'order-summary'
					new_quantity = int(item.quantity_in_stock) - 1
					item_to_update = Item.objects.filter(id=product_id)
					item_to_update.update(quantity_in_stock=new_quantity)

					order.items.add(order_item)
					data = {}
					try:
						qs = Order.objects.filter(user=request.user, ordered=False)
						if qs.exists():
							qty = qs[0].items.count()
							data['qty'] = qty
							data['title'] = f'"{order_item.item.title}" added to your cart.'
							data['timer'] = '2500'
							data['confirmButtonText'] = '<i class="fas fa-thumbs-up"></i>'
							return JsonResponse(data)
						else:
							pass
					except:
						data['title'] = f'"{order_item.item.title}" added to your cart.'
						data['timer'] = '2500'
						data['confirmButtonText'] = '<i class="fas fa-thumbs-up"></i>'
						return JsonResponse(data)

				else:
					data = {}
					try:
						qs = Order.objects.filter(user=request.user, ordered=False)
						if qs.exists():
							qty = qs[0].items.count()
							data['qty'] = qty
							data['title'] = f'"{order_item.item.title}" added to your cart.'
							data['confirmButtonText'] = '<i class="fas fa-thumbs-up"></i>'
							return JsonResponse(data)
						else:
							pass
					except:
						data['title'] = f'"{order_item.item.title}" added to your cart.'
						data['confirmButtonText'] = '<i class="fas fa-thumbs-up"></i>'
						return JsonResponse(data)

		else:# Si no tienes carrito creado, te crea uno. Te crea un Order si no lo tienes

			if item.quantity_in_stock >= 1:
				data = {}
				# Reduces 1 item from Stock if the user add a new item in 'order-summary'
				new_quantity = int(item.quantity_in_stock) - 1
				item_to_update = Item.objects.filter(id=product_id)
				item_to_update.update(quantity_in_stock=new_quantity)

				# Si no tienes carrito creado, te crea uno. Te crea un Order si no lo tienes
				ordered_date = timezone.now()
				order = Order.objects.create( user=request.user, ordered_date=ordered_date )
				order.items.add(order_item)
				
				try:
					qs = Order.objects.filter(user=request.user, ordered=False)
					if qs.exists():
						qty = qs[0].items.count()
						data['qty'] = qty
						data['title'] = f'"{order_item.item.title}" added to your cart.'
						data['icon'] = ''
						data['confirmButtonText'] = '<i class="fas fa-thumbs-up"></i>'
						data['timer'] = '2500'
						#messages.info(request, f'"{order_item.item.title}" added to your cart.')
						return JsonResponse(data)
					

				except Exception as e:
					data['qty'] = '1+'
					data['title'] = f'Error: {e}'
					data['confirmButtonText'] = 'OK'
					return JsonResponse(data)

			else:
				# TODO: send a message to the owner alerting that exists 0 products is Stock
				data = {}
				try:
					qs = Order.objects.filter(user=request.user, ordered=False)
					if qs.exists():
						qty = qs[0].items.count()
						data['qty'] = qty
						data['title'] = f'We are so sorry. But we do not have more of "{order_item.item.title}" in stock.'
						data['confirmButtonText'] = 'OK'
						return JsonResponse(data)
					else:
						pass
				except:
					data['title'] = f'We are so sorry. But we do not have more of "{order_item.item.title}" in stock.'
					data['confirmButtonText'] = 'OK'
					return JsonResponse(data)

		return JsonResponse(data = {'title': 'Sorry, we are having some problems procesing your request.', 'confirmButtonText': 'OK'})
		

# DONE
@login_required
def add_single_item_to_cart(request, slug): # I added slug argument
	item = get_object_or_404(Item, slug=slug) # Change pk to slug in JustDjango
	order_item, created = OrderItem.objects.get_or_create(
		item = item,
		user = request.user,
		ordered = False
	)

	order_qs = Order.objects.filter(user=request.user, ordered=False)

	if order_qs.exists():
		order = order_qs[0]
		# Check if the Order Item is in the order
		if order.items.filter(item__slug=item.slug).exists():

			# Reduces 1 item from Stock if the user add a new item in 'order-summary'
			if item.quantity_in_stock >= 1:
				new_quantity = int(item.quantity_in_stock) - 1
				item_to_update = Item.objects.filter(slug=slug)
				item_to_update.update(quantity_in_stock=new_quantity)
			else:
				# TODO: send a message to the owner alerting that exists 0 products is Stock
				messages.info(request, f'We are so sorry. But we do not have more of "{order_item.item.title}" in stock.')
				return redirect("order-summary")

			# Add 1 more of this specific item in my Ordered Items
			order_item.quantity += 1
			order_item.save()
			messages.info(request, f'Added a new item of "{order_item.item.title}" to your cart.')
			return redirect("order-summary")

		else:
			# If you don't have this Item in your Cart
			order.items.add(order_item)
			messages.info(request, f'"{order_item.item.title}" added to your cart.')
			return redirect("order-summary")

	else:
		ordered_date = timezone.now()
		order = Order.objects.create( user=request.user, ordered_date=ordered_date )
		order.items.add(order_item)
		messages.info(request, f'"{order_item.item.title}" added to your cart.')
		return redirect("order-summary")

# DELETE THIS, implemented with ajax now
@login_required
def add_directly_to_cart(request, slug):
	item = get_object_or_404(Item, slug=slug) # Retrieves the specific Item by 'slug' (could by 'pk')
	convert_to_int = 1 #request.POST['quantity']
	quantity = int(convert_to_int)
	item_discount_stock = Item.objects.filter(slug=slug) # Will discount from this Item'stuck

	# Send an email to the owner of the websit adverting that there are less than 10 items in the stock for this particular Item
	if item.quantity_in_stock <= 9:
		pass

	# Updates the Item' stock
	if item.quantity_in_stock >= int(quantity):
		new_quantity = int(item.quantity_in_stock) - int(quantity)
		new_smart_quantity = int(item.smart_quantity_stock_to_display) - int(quantity)
		item_discount_stock.update(quantity_in_stock=new_quantity, smart_quantity_stock_to_display=new_smart_quantity)
		if item.smart_quantity_stock_to_display <=5:
			increment_smart_quantity = 150
			item_discount_stock.update(smart_quantity_stock_to_display=increment_smart_quantity)

		order_item, created = OrderItem.objects.get_or_create(
			item = item,
			user = request.user,
			quantity = quantity,
			ordered = False
		)
		item_discount_stock = Item.objects.filter(slug=slug) # DELETE is duplicated
		# Updates the stuck
		if item.quantity_in_stock >= int(quantity):
			new_quantity = int(item.quantity_in_stock) - int(quantity)
			item_discount_stock.update(quantity_in_stock=new_quantity)

		order_qs = Order.objects.filter(user=request.user, ordered=False)

		if order_qs.exists():
			order = order_qs[0]
			# Ceck if the Order Item is in the order. If exists will prevent to re-add this Item to Cart, and redirect to 'order-summary'
			if order.items.filter(item__slug=item.slug).exists():
				#order_item.quantity = quantity # +=1
				#order_item.ordered = True
				messages.info(request, f'"{order_item.item.title}" is already in your cart.')
				return redirect("order-summary")

			else:
				added = order.items.add(order_item)
				navbarcategories =  Category.objects.filter(will_be_shown_as_recomendation=True).order_by('order_to_display').all()
				countcatgnav = navbarcategories.count()
				context = {
					'items': Item.objects.all(),
					'carousels': Carousel.objects.all(),
					'navbarcategories':navbarcategories,
					'countcatgnav':countcatgnav,
					'favorit_color_theme': request.session.get('color_theme'),

					'timer': '2500',
					'message':f"{quantity} item added to your cart.",
					'position': 'center',
					'icon': 'success', #success, warning, info, question
					'confirmButtonText': '<i class="fas fa-cart-plus"></i>',

				}
				return render(request, 'home/home_page.html', context)
				#data = {}
				#data = list(Order.objects.values())
				#messages.info(request, f'{quantity} item added to your cart. This')
				#data['']
				#return redirect('/')
				#return JsonResponse(data, safe=False, status=200)

		else:
			# Create an active order (First item in your cart)
			ordered_date = timezone.now()
			order = Order.objects.create( user=request.user, ordered_date=ordered_date )
			added = order.items.add(order_item)
			#data = list(Order.objects.values())
			navbarcategories =  Category.objects.filter(will_be_shown_as_recomendation=True).order_by('order_to_display').all()
			countcatgnav = navbarcategories.count()
			context = {
				'items': Item.objects.all(),
				'carousels': Carousel.objects.all(),
				'navbarcategories':navbarcategories,
				'countcatgnav':countcatgnav,
				'favorit_color_theme': request.session.get('color_theme'),

				'timer': '2500',
				'message':f"{quantity} item added to your cart.",
				'position': 'center',
				'icon': 'success', #success, warning, info, question
				'confirmButtonText': '<i class="fas fa-cart-plus"></i>',
			}
			return render(request, 'home/home_page.html', context)

	# If quantity to discount to Item > quantity_in_stock
	else:
		messages.info(request, f'The quantity {quantity} you are trying to buy is higher that ower stock. We only have {item.quantity_in_stock}')
		return redirect("product-detail", slug=slug)

# Next function is called when the user click in the TRASH CAN btn, in the checkout-page
@login_required
def remove_from_cart(request, slug):
	item = get_object_or_404(Item, slug=slug)
	order_qs = Order.objects.filter(
		user=request.user,
		ordered=False
	)
	try:
		# Check if the deleted Item exists in the Cart
		orderItem = OrderItem.objects.get(user=request.user, item__slug=slug)
	except:
		messages.info(request, 'The Item selected is not in your cart.')
		return redirect('/')

	# If Check if the Item exists in the Full Cart
	if order_qs.exists():
		order = order_qs[0]

		if order.items.filter(item__slug=item.slug).exists():
			order_item = OrderItem.objects.filter(
				item=item,
				user=request.user,
				ordered=False
			)[0]

			# Add 1 item in my Stock if the user reduce this specific item in 'order-summary'
			new_quantity = int(item.quantity_in_stock) + 1
			item_to_update = Item.objects.filter(slug=slug)
			item_to_update.update(quantity_in_stock=new_quantity)

			order.items.remove(order_item)	#  CHECK THIS PIECE OF CODE
			orderItem.delete()
			messages.info(request, "\""+order_item.item.title+"\" removed from your cart.")
			return redirect("order-summary")

		else: # Si hay Order, pero este Item no está en tu Cart
			messages.info(request, "This item was not in your cart")
			return redirect("order-summary")

	else:	# Si no hay Order
		context = {
			'items': Item.objects.all(),
			'favorit_color_theme': request.session.get('color_theme'),
			'message':f"You don't have items in your cart.",
			'position': 'center',
			'icon': 'warning', #success, warning, info, question
			'confirmButtonText': 'OK',
			'showCloseButton': 'true',
		}
		messages.info(request, "You don't have items in your cart.")
		return redirect("order-summary")

@login_required
def remove_single_item_from_cart(request, slug):
	item = get_object_or_404(Item, slug=slug)
	order_qs = Order.objects.filter(
		user=request.user,
		ordered=False
	)

	if order_qs.exists():
		order = order_qs[0]

		if order.items.filter(item__slug=item.slug).exists():
			order_item = OrderItem.objects.filter(
				item=item,
				user=request.user,
				ordered=False
			)[0]

			if order_item.quantity > 1:

				# Add 1 item in my Stock if the user reduce this specific item in 'order-summary'
				new_quantity = int(item.quantity_in_stock) + 1
				item_to_update = Item.objects.filter(slug=slug)
				item_to_update.update(quantity_in_stock=new_quantity)

				order_item.quantity -= 1
				order_item.save()
			else:
				return redirect('remove-from-cart', slug=slug)

			messages.info(request, "\""+order_item.item.title+"\" quantity was updated.")
			return redirect("order-summary")

		else:
			messages.info(request, "This item was not in your cart")
			return redirect("order-summary")

	else:
		navbarcategories =  Category.objects.filter(will_be_shown_as_recomendation=True).order_by('order_to_display').all()
		countcatgnav = navbarcategories.count()
		context = {
		'items': Item.objects.all(),
		'carousels': Carousel.objects.all(),
		'navbarcategories':navbarcategories,
		'countcatgnav':countcatgnav,
		'favorit_color_theme': request.session.get('color_theme'),
		'message':f"You don't have items in your cart.",
		'position': 'center',
		'icon': 'warning', #success, warning, info, question
		'confirmButtonText': 'OK',
		'showCloseButton': 'true',
	}
	#return render(request, 'home/home_page.html', context)
	messages.info(request, "You don't have items in your cart.")
	return redirect("/")

@login_required
def clean(request):
	client_order = Order.objects.filter(user=request.user)
	client_order_items = OrderItem.objects.filter(user=request.user)


	if client_order.exists() and client_order_items.exists():

		items_ordered_by_client = client_order_items.all()

		# Iterate in the Items Ordered by the client, and updates my stock
		for item in items_ordered_by_client:
			Qty = item.quantity
			the_slug = item.item.slug
			new_quantity = int(item.item.quantity_in_stock) + int(Qty)
			item_to_update = Item.objects.filter(slug=the_slug)
			item_to_update.update(quantity_in_stock=new_quantity)

		client_order[0].delete()
		client_order_items.delete()
		context = {
			'items': Item.objects.all(),
			'favorit_color_theme': request.session.get('color_theme'),

			'timer': '2500',
			'message':f"All your orders have been cleaned.",
			'position': 'center',
			'icon': 'success', #success, warning, info, question
			'confirmButtonText': 'OK',
		}
		#return render(request, 'home/home_page.html', context)
		messages.info(request, "All your orders have been cleaned.")
		return redirect("/")

