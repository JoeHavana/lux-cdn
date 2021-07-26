import datetime
import allauth.app_settings
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from ckeditor import fields as ckedit
# from django_extensions.db.fields import AutoSlugField 
#from django.contrib.auth.models import User
#import requests  To work with class Latitude

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from wagtail.core import blocks
from wagtail.core.models import Page, Orderable, PageManager, PageQuerySet
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.blocks import *
from wagtail.admin.edit_handlers import (
	FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, PageChooserPanel, StreamFieldPanel, ObjectList, TabbedInterface
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from django.db.models.signals import (
	post_delete, # Used
	post_init, 
	post_migrate,
	post_save,
	pre_save, 
	pre_delete,
	pre_init,
	m2m_changed, 
)
from django.shortcuts import reverse
#from django.dispatch import receiver, signals # No-Used
from core.streams.blocks import *
from core.streams.choices import *


today = datetime.date.today()
now = datetime.datetime.now()

SHOW_AS_CHOICES = [	# New from justdj
	('CLT','Clusters'),
	('CI','Carousel')
]

LABEL_COLOR_CHOICES = [	# New from justdj
	('P','primary'),
	('S','secondary'),
	('D','danger'),
]

ADDRESS_CHOICES = [	# New from justdj
	('B','Billing'),
	('S','Shipping'),
]

COUPON_CHOICES = [
	('P', 'Percent'),
	('Q', 'Quantity'),
]

ORDER_CHOICES = [
	('St','Started'),
	('Ab','Abandoned'),
	('Fi','Finished'),
]

# JustDjango
class UserProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
	one_click_purchasing = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username

# Not in DjustDjango
class ItemImages(Orderable):
	image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, related_name="+", on_delete=models.CASCADE)
	alternative_text = models.CharField(max_length=150, blank=True, null=True)

	page = ParentalKey("Item", related_name="images_of_item")

	panels = [
		MultiFieldPanel([
			ImageChooserPanel("image"),
			FieldPanel("alternative_text"),
		], heading="Single Menu Item")
	]

	def __str__(self):
		return self.image.title

	class Meta:
		verbose_name = "Image for an Item"
		verbose_name_plural = "Images for the Items"

# from justdj => Category
class ItemCategory(models.Model):
	category_name = models.CharField(unique=True, blank=False, null=True, max_length=150, editable=True, help_text="Name must be shorts. If you would like to give extra information, fill out in 'Category description'.")
	slug =  models.CharField(unique=True, blank=False, null=True, max_length=150, editable=True, help_text="Slugs must be uniques")
	category_description = models.TextField(blank=True, null=True, help_text="Give a small description")
	tags_related = models.ManyToManyField("store.ItemTag", related_name="+", blank=True, help_text="KeyWords will be used in order to filtering")
	image_related = models.ForeignKey("wagtailimages.Image", null=True, blank=True, related_name="+", on_delete=models.CASCADE)
	image_description = models.CharField(blank=False, null=True, max_length=150, editable=True, help_text='Give a short description for "Image related". This is very important for the SEO.')
	priority = models.PositiveIntegerField(unique=True, default=1, editable=True)
	will_be_recomended = models.BooleanField(default=False, blank=True, null=True)
	
	items_related = models.ManyToManyField("Item", related_name="+", blank=True, editable=True)

	panels = [
		MultiFieldPanel([
			FieldPanel("category_name"),
			FieldPanel("category_description"),
			ImageChooserPanel("image_related"),
			FieldPanel("image_description"),
			FieldPanel("priority"),
			FieldPanel("will_be_recomended"),
			FieldPanel("slug"),
		], heading="Categories")
	]

	def __str__(self):
		return self.category_name

	class Meta:
		verbose_name = 'Item Category'
		verbose_name_plural = 'Items Categories'

	def get_absolute_url(self):
		return reverse("category-detail", kwargs={ "slug":self.slug }) # core = appname; product is my url_name, in urls.py

# from justdj => Tag
class ItemTag(Orderable):
	tag_name = models.CharField(max_length=150, blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)
	slug =  models.SlugField(editable=True, unique=True, help_text="Slugs must be uniques")

	page = ParentalKey("Item", related_name="tags_of_item")

	panels = [
		MultiFieldPanel([
			FieldPanel("tag_name"),
			FieldPanel("slug"),
			FieldPanel("active"),
		], heading="Tags")
	]

	def __str__(self):
		return self.tag_name
		
	class Meta:
		verbose_name = 'Item Tag'
		verbose_name_plural = 'Item Tags'


class EmailsToAlertMinimalStock(Orderable):
	""" the emails used to send a message when the Stock get to the minimal quantity """
	email = models.EmailField(blank=True, null=True)
	page = ParentalKey("Item", related_name="emails_to_alert")

	def __str__(self):
		return self.email
		
	class Meta:
		verbose_name = 'Email to alert'
		verbose_name_plural = 'Emails to alert'

# In JustDjango (Extended)
class Item(ClusterableModel):
	# the_product_file = models.FileField(upload_to='jhsdsgsgs/%Y/%m/%d', null=True, blank=False, editable=True, help_text="The folder containing the product you want to sale.")
	title = models.CharField(max_length=100, editable=True, unique=True, help_text="The title of this particular Item")
	slug = models.SlugField(editable=True, unique=True, help_text="Slugs must be uniques")
	is_available = models.BooleanField(default=True)
	
	real_price = models.DecimalField("Current Price", max_digits=9,decimal_places=2, blank=False, null=True, editable=True, help_text="Set the current price of this Item.")
	previos_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, editable=True, help_text="Previus price will be shown dotted.")
	discount_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, editable=True, help_text="Set an amount to be discounted if has.")
	
	quantity_in_stock = models.PositiveIntegerField(blank=True, null=True, default=1, help_text="Set the real number of Items you have in stock.")
	# IMPORTANT: smart_quantity_stock_to_display = models.PositiveIntegerField(blank=True, null=True, help_text="Set an smart number that you would like to show to the clients as 'stock' for this specific Item.")
	alert_minimal_stock = models.PositiveIntegerField("Alert when the quantity stock get to", blank=True, null=True, default=1, help_text="An email will sent when the amount in stock get to this number.")
	
	short_description = models.TextField(blank=True, null=True, help_text="Give a short description for this Item. No more that 250 characters.")
	full_description = ckedit.RichTextField(blank=True, null=True, help_text="Give a complete description for this Item")
	# real_mount_of_downloads_to_display = models.PositiveIntegerField(blank=True, null=True)
	# smart_quantity_of_downloads_to_display = models.CharField(max_length=7, blank=True, null=True, default="1.3K", help_text="Show a smart quantity of downloads for this products. This could be important for marketing.")
	smart_rating_stars_to_display = models.CharField("Custom Rate", max_length=3, default="4.5", choices=[("1","1",),("1.5","1.5",),("2","2",),("2.5","2.5",),("3","3",),("3.5","3.5",),("4","4",),("4.5","4.5",),("5","5",),], blank=True, null=True, help_text="Choose an option given to be shown in the 'Item Page'.")
	real_rating_by_users = models.FloatField(blank=True, null=True, editable=True)
	rated_by =  models.PositiveIntegerField(default=0, blank=True, null=True, editable=True)
	real_rate_average = models.FloatField(blank=True, null=True, editable=True)
	comments_in_ratings = models.TextField(blank=True, null=True)
	commented_by_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,)
	
	main_picture_of_presentation = models.ForeignKey("wagtailimages.Image", on_delete=models.SET_NULL, null=True, blank=False, related_name="+")
	video_trailer = models.FileField(upload_to='VideoTrailer/%Y/%m/%d', null=True, blank=True, editable=True, help_text="A video trailer")
	categories = models.ManyToManyField(ItemCategory, blank=True, help_text="Select if exists one or more categories related to this Item. Press 'CTRL' to select multiple.")
	# DELETE, now have InlinePanel | tags = models.ManyToManyField(ItemTag, blank=True, help_text="Choose if exists one or more tags related to this Item.")
	
	panels = [
		#FieldPanel("the_product_file"),
		MultiFieldPanel([
			FieldPanel("title"),
			FieldPanel("slug"),
			FieldPanel("is_available"),
			FieldPanel("real_price"),
			FieldPanel("previos_price"),
			FieldPanel("quantity_in_stock"),
			FieldPanel("smart_quantity_stock_to_display"),
			FieldPanel("alert_minimal_stock"),
			InlinePanel("emails_to_alert", label="one or more emails, to send a message when the stock quantity get to the number selected above."),
			# DELETE 	FieldPanel("discount_price"),
			FieldPanel("short_description"),
			FieldPanel("full_description"),
			FieldPanel("smart_rating_stars_to_display"),
			#FieldPanel("real_rating_by_users"),
			#FieldPanel("rated_by"),
			#FieldPanel("real_rate_average"),
		], heading="Main Data"),
		MultiFieldPanel([
			ImageChooserPanel("main_picture_of_presentation"),
			InlinePanel("images_of_item", label="Some Images related to this particular Item"),
			FieldPanel("video_trailer"),
		], heading="Media data related"),
		MultiFieldPanel([
			FieldPanel("categories"),
			InlinePanel("tags_of_item", label="Tags related to this particular Item"),
		], heading="Tags & Categories related"),
	]

	def __str__(self):
		return self.title
		
	class Meta:
		verbose_name = 'Item'
		verbose_name_plural = 'Items'

	def set_rating_url(self):
		return reverse("rating-items", kwargs={ "slug":self.slug })

	def get_absolute_url(self):
		return reverse("product-detail", kwargs={ "slug":self.slug }) # core = appname; product is my url_name, in urls.py

	def get_add_to_cart_url(self):
		return reverse("add-to-cart", kwargs={ "slug":self.slug }) #reverse("core:add-to-cart", kwargs={ "pk":self.pk })

	def get_add_directly_to_cart_url(self):
		return reverse("add-single-item-to-cart", kwargs={ "slug":self.slug })
		
	def get_remove_from_cart_url(self):
		return reverse("remove-from-cart", kwargs={ "slug":self.slug })
'''
	def get_add_directly_with_ajax(self):
		return reverse("add-directly-with-ajax", kwargs={ "slug":self.slug })
'''

# In JustDjango (Extended)
class Address(models.Model):	# BillingAddress 
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	#apartment_address = models.CharField(max_length=100, blank=True, null=True)
	street_address = models.CharField(max_length=150, blank=False, null=True)
	city_address = models.CharField(max_length=50, default='Miami', blank=False, null=True)
	country = CountryField(multiple=False, default='United States', blank=True, null=True)
	zipfield = models.CharField(max_length=150, blank=False, null=True)
	address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES, editable=True)
	default = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username

	class Meta:
		verbose_name = 'Address'
		verbose_name_plural = 'Addresses'

# In JustDjango
class Payment(models.Model):
	stripe_charge_id = models.CharField(max_length=50)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
	amount = models.DecimalField(max_digits=9,decimal_places=2)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.username

# from JustDjango (Extended)
class Coupon(models.Model):
	code = models.CharField(max_length=50, unique=True, editable=True)
	amount = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, help_text='Fill this field, only if you have selected "Type of discount" as "Quantity" down bellow.')
	percent = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, help_text='Fill this field, only if you have selected "Type of discount" as "Percent" down bellow.')
	type_of_discount = models.CharField(max_length=1, default='Q', editable=True, choices=COUPON_CHOICES)
	last_date_of_the_coupon_live = models.DateField(blank=True, null=True, editable=True, help_text="This field is not required, may be stay empty")
	disable = models.BooleanField(default=False, help_text="Select this to disable this coupon.")

	def __str__(self):
		if self.amount and self.type_of_discount == 'P':
			return f'ERROR: "Amount" field must to be empty, if "Type of discount" = Percent'
		elif self.percent and self.type_of_discount == 'Q':
			return f'ERROR: "Percent" field must to be empty, if "Type of discount" = Quantity'
		elif self.amount and self.percent:
			return f'ERROR: "Amount" and "Percent" can not be both selected'
		elif not self.amount and not self.percent:
			return f'ERROR: You have to fill in any of the following fields, "Amount" or "Percent"'
		else:
			return self.code

# Items in Carts, from JustDjango
class OrderItem(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	user = models.ForeignKey(allauth.app_settings.USER_MODEL, on_delete=models.CASCADE)
	ordered = models.BooleanField(default=False)
	quantity = models.IntegerField(default=1)

	def __str__(self):
		return f'{self.quantity} of {self.item.title}'

	def get_total_item_price(self):
		return self.quantity * self.item.real_price

	def calculate_discount_price(self):
		return self.item.real_price - self.item.discount_price

	def get_total_discount_item_price(self):
		return self.quantity * self.calculate_discount_price()

	def get_amount_saved(self):
		total = self.get_total_item_price() - self.get_total_discount_item_price()
		return total

	def get_final_price(self):
		if self.item.discount_price:
			return self.get_total_discount_item_price()
		else:
			return self.get_total_item_price() # Remove the int()

			
	class Meta:
		verbose_name = 'Ordered Item'
		verbose_name_plural = 'Items in Carts'
		ordering = ['item']

# In JustDjango (Extended)
class Order(models.Model): # The Full Cart
	""" 
	1  Item added to cart
	2. Adding billing address (Failed checkout)
	3. Payment (Preprocessing, processing, packaging, etc..)
	4. Being delivered
	5. Received
	6. Refounds
	"""
	user = models.ForeignKey(allauth.app_settings.USER_MODEL, on_delete=models.CASCADE)
	status = models.CharField(max_length=2, choices=ORDER_CHOICES, default='St', blank=False, null=False)
	ref_code = models.CharField(max_length=60, blank=True, null=True, unique=True)
	ordered = models.BooleanField(default=False)
	items = models.ManyToManyField(OrderItem)
	start_date = models.DateTimeField(auto_now_add=True)
	ordered_date = models.DateTimeField()
	updated_at = models.DateTimeField(null=True)
	billing_address = models.ForeignKey(Address, related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
	shipping_address = models.ForeignKey(Address, related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
	payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
	coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
	being_delivered = models.BooleanField(default=False)
	received = models.BooleanField(default=False)
	refund_requested = models.BooleanField(default=False)
	refund_granted = models.BooleanField(default=False)
	sub_price = models.DecimalField(max_digits=9,decimal_places=2, blank=True, null=True, editable=True)
	discount = models.DecimalField(max_digits=9,decimal_places=2, blank=True, null=True, editable=True)
	total_price = models.DecimalField(max_digits=9,decimal_places=2, blank=True, null=True, editable=True)

	def __str__(self):
		return self.user.username

	def get_total(self):
		total = 0
		for order_item in self.items.all():
			total += order_item.get_final_price()
		return total

	def get_total_with_coupon_code(self):
		if self.coupon.last_date_of_the_coupon_live == today:
			return f'Coupon out of day'
		elif self.coupon.type_of_discount == 'Q':
			total = 0
			for order_item in self.items.all():
				total += order_item.get_final_price()
			total -= self.coupon.amount
			if total < 0:
				return False
			else:
				return total

		elif self.coupon.type_of_discount == 'P':
			total = 0
			for order_item in self.items.all():
				total += order_item.get_final_price()

			percent_precalculated = float(self.coupon.percent) * 0.01 # Llevar percent a %
			quantity_to_discount = float(total) * percent_precalculated # Calcular el % del total
			discount_from_total = float(total) - quantity_to_discount # Descontar el % calculado al total
			total = discount_from_total # Asignar a la var total el nuevo coeficiente
			if total < 0:
				return False
			else:
				return total
		else:
			return False

	class Meta:
		verbose_name = 'Order'
		verbose_name_plural = 'Orders'
		ordering = ['-pk']

# In JustDjango
class Refund(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	reason = models.TextField(blank=False, null=True)
	accepted = models.BooleanField(default=False)
	email = models.EmailField(blank=False, null=True)

	def __str__(self):
		return f'{self.pk}'

# In JustDjango
def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)