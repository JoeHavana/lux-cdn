from django import forms
from django.db import models
from django.shortcuts import render
from django.http import JsonResponse
from django_comments_xtd.models import XtdComment
from django_extensions.db.fields import AutoSlugField
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
#from django.utils.tranlation import gettext_lazy as _

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable, PageManager, PageQuerySet
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import *
from wagtail.admin.edit_handlers import (
	FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, 
	PageChooserPanel, StreamFieldPanel, ObjectList, TabbedInterface
)
from wagtail.admin.forms import WagtailAdminModelForm, WagtailAdminPageForm
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.api.fields import ImageRenditionField
from wagtail.embeds.models import Embed
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.search import index
from wagtail.api import APIField

from rest_framework.fields import Field
from ckeditor import fields as ckedit
#from wagtailstreamforms.blocks import WagtailFormBlock
# from wagtailcodeblock.blocks import CodeBlock

from core.streams.blocks import *
from core.streams.choices import *
#from core.carousels.models import *
from core.store.models import *
from core.site_settings.models import *
from core.menus.models import *

#### 	Page Menus Start 	###
class MenuItem(Orderable):
	""" Menu Item, only for DropDowns """
	link_title = models.CharField(blank=False, null=True, max_length=50)
	link_url = models.URLField(max_length=500, blank=True, null=True)
	link_page = models.ForeignKey("wagtailcore.Page", null=True, blank=True, related_name="+", on_delete=models.CASCADE)
	open_in_new_tab = models.BooleanField(default=False, help_text='Default is "False"')
	rel_attribute = models.CharField(max_length=250, blank=True, null=True)

	page = ParentalKey("Menu", related_name="menu_items", null=True)

	panels = [
		FieldPanel("link_title"),
		FieldPanel("link_url"),
		PageChooserPanel("link_page"),
		FieldPanel("open_in_new_tab"),
		FieldPanel("rel_attribute"),
	]

	

class Menu(ClusterableModel):
	""" DropDown Menu Class """
	title = models.CharField(max_length=50, editable=True, unique=True)
	slug = AutoSlugField(populate_from="title", editable=True, unique=True)
	menu_type = models.CharField(max_length=3, default="pgs", blank=True, null=True)
	page = ParentalKey("home.HomePage", related_name="page_dropdown_menu")

	panels = [
		MultiFieldPanel([
			FieldPanel("title"),
		], heading="Dropdown Menu"),
		InlinePanel("menu_items", min_num=1, label="Links")
	]

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = "Menu with Dropdown"
		verbose_name_plural = "Menus with Dropdown"


class SingleMenuItem(Orderable):
	title = models.CharField(blank=False, null=True, max_length=50)
	menu_type = models.CharField(max_length=3, default="sng", blank=True, null=True)
	open_in_new_tab = models.BooleanField(default=False, help_text='Default is "False"')
	rel_attribute = models.CharField(max_length=250, blank=True, null=True)
	link_url = models.URLField(max_length=500, blank=True, null=True)
	link_page = models.ForeignKey("wagtailcore.Page", null=True, blank=True, related_name="+", on_delete=models.CASCADE)
	page = ParentalKey("home.HomePage", related_name="page_single_menu")

	panels = [
		MultiFieldPanel([
			FieldPanel("title"),
			FieldPanel("link_url"),
			PageChooserPanel("link_page"),
			FieldPanel("open_in_new_tab"),
			FieldPanel("rel_attribute"),
		], heading="Single Menu Item")
	]

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = "Single Menu"
		verbose_name_plural = "Single Menus"

#### 	Page Menus End 	###
#####################################################################################
class ItemCardsCustomized(Orderable):
	""" DELETE NEXT CLASS """
	id = models.AutoField(primary_key=True, default=1)
	label_text = models.CharField(max_length=50, blank=True, null=True, editable=True)
	label_color = models.CharField(max_length=7, choices=COLOR_CHOICES, blank=True, null=True, editable=True)
	footer_text = models.CharField(max_length=500, blank=True, null=True, editable=True)
	item = models.ForeignKey("store.Item", null=True, blank=True, related_name="+", on_delete=models.CASCADE)
	
	page = ParentalKey("InlineSectionCards", related_name="item_card")

	panels = [
		MultiFieldPanel([
			FieldPanel("item"),
			FieldPanel("label_text"),
			FieldPanel("text_label_color"),
			FieldPanel("background_color_of_label"),
		], heading="Categories of Items")
	]

	def __str__(self):
		return self.item.title

	class Meta:
		verbose_name = "Item"
		verbose_name_plural = "Items"


class InlineSectionCards(ClusterableModel):
	""" DELETE NEXT CLASS """
	section_ID = models.CharField(max_length=50, blank=True, null=True)
	section_title = models.CharField(max_length=250, blank=True, null=True)
	section_subtitle = models.TextField(blank=True, null=True)
	link_page = models.ForeignKey("wagtailcore.Page", null=True, blank=True, related_name="+", on_delete=models.CASCADE, help_text="This are used to point into an internal Page.")
	link_external_url = models.URLField(blank=True, null=True, help_text="This are used to point into an external Link.")
	open_in_a_new_tab = models.BooleanField(default=False, blank=True, null=True)
	followed_by_the_Google_Spiders = models.BooleanField(default=True, blank=True, null=True)

	panels = [
		MultiFieldPanel([
			FieldPanel("section_ID"),
			FieldPanel("section_title"),
			FieldPanel("section_subtitle"),
		], heading="Section Data"),
		MultiFieldPanel([
			PageChooserPanel("link_page"),
			FieldPanel("link_external_url"),
		], heading='If you want to convert the "Section title" into a link, select one of the next choices.'),
		InlinePanel("item_card", label="Item related")
	]

	def __str__(self):
		return self.section_title

	class Meta:
		verbose_name = "Inline Section of Cards"
		verbose_name_plural = "Inline Sections of Cards"

# Esta es la clase que trabaja con el carrusel del header
class HomePageCarouselTruncated(Orderable):
	id = models.AutoField(primary_key=True, default=1)
	page = ParentalKey("home.HomePage", related_name="carousel_images")
	carousel_image = models.ForeignKey("wagtailimages.Image", related_name="+", blank=True, null=True, on_delete=models.SET_NULL)

	link_url = models.URLField(max_length=500, blank=True, null=True)
	link_page = models.ForeignKey("wagtailcore.Page", null=True, blank=True, related_name="+", on_delete=models.CASCADE)
	open_in_a_new_tab = models.BooleanField(blank=True, null=True)
	rel_attribute = models.CharField(max_length=250, blank=True, null=True)

	panels = [
		ImageChooserPanel("carousel_image"),
		MultiFieldPanel([
			FieldPanel("link_url"),
			PageChooserPanel("link_page"),
		], heading="Select one of the next options if you want to add a hidden link."),
		MultiFieldPanel([
			FieldPanel("open_in_a_new_tab"),
			FieldPanel("rel_attribute"),
		], heading="Select the behavior of the link")
	]


class HomePage(Page):
	AUTOFILL_ITEMS_CHOICES = [
		("1","Before the Auto-Generated Items"),
		("2","After the  Auto-Generated Items"),
		("3","Don't appear."),
	]
	template = 'home/home_page.html'
	#parent_page_type = ['wagtailcore.Page'] # appname.ModelName
	# subpage_types = ['blog.BlogSinglePage', 'contact.FormPage'] # appname.ModelName
	search_auto_update = False
	#max_count = 1

# Header Panel
	alert_about_cookies = models.BooleanField(default=True, null=True, blank=True)
	custom_css_file	= models.ForeignKey("wagtaildocs.Document", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
	custom_js_file	= models.ForeignKey("wagtaildocs.Document", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
	favicon_icon = models.ForeignKey("wagtailimages.Image", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
	main_title_of_the_page = models.CharField(max_length=350, blank=False, null=True, help_text='This is the "<h1>"')
	main_title_color = models.CharField(max_length=7, choices=COLOR_CHOICES, blank=True, null=True)
	header_subtitle = models.CharField(max_length=500, blank=True, null=True)
	subtitle_color = models.CharField(max_length=7, choices=COLOR_CHOICES, blank=True, null=True)

# Navigation Menu
	use_general = models.BooleanField("Use the general menu from 'Snippets'", default=True, blank=True, null=True, help_text="Default is 'True', if False you should customize the navigation menu in this panel.")
	show_user_opt = models.BooleanField("Show the User'Options", default=True, blank=True, null=True, help_text="Default is 'True'.")
	show_search = models.BooleanField("Show the 'Search bar'.", default=True, blank=True, null=True, help_text="Default is 'True'.")
	show_cart = models.BooleanField("Show the 'User Cart'.", default=True, blank=True, null=True, help_text="Default is 'True'.")

# Aside Panel
	aside_section = models.BooleanField(default=False, blank=True, null=True, help_text="Show a column aside with extra content.")
	aside_floating = models.CharField(max_length=1, choices=[("l", "Left",),("r","Right",),], default="r", blank=True, null=True, help_text="Selects where the aside column will be shown.")
	background_color = models.CharField(max_length=7, choices=COLOR_CHOICES, blank=True, null=True, help_text="Selects the background color of the aside column")

# Promote Panel
	meta_language = models.CharField(max_length=2, choices=META_LANGUAGES, blank=True, null=True, help_text="Select in what language the content of this page is. Default is 'en'.")
	meta_keywords = models.TextField(blank=True, null=True, help_text="All your keywords you add here, must to be in your content.")
	meta_revisit_after = models.PositiveIntegerField(blank=True, null=True, default="365", help_text="Select how many days Google Spiders could revisit this page. Default is 365 days.")
	meta_robots = models.CharField(max_length=17, blank=True, null=True, choices=META_ROBOTS_CHOICE, help_text="Deside if this page will be Indexed and/or Followed by the Google Spiders. Default is 'index, follow'.")
	
# Content Panel
	# DELETE Carousel_of_One_Image = ParentalManyToManyField("carousels.CarouselSimpleImage", blank=True)
	# DELETE Carousel_of_Multiple_Images = ParentalManyToManyField("carousels.CarouselMultipleImages", blank=True)
	auto_fill_products = models.BooleanField(default=True, blank=True, null=True, help_text='If selected, the products "availables" in the database will be shown automatically.')
	auto_generated_items = models.CharField(max_length=1, choices=AUTOFILL_ITEMS_CHOICES, default="3", blank=True, null=True, help_text='Select where you would like the "Cuistomized Content" appear.')
	custom_css = models.TextField("Custom CSS", blank=True, null=True, help_text="Paste the custom css for this particular page. Including all HTML tags")
	custom_js = models.TextField("Custom JavaScript", blank=True, null=True, help_text="Paste the custom JavaScript for this particular page. Including <script><script/> tag")
#	inline_cards_of_items = models.ManyToManyField("InlineSectionCards",  blank=True)

	content = StreamField(
		[
			("intro_home", IntroSectionBGImageCentederTextBlock()),
			("custom_html", CustomHTML()),
			("divider", DividerBlock()),
			("accordion", ColapsibleBlock()),
			("summary", SummaryBlock()),
			("icon_link", CardWithIconBlock()),
			('counter_up', CountersBlock()),
			('img_info_bar', InfoBlock()),
			("pricing_card", PricingCardsBlock()),
			("jumbotron", JumbotronBlock()),
			("contactmap", ContactMapBlock()),
		],
		null=True,
		blank=True,
	)

	navbar_panel = [
		MultiFieldPanel([
			FieldPanel("use_general"),
			FieldPanel("show_user_opt"),
			FieldPanel("show_search"),
			FieldPanel("show_cart"),
		]),
		MultiFieldPanel([
			InlinePanel("page_single_menu", help_text="Add a Menu to the Navigation Bar, for this particular page.", label="a Single Memu"),
			InlinePanel("page_dropdown_menu", help_text="Add a DropDown Menu to the Navigation Bar, for this particular page.", label="a DropDown Menu"),
		], heading="Navigation Menu Bar"),
	]

	content_panels = Page.content_panels + [
		FieldPanel("custom_css"),
		FieldPanel("custom_js"),
		FieldPanel("auto_fill_products"),
		FieldPanel("auto_generated_items"),
		MultiFieldPanel([
			StreamFieldPanel("content"),
		], heading="Main Section"),
#		MultiFieldPanel([
#			FieldPanel("Carousel_of_One_Image", widget=forms.CheckboxSelectMultiple),
#			FieldPanel("Carousel_of_Multiple_Images"),
#		], heading="Carousels"),
#		MultiFieldPanel([
#			FieldPanel("inline_cards_of_items"),
#		], heading="Inline Itemts")
	]

	header_panels = [
		MultiFieldPanel([
			DocumentChooserPanel("custom_css_file"),
			DocumentChooserPanel("custom_js_file"),
		], heading="Upload the CSS and JavaScript files for this particular Page. (Or maybe the generals one)"),
		MultiFieldPanel([
			ImageChooserPanel("favicon_icon"),
		], heading="Icon of Page Tab"),
		MultiFieldPanel([
			FieldPanel("main_title_of_the_page"),
			FieldPanel("main_title_color"),
			FieldPanel("header_subtitle"),
			FieldPanel("subtitle_color"),
		], heading="Header Content"),
		MultiFieldPanel([
			InlinePanel("carousel_images", help_text="Add a Carousel of Images. At less one.", min_num=1),
		], heading="Carousel of Images"),
	]

	sidebar_panels = [
		MultiFieldPanel([
			FieldPanel("aside_section"),
			FieldPanel("aside_floating"),
			FieldPanel("background_color"),
		], heading="Aside Column")
	]

	promote_panels = Page.promote_panels + [
		MultiFieldPanel([
			FieldPanel("meta_language"),
			FieldPanel("meta_keywords"),
			FieldPanel("meta_revisit_after"),
			FieldPanel("meta_robots"),
		], heading="Extra page configuration for the SEO.")
	]

	edit_handler = TabbedInterface([
		ObjectList(header_panels, heading="Header"),
		ObjectList(navbar_panel, heading="Navigation Bar"),
		ObjectList(content_panels, heading="Content"),
		ObjectList(sidebar_panels, heading="Aside"),
		ObjectList(promote_panels, heading="Promote"),
		ObjectList(Page.settings_panels, heading="Settings"),
	])

#	search_fields = Page.search_fields + [
#        index.SearchField('main_title_of_the_page'), # These are used for performing full-text searches on your models, usually for text fields.
#        index.FilterField('header_subtitle'), # These are added to the search index but are not used for full-text searches
 
#    	 index.RelatedFields('author', [ # This allows you to index fields from related objects. It works on all types of related fields
#            index.SearchField('name'),
#            index.FilterField('date_of_birth'),
#        ]),
#    ]

	def get_context(self, request, *args, **kwargs):
		context = super().get_context(request, *args, **kwargs)
		#context['carousel_one_image'] = self.Carousel_of_One_Image.all
		#context['carousel_multiple_images'] = self.Carousel_of_Multiple_Images.all
		context['items'] = Item.objects.filter(is_available=True).distinct()
	#	context['inline_cards'] = self.inline_cards_of_items.all
		context['nav2categories'] = ItemCategory.objects.filter(will_be_recomended=True).order_by('priority').all()
		context['countcatgnav2'] = ItemCategory.objects.filter(will_be_recomended=True).order_by('priority').count()
		
		return context

	class Meta:
		verbose_name = 'Products Listing Page'
		verbose_name_plural = 'Products Listing Pages'
