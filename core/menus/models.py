from django.db import models
from django_extensions.db.fields import AutoSlugField
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.http import JsonResponse
from django_comments_xtd.models import XtdComment

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable, PageManager, PageQuerySet
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import *
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, PageChooserPanel, StreamFieldPanel,)
from wagtail.admin.forms import WagtailAdminModelForm, WagtailAdminPageForm
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.search import index

from ckeditor import fields as ckedit

from core.streams.blocks import *
from core.streams.choices import *
from home.models import *


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

	
@register_snippet
class Menu(ClusterableModel):
	""" DropDown Menu Class """
	title = models.CharField(max_length=50, editable=True, unique=True)
	slug = AutoSlugField(populate_from="title", editable=True, unique=True)
	menu_type = models.CharField(max_length=3, default="pgs", blank=True, null=True)

	panels = [
		MultiFieldPanel([
			FieldPanel("title"),
		], heading="Dropdown Menu"),
		InlinePanel("menu_items", min_num=1, label="Links")
	]

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = "Menu with Dropdown for Top Navigation"
		verbose_name_plural = "Menus with Dropdown for Top Navigation"


@register_snippet
class SingleMenuItem(Orderable):
	title = models.CharField(blank=False, null=True, max_length=50)
	menu_type = models.CharField(max_length=3, default="sng", blank=True, null=True)
	open_in_new_tab = models.BooleanField(default=False, help_text='Default is "False"')
	rel_attribute = models.CharField(max_length=250, blank=True, null=True)
	link_url = models.URLField(max_length=500, blank=True, null=True)
	link_page = models.ForeignKey("wagtailcore.Page", null=True, blank=True, related_name="+", on_delete=models.CASCADE)

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
		verbose_name = "Single Menu for Top Navigation"
		verbose_name_plural = "Single Menus for Top Navigation"