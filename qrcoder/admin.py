from django.contrib import admin
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from .models import *


class QRCoderAdmin(ModelAdmin):

    model = QRCoder
    menu_label = "QRCode Generator"
    menu_icon = "fa-qrcode"
    menu_order = 301
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "subject", "data")
    list_display_links = ("name", "subject", "data")
    search_fields = ("name", "subject", "data")
    list_filter = ("name", "subject", "data")
    empty_value_display = '------'
    list_select_related = True
    list_per_page = 20
    prepopulated_fields = {'slug' : ('name',)}
    exclude = ('save_img_as',)

modeladmin_register(QRCoderAdmin)
admin.site.register(QRCoder)