from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.images.edit_handlers import ImageChooserPanel
from core.streams.choices import *


@register_setting
class FromGoogle(BaseSetting):
    gmail_user_account = models.TextField(unique=True, blank=True, null=True, editable=True, help_text="Your email probided by Goggle")
    gmail_password = models.TextField(unique=True, blank=True, null=True, editable=True, help_text="G-mail account password")
    google_analytics = models.TextField(unique=True, blank=True, null=True, editable=True, help_text="Copy and Paste here the scripts provided by Google Analytics.")
    google_adsense = models.TextField(unique=True, blank=True, null=True, editable=True, help_text="Copy and Paste here the scripts provided by Google Ads.")
    google_maps = models.TextField(unique=True, blank=True, null=True, editable=True, help_text="Copy and Paste here the scripts provided by Google Maps.")
    
    panels = [
        FieldPanel("gmail_user_account"),
        FieldPanel("gmail_password"),
        FieldPanel("google_analytics"),
        FieldPanel("google_adsense"),
        FieldPanel("google_maps"),
    ]

    class Meta:
        verbose_name = 'From Google'


@register_setting
class Brand(BaseSetting):
    favicon_image = models.ForeignKey("wagtailimages.Image", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    brand_image_logo = models.ForeignKey("wagtailimages.Image", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    brand_name = models.CharField(max_length=50, blank=True, null=True, unique=True, editable=True, help_text='If "Brand image logo" was selected, do not select this.')
    show_logo_image = models.BooleanField(default=False, blank=True, null=True)
    show_brand_name = models.BooleanField(default=True, blank=True, null=True)
    public_email = models.EmailField(blank=True, null=True, help_text="This email will be used for comuniction with users.")

    panels = [
        MultiFieldPanel([
            ImageChooserPanel("favicon_image"),
            ImageChooserPanel("brand_image_logo"),
            FieldPanel("brand_name"),
            FieldPanel("show_logo_image"),
            FieldPanel("show_brand_name"),
            FieldPanel("public_email"),
        ], heading="Brand Data"),
    ]


'''
    """ Borra esta mierda """
class LoginStyles(BaseSetting):
    background_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, related_name="+", on_delete=models.CASCADE)
    allow_particles_effect = models.BooleanField(default=True, blank=True, null=True)
    background_card = models.CharField(blank=True, null=True, default="#000000", choices=COLOR_CHOICES, max_length=7)
    text_color = models.CharField(blank=True, null=True, default="#ffffff", choices=COLOR_CHOICES, max_length=7)

    panels = [
        ImageChooserPanel("background_image"),
        FieldPanel("allow_particles_effect"),
        FieldPanel("background_card"),
        FieldPanel("text_color"),
    ]
'''