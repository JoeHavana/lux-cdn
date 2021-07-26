from django.db import models
from wagtail.core.models import Orderable
from wagtail.core.fields import RichTextField
from modelcluster.fields import ParentalKey 
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, PageChooserPanel, StreamFieldPanel,)
from wagtail.snippets.models import register_snippet
from modelcluster.models import ClusterableModel
from django_extensions.db.fields import AutoSlugField


class SocialLinks(Orderable):
	""" The Social Icons, for the class BrandInfo """
	social_icon_code = models.CharField(blank=False, null=True, max_length=30)
	link_url = models.URLField(max_length=500, blank=True, null=True)
	rel_attribute = models.CharField(max_length=250, blank=True, null=True)

	page = ParentalKey("BrandInfo", related_name="social_items", null=True)

	panels = [
		FieldPanel("social_icon_code"),
		FieldPanel("link_url"),
		FieldPanel("rel_attribute"),
	]

class ColumnLinkItem(Orderable):
	""" The Links, for the class FooterColumns """
	link_title = models.CharField(blank=False, null=True, max_length=50)
	link_icon_code = models.CharField(blank=True, null=True, max_length=50)
	link_title_color_code = models.CharField(blank=True, null=True, max_length=50)
	link_url = models.URLField(max_length=500, blank=True, null=True)
	#link_page = models.ForeignKey("wagtailcore.Page", null=True, blank=True, related_name="+", on_delete=models.CASCADE)
	#open_in_new_tab = models.BooleanField(default=False, help_text='Default is "False"')
	rel_attribute = models.CharField(max_length=250, blank=True, null=True)
	page = ParentalKey("FooterColumns", related_name="column_items", null=True)

	panels = [
		FieldPanel("link_title"),
		FieldPanel("link_icon_code"),
		FieldPanel("link_color_code"),
		FieldPanel("link_url"),
		PageChooserPanel("link_page"),
		FieldPanel("open_in_new_tab"),
		FieldPanel("rel_attribute"),
	]


@register_snippet
class BrandInfo(ClusterableModel):
	""" In the Footer, the Brand Info """
	text_intro = RichTextField(blank=True, null=True, features=['link'])
	company_direction = models.TextField(blank=True, null=True,)
	company_phone = models.CharField(max_length=50, blank=True, null=True,)
	company_email = models.EmailField(max_length=50, blank=True, null=True,)

	panels = [
		MultiFieldPanel([
			FieldPanel("text_intro"),
			FieldPanel("company_direction"),
			FieldPanel("company_phone"),
			FieldPanel("company_email"),
			InlinePanel("social_items", label="Social Icon"),
		], heading="Brand Information"),
	]

	class Meta:
		ordering = ['-id']
		verbose_name = "Brand Information in the Footer"
		verbose_name_plural = "Brand Information in the Footer"


@register_snippet
class FooterColumns(ClusterableModel):
	""" Each Column of the Footer """
	title = models.CharField(max_length=50, editable=True, unique=True)
	title_color_code = models.CharField(max_length=50, blank=True, null=True)
	slug = AutoSlugField(populate_from="title", editable=True, unique=True)
	menu_type = models.CharField(max_length=3, default="pgs", blank=True, null=True)

	panels = [
		MultiFieldPanel([
			FieldPanel("title"),
			FieldPanel("title_color"),
		], heading="Column"),
		InlinePanel("column_items", min_num=1, label="Links"),
	]

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = "Column of the Footer"
		verbose_name_plural = "Columns of the Footer"
