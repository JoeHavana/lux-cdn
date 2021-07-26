from django.contrib import admin
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from .models import *


######## Wagtail Admin #####
class NewsletterUserAdmin(ModelAdmin):
    model = NewsletterUser
    menu_label = "Subscribers"
    menu_icon = "fa-users"
    menu_order = 292
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "email", "email_verified", "date_added",)
    search_fields = ("name", "email", "email_verified", "date_added",)
    list_filter = ("date_added", "email_verified")
    empty_value_display = '------'
    list_select_related = True
    list_per_page = 50
    list_export = ("name", "email", "email_verified", "date_added",)
    #prepopulated_fields = {'slug' : ('category_name',)}


class NewsletterAdmin(ModelAdmin):
    model = Newsletter
    menu_label = "Newsletter Creator"
    menu_icon = "fa-file"
    menu_order = 293
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("subject", "status",)
    list_filter = ("status",)
    empty_value_display = '------'
    list_select_related = True
    list_per_page = 50


class NewsletterGroup(ModelAdminGroup):
    menu_label = "Newsletter App"
    menu_icon = "fa-envelope"
    menu_order = 111
    items = (NewsletterUserAdmin, NewsletterAdmin)

modeladmin_register(NewsletterGroup)
