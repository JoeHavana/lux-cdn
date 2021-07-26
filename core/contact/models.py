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

# Create your models here.
class FormField(AbstractFormField):
	page = ParentalKey("FormPage", on_delete=models.CASCADE, related_name="form_fields")


class FormPage(AbstractEmailForm):
	template = "contact/contact_page.html"
	landing_page_template = "contact/contact_page_landing.html"

	intro = RichTextField(blank=True)
	Thank_you_text = RichTextField(blank=True)

	content_panels = AbstractEmailForm.content_panels + [
		FieldPanel("intro"),
		InlinePanel("form_fields", label="Form Fields"),
		FieldPanel("Thank_you_text"),
		MultiFieldPanel([
			FieldRowPanel([
				FieldPanel("from_address", classname="col6"),
				FieldPanel("to_address", classname="col6"),
			]),
		FieldPanel("subject")
		], heading="Email Settings")
	]