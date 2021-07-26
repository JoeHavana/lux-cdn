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
	FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, PageChooserPanel, StreamFieldPanel, ObjectList, TabbedInterface
)
from wagtail.admin.forms import WagtailAdminModelForm, WagtailAdminPageForm
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.api.fields import ImageRenditionField
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
# from wagtailtrans.models import TranslatablePage

from core.streams.blocks import *
from core.streams.choices import *
from home.models import *
#from lux.abstracts import *


class ImageSerializedField(Field):
	def to_representation(self, value):
		return {
			"url": value.file.url,
			"title": value.title,
			"width": value.width,
			"height": value.height,
		}


class BlogPageTag(TaggedItemBase):
	content_object = ParentalKey("BlogSinglePage", related_name="tagged_items", on_delete=models.CASCADE)

class BlogSinglePage(Page):
	template = 'blog/blog_single_page.html'
	# subpage_types = ['blog.BlogSinglePage', 'contact.FormPage'] # appname.ModelName
	# parent_page_types = ['home.HomePage', 'blog.BlogListingPage']

	header_image = models.ForeignKey( "wagtailimages.Image", null=True, blank=False, on_delete=models.SET_NULL, related_name="+")
	main_title = models.CharField(max_length=250, blank=False, editable=True, null=True)
	main_title_color = models.CharField(max_length=7, choices=COLOR_CHOICES, blank=True, null=True)
	subtitle = RichTextField(blank=True, editable=True, null=True, features=['h2','h3','h4','h5','h6','link'])
	subtitle_color = models.CharField(max_length=7, choices=COLOR_CHOICES, blank=True, null=True)

	tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
	categories = ParentalManyToManyField("blog.BlogCategory", blank=True) # You can change this into an Orderable in order to show at the api

	published_date_display = models.DateTimeField(null=True, blank=True)

	content = StreamField(
		[
			("intro_home", IntroSectionBGImageCentederTextBlock()),
			("icon_link", CardWithIconBlock()),
			("divider", DividerBlock()),
			("richtext", RichTextBlock()),
			("accordion", ColapsibleBlock()),
			("pricing_card", PricingCardsBlock()),
			('counter_up', CountersBlock()),
		],
		null=True,
		blank=True,
	)

	search_fields = Page.search_fields + [
		index.FilterField("main_title"),
	]
	content_panels = Page.content_panels + [
		MultiFieldPanel([
			ImageChooserPanel("header_image"),
			FieldPanel("published_date_display"),
			FieldPanel("main_title"),
			FieldPanel("main_title_color"),
			FieldPanel("subtitle"),
			FieldPanel("subtitle_color"),
		], heading='The "Header" section.'),
		MultiFieldPanel([
			FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
			FieldPanel("tags"),
		], heading='Categories & Tags related.'),
		MultiFieldPanel([
			StreamFieldPanel("content"),
		], heading='Content'),
		MultiFieldPanel([
			InlinePanel("blog_authors", label="Author", min_num=0, max_num=5),
		], heading='Author(s)'),
		MultiFieldPanel([
			InlinePanel("customcomments", label="Comment", max_num=1),
		], heading='Fix a Comment'),
	]
	# Cap 45
	sidebar_panels = [
		MultiFieldPanel([
			FieldPanel("main_title")
		], heading="Custom 1")
	]

	# Cap 45
	edit_handler = TabbedInterface([
		ObjectList(content_panels, heading="Content"),
		ObjectList(Page.promote_panels, heading="Promote"),
		ObjectList(Page.settings_panels, heading="Settings"),
	])


	api_fields = [
		APIField("content"),
		APIField("blog_authors"),
	]

	def get_context(self, request, *args, **kwargs):
		context = super().get_context(request, *args, **kwargs)
		context['all_categories'] = BlogCategory.objects.all()
		return context

	# Comments
	def get_absolute_url(self):
		return self.get_url()

	class Meta:
		verbose_name = 'Post Page'
		verbose_name_plural = 'Post Pages'


	def get_sitemap_urls(self, request):
		sitemap = super().get_sitemap_urls(request)
		sitemap.append(
			{
				"location": self.full_url,
				"lastmod": (self.published_date_display or self.last_published_at or self.latest_revision_created_at),
				"priority": 1, # A number between 0-1
			}
		)
		return sitemap


class BlogListingPage(RoutablePageMixin, Page):
	template = 'blog/blog_listing_page.html'
	#ajax_template = "blog/blog_listing_page_ajax.html"
	#max_count = 2
	subpage_types = ['blog.BlogSinglePage', 'contact.FormPage'] # appname.ModelName
	parent_page_types = ['home.HomePage']

	header_image = models.ForeignKey( "wagtailimages.Image", null=True, blank=False, on_delete=models.SET_NULL, related_name="+")
	main_title = models.CharField(max_length=250, blank=False, editable=True, null=True)
	main_title_color = models.CharField(max_length=7, choices=COLOR_CHOICES, blank=True, null=True)
	subtitle = RichTextField(blank=True, editable=True, null=True, features=['h2','h3','h4','h5','h6','link'])
	subtitle_color = models.CharField(max_length=7, choices=COLOR_CHOICES, blank=True, null=True)

	content = StreamField(
		[
			("intro_home", IntroSectionBGImageCentederTextBlock()),
			("icon_link", CardWithIconBlock()),
			("divider", DividerBlock()),
			("richtext", RichTextBlock()),
			("accordion", ColapsibleBlock()),
			("pricing_card", PricingCardsBlock()),
			('counter_up', CountersBlock()),
		],
		null=True,
		blank=True,
	)

	content_panels = Page.content_panels + [
		MultiFieldPanel([
			ImageChooserPanel("header_image"),
			FieldPanel("main_title"),
			FieldPanel("main_title_color"),
			FieldPanel("subtitle"),
			FieldPanel("subtitle_color"),
		], heading='The "Header" section.'),
		MultiFieldPanel([
			StreamFieldPanel("content"),
		], heading='Content'),
	]


	def get_context(self, request, *args, **kwargs):
		context = super().get_context(request, *args, **kwargs)
		# If "posts" have child pages; yoou'll need to use .specific in the template
		# in order to access child properties, such as youtube_video_id and subtitle
		all_posts = BlogSinglePage.objects.live().public().order_by('-first_published_at').distinct()

		if request.GET.get('tag', None):
			tags = request.GET.get('tag')
			all_posts = all_posts.filter(tags__slug__in=[tags])
			
		# Pagination
		paginator = Paginator(all_posts, 1) # Determines how many post show for page
		page = request.GET.get("page") # "page" is a name that you can change if you want ?page={{post.previous_page_number}}
		try:
			posts = paginator.page(page)
		except PageNotAnInteger:
			posts = paginator.page(1)
		except EmptyPage:
			posts = paginator.page(paginator.num_pages)

		context['posts'] = posts # BlogSinglePage.objects.live().public().order_by('-first_published_at')
		context['all_categories'] = BlogCategory.objects.all()
		return context

	class Meta:
		verbose_name = 'Blog Listing Page'
		verbose_name_plural = 'Blog Listing Pages'

	@route(r'^latest/?', name="latest_posts")
	def latest_blog_posts(self, request, *args, **kwargs):
		context = self.get_context(request, *args, **kwargs)
		context['latest_posts'] = context['posts'][:3]
		return render(request, 'blog/latest_posts.html', context)

	@route(r'^subscribe/?$', name="subscribe")
	def the_subscribe_page(self, request, *args, **kwargs):
		context = self.get_context(request, *args, **kwargs)
		#context['reverse_subpage'] = self.reverse_subpage('latest_posts') # Cap 17
		return render(request, 'cms/contact_page.html', context)

	@route(r"^/?(\d+)/$", name="blogs_by_year")
	def blogs_by_year(self, request, year):
		context = self.get_context(request)

		try:
			year = BlogSinglePage.objects.get(first_published_at__year=year)

		except Exception:
			year = None

		if year == None:
			pass

		context['posts'] = BlogSinglePage.objects.filter(first_published_at__in=[year])
		return render(request, 'blog/blog_listing_page.html', context)

	@route(r"^category/(?P<cat_slug>[-\w]*)/$", name="category_view")
	def category_view(self, request, cat_slug):
		# Find blog posts based on a category
		context = self.get_context(request)

		try:
			category = BlogCategory.objects.get(slug=cat_slug)

		except Exception:
			category = None

		if category == None:
			pass

		context['posts'] = BlogSinglePage.objects.filter(categories__in=[category]).distinct()
		return render(request, 'blog/blog_listing_page.html', context)


	def get_sitemap_urls(self, request):
		sitemap = super().get_sitemap_urls(request)
		sitemap.append(
			{
				"location": self.full_url + self.reverse_subpage("latest_posts"),
				"lastmod": (self.last_published_at or self.latest_revision_created_at),
				"priority": 0.9,
			}
		)
		return sitemap

#===============   EXTRAS  ======================#

class BlogAuthorsOrderable(Orderable):
	id = models.AutoField(primary_key=True, default=1)
	page = ParentalKey("blog.BlogSinglePage", related_name="blog_authors")
	author = models.ForeignKey("blog.BlogAuthor", on_delete=models.CASCADE)

	panels = [
		SnippetChooserPanel("author")
	]

	@property
	def author_name(self):
		return self.author.name

	@property
	def author_website(self):
		return self.author.website

	@property
	def original_image(self):
		return self.author.image

	@property
	def author_image(self):
		return self.author.image

	api_fields = [
		APIField("author_name"),
		APIField("author_website"),
		APIField("original_image", serializer=ImageSerializedField()),
		APIField("image", serializer=ImageRenditionField("fill-360x360", source="author_image")),
	]
	
#=====================================
''' Snippets '''
#=====================================
class BlogAuthor(models.Model):
	name = models.CharField(max_length=50, blank=False, null=True, unique=True)
	website = models.URLField(blank=True, null=True)
	image = models.ForeignKey("wagtailimages.Image", on_delete=models.SET_NULL, null=True, blank=False, related_name="+")
	social_networks = StreamField([("social", SocialLinksBlock()),], null=True, blank=True,)

	panels = [
		MultiFieldPanel([
			FieldPanel("name"),
			FieldPanel("website"),
			ImageChooserPanel("image"),
		], heading="Author Data"),
		MultiFieldPanel([
			StreamFieldPanel("social_networks")
		], heading="Social Networks")
	]

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Blog Author'
		verbose_name_plural = "Blogs Authors"


register_snippet(BlogAuthor)


class BlogCategory(models.Model):
	name = models.CharField(max_length=50, blank=False, null=True)
	slug = models.SlugField(verbose_name="slug", allow_unicode=True, max_length=250, unique=True, help_text="A slug to identify posts by this category.")

	panels = [
		FieldPanel("name"),
		FieldPanel("slug"),
	]

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Blog Category"
		verbose_name_plural = "Blogs Categories"
		ordering = ['name']


register_snippet(BlogCategory)

#===============  Comments =============#
class CustomComment(Orderable):
	id = models.AutoField(primary_key=True, default=1)
	page = ParentalKey("BlogSinglePage", on_delete=models.CASCADE, related_name="customcomments")
	author = models.ForeignKey("blog.BlogAuthor", on_delete=models.CASCADE, null=True, blank=False)

	comment = RichTextField(blank=False, null=True, editable=True)
	datetime_commented = models.DateTimeField(blank=True, null=True)

	panels = [
		SnippetChooserPanel("author"),
		FieldPanel("comment"),
	]