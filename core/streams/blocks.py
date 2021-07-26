from django.db import models
from wagtail.core import blocks
from wagtail.core import blocks as natives
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core.models import Page, Orderable, PageManager, PageQuerySet
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from .choices import *

from django.db import models


PUSH_IMAGE_CHOICES = [
	("left","Left"),
	("right","Right"),
]
PUSH_CONTENT_CHOICES = [
	("left","Left"),
	("right","Right"),
	("center","Center"),
]

BG_COLOR_CHICES = [
	("transparent", "Transparent"),
	("danger", "Red"),
	("success", "Green"),
	("info", "Sky Blue"),
	("primary", "Blue"),
	("secondary", "Gray"),
	("dark", "Dark"),
	("white", "White"),
]

LABEL_COLOR_CHOICES = [
	("#000", "Black"),
	("steelblue", "Steel Blue"),
	("blue", "Blue"),
	("deeppink", "Deep Pink"),
	("green", "Green"),
	("deeppurple", "Purple"),
	("red", "Red"),
]

#====================  Home Page =========================
#============  CARDS ============#
class CardWithIconBlock(blocks.StructBlock):	# DONE
	section_title = blocks.CharBlock(max_length=250, required=False, help_text="Add a Title")
	section_subtitle =  blocks.TextBlock(required=False, help_text="Add a Title")
	
	cards = blocks.ListBlock(
			blocks.StructBlock([
				("main_color", blocks.CharBlock(required=False, max_length=50, default="#000", help_text="Hexagesimal or Web colors only.")),
				("icon", blocks.CharBlock(required=False, max_length=50)),
				("card_title", blocks.CharBlock(max_length=250, required=False, editable=True)),
				("card_text", blocks.TextBlock(required=False, max_length=250)),
				("internal_page_url", blocks.PageChooserBlock(required=False, help_text="Internal Page Link")),
				("url", blocks.URLBlock(required=False)),
				("open_in_a_new_tab", blocks.BooleanBlock(default=False, help_text='Default is "False"', required=False)),
				("rel_attribute", blocks.TextBlock(required=False, max_length=250)),
			]),
		)
				
	class Meta:
		template = "streams/homepage/FIXED/card_with_icon_block.html"
		icon = 'fa-clone'
		label = "Card with Icon"
		group = "Cards"


class PricingCardsBlock(blocks.StructBlock):	# DONE
	section_title = blocks.CharBlock(max_length=250, required=False)
	section_subtitle =  blocks.TextBlock(required=False)

	cards = blocks.ListBlock(
			blocks.StructBlock([
				("card_active", blocks.BooleanBlock(required=False, default=False)),
				("outline_color", blocks.CharBlock(required=False, max_length=50, default="#000", help_text="Hexagesimal or Web colors only.")),
				("label", blocks.CharBlock(max_length=250, required=False, editable=True)),
				("label_color", blocks.CharBlock(required=False, max_length=50, default="transparent", help_text="Hexagesimal or Web colors only.")),
				("card_title", blocks.CharBlock(max_length=250, required=False, editable=True)),
				("amount", blocks.DecimalBlock(default=1, min_value=0, decimal_places=2, required=True, editable=True)),
				#("amount_color", blocks.CharBlock(required=False, max_length=50, default="#000", help_text="Hexagesimal or Web colors only.")),
				("amount_for", blocks.CharBlock(max_length=250, required=False, editable=True)),
				("content_text", blocks.RichTextBlock(required=False, features=[
					'h2', 'h3', 'h4', 'h5','h6', 'bold', 'italic', 'link', 'ol', 'ul', 'hr',
					'code', 'superscript', 'subscript', 'strikethrough', 'blockquote'
				])),
				("call_to_action", blocks.CharBlock(max_length=50, required=False, editable=True)),
				("internal_page_url", blocks.PageChooserBlock(required=False, help_text="Internal Page Link")),
				("url", blocks.URLBlock(required=False)),
				("open_in_a_new_tab", blocks.BooleanBlock(default=False, help_text='Default is "False"', required=False)),
				("rel_attribute", blocks.TextBlock(required=False, max_length=250)),
			]),
		)
				
	class Meta:
		template = "streams/homepage/FIXED/pricing_cards_block.html"
		icon = 'fa-money'
		label = "Pricing Cards"
		group = "Cards"


class ColapsibleBlock(blocks.StructBlock):	# DONE
	section_title = blocks.CharBlock(max_length=250, required=False)
	section_subtitle =  blocks.TextBlock(required=False)
	
	container = blocks.ListBlock(
			blocks.StructBlock([
				("question", blocks.TextBlock(required=True)),
				("answerd", blocks.RichTextBlock(required=True, features=[
					'h3', 'h4', 'h5','h6', 'center', 'left', 'bold', 'italic', 'link', 'ol', 'ul', 'hr',
					'document-link', 'image', 'embed', 'code', 'superscript', 'subscript', 'strikethrough', 'blockquote'])),
			]),
		)
			
	class Meta:
		template = "streams/homepage/FIXED/accordeon_block.html"
		icon = "plus-inverse"
		label = "Accordeon Area"
		group = "Extras"


class SummaryBlock(blocks.StructBlock):	# DONE
	section_title = blocks.CharBlock(max_length=250, required=False)
	section_subtitle =  blocks.TextBlock(required=False)

	container = blocks.ListBlock(
			blocks.StructBlock([
				("summary", blocks.TextBlock(required=True)),
				("content", blocks.RichTextBlock(required=True, features=[
					'h3', 'h4', 'h5','h6', 'center', 'left', 'bold', 'italic', 'link', 'ol', 'ul', 'hr',
					'document-link', 'image', 'embed', 'code', 'superscript', 'subscript', 'strikethrough', 'blockquote'])),
			]),
		)
			
	class Meta:
		template = "streams/homepage/FIXED/summary_block.html"
		icon = "arrow-right"
		label = "Summary"
		group = "Extras"


class CustomHTML(blocks.StructBlock): 	# DONE
	html_content = blocks.TextBlock(required=True, help_text="Anjoy writing your code here.")
			
	class Meta:
		template = "streams/homepage/FIXED/custom_html_block.html"
		icon = "code"
		label = "Custom HTML"
		group = "Extras"


class CountersBlock(blocks.StructBlock):	# DONE
	background_image = ImageChooserBlock(required=False)

	counters = blocks.ListBlock(
		blocks.StructBlock(
			[
				("icon", blocks.CharBlock(max_length=50, required=True)),
				("header_color", blocks.CharBlock(required=False, max_length=50, default="#000", help_text="Hexagesimal or Web colors only.")),
				("number", blocks.IntegerBlock(required=True)),
				("comment", blocks.CharBlock(max_length=100, required=True)),
			]
		)
	)
	
	class Meta:
		template = "streams/homepage/FIXED/counters_up_block.html"
		icon = "fa-dot-circle-o"
		label = "Progress Numeral Card"
		group = "Progress"


class InfoBlock(blocks.StructBlock):	# Done
	section_title = blocks.CharBlock(max_length=250, required=False, help_text="Add a Title")
	section_subtitle =  blocks.TextBlock(required=False, help_text="Add a Title")
	
	image = ImageChooserBlock(required=False, help_text="Size: 'min width' = 200px")
	content_title = blocks.CharBlock(max_length=250, required=False, help_text="Add a Title")
	content = blocks.RichTextBlock(required=False, editable=True, features=['h2', 'h3', 'h4', 'h5','h6', 'bold', 'italic', 'link', 'ol', 'ul', 'hr','document-link', 'code', 'superscript', 'subscript', 'strikethrough', 'blockquote'])

	class Meta:
		template = "streams/homepage/FIXED/img_info_section_block.html"
		icon = 'fa-list'
		label = "Section type A"
		group = "Sections"


class IntroSectionBGImageCentederTextBlock(blocks.StructBlock):	# DONE

	background_image = ImageChooserBlock(required=False)
	#background_image_style = blocks.ChoiceBlock(max_length=4, required=False, choices=[("full", "Full Screen"),("mdle", "Truncated"),], help_text="Select how the header image will be shown.")
	title = blocks.CharBlock(max_length=250, required=False, editable=True)
	title_color = blocks.CharBlock(required=False, max_length=50, default="#000", help_text="Hexagesimal or Web colors only.")
	typed_subtitle = blocks.TextBlock(required=False, editable=True, help_text="Separating by commas couse the typed effect.")
	subtitle_color =  blocks.CharBlock(required=False, max_length=50, default="#000", help_text="Hexagesimal or Web colors only.")

	button_url = blocks.ListBlock(
		blocks.StructBlock(
			[
				("background_color", blocks.CharBlock(required=False, max_length=50, default="#000", help_text="Hexagesimal or Web colors only.")),
				("outline_color_only", blocks.BooleanBlock(default=True, help_text='Default is "True"', required=False)),
				("call_to_action", blocks.CharBlock(max_length=100, required=False)),
				("text_color", blocks.CharBlock(required=False, max_length=50, default="#000", help_text="Hexagesimal or Web colors only.")),
				("URL", blocks.URLBlock(required=False, max_length=500, min_leght=6)),
				("open_in_a_new_tab", blocks.BooleanBlock(default=True, help_text='Default is "True"', required=False)),
				("rel_attribute", blocks.TextBlock(max_length=250, required=False)),
			]
		)
	) 

	class Meta:
		template = "streams/homepage/FIXED/section_type_b_block.html"
		icon = 'fa-list'
		label = "Section type B (Typed Subtitle)"
		group = "Sections"

class DividerBlock(blocks.StructBlock):	# DONE
	height_in_px = blocks.IntegerBlock(default=15)
	opacity = blocks.DecimalBlock(default=1, min_value=0, max_value=1, decimal_places=2, help_text="Only acepts a number between 0-1")
	background_color = blocks.CharBlock(required=False, max_length=50, default="transparent", help_text="Hexagesimal or Web colors only.")

	class Meta:
		template = "streams/homepage/divider_block.html"
		icon = 'horizontalrule'
		label = "Horizontal Divider"
		group = "Extras"

class JumbotronBlock(blocks.StructBlock):	# DONE
	title = blocks.RichTextBlock(required=False, editable=True, features=['h2', 'h3', 'h4', 'h5','h6', 'bold'])
	content = blocks.RichTextBlock(required=False, editable=True, features=['h3', 'h4', 'h5','h6', 'bold', 'italic', 'link', 'ol', 'ul', 'hr','image','document-link', 'code', 'superscript', 'subscript', 'strikethrough', 'blockquote'])

	class Meta:
		template = "streams/homepage/jumbotron_block.html"
		icon = 'pilcrow'
		label = "Floating Content"
		group = "Extras"

class ContactMapBlock(blocks.StructBlock):
	section_title = blocks.TextBlock(max_length=100, required=False)
	phone_number = blocks.TextBlock(max_length=100, required=False)
	phone_number_comment = blocks.TextBlock(max_length=100, required=False, help_text='Add a comment for "Phone Number Column".')
	email_address = blocks.TextBlock(max_length=100, required=False)
	email_address_comment = blocks.TextBlock(help_text='Add a comment for "Email Address Column".', max_length=100, required=False)
	location_street = blocks.TextBlock(max_length=100, required=False)
	location_city = blocks.TextBlock(help_text="City, ZIP, Country", max_length=100, required=False)
	google_map_iframe = blocks.TextBlock(max_length=1000, required=False)

	class Meta:
		template = "streams/homepage/FIXED/contact_map_block.html"
		icon = 'fa-map-marker-alt'
		label = "Contact with Map Embeded"
		group = "Contact Sections"
#######################################################################
#				DELETE
#######################################################################
class SocialLinksBlock(blocks.StructBlock):	# DELETE
	social_net_icon = blocks.ChoiceBlock(required=True, choices=SOCIALLINKS_CHOICES, help_text="Select a Social NetWork.")
	url = blocks.URLBlock(required=True, max_length=500, min_leght=6)

	class Meta:
		template = "streams/social_links_block.html"
		icon = "fa-spinner"
		label = "Social NetWorks"



class CustomTableBlock(TableBlock):	# TRY TO FIX THIS SHIT
	table = TableBlock()

	class Meta:
		icon = "fa-table"
		label = "Table"
		group = "Extras"

class RichTextBlock(blocks.RichTextBlock):	# DELETE
	content = blocks.RichTextBlock(required=True, editable=True)

	class Meta:
		template = "streams/homepage/FIXED/rich_text.html"
		icon = 'fa-paragraph'
		label = "Rich Content"
		group = "Texts"
'''

	'h2', 'h3', 'h4', 'h5','h6', 'center', 'right', 'left', 'bold', 'italic', 'link', 'ol', 'ul', 'hr',
	'document-link', 'image', 'embed', 'code', 'superscript', 'subscript', 'strikethrough', 'blockquote'
'''