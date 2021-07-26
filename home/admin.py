from django.contrib import admin
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from .models import *

# Next could be declarated at the URLs
admin.site.index_title=f'Coastline Games Administrator'
admin.site.site_header=f'Control Panel'
admin.site.site_title=f'Administrator'


'''
class InlineSectionCardsAdmin(ModelAdmin):

    model = InlineSectionCards
    menu_label = "Inline Cards of Items"
    menu_icon = "fa-clone"
    menu_order = 299
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("section_ID", "section_title")
    search_fields = ("section_ID", "section_title")
    list_filter = ("section_ID", "section_title")
    empty_value_display = '------'
    list_select_related = True
    list_per_page = 50


modeladmin_register(InlineSectionCardsAdmin)

admin.site.register(InlineSectionCards)

    list_display_add_buttons = None
    list_export = ()
    inspect_view_fields = []
    inspect_view_fields_exclude = []
    inspect_view_enabled = False
    ordering = None
    parent = None
    index_view_class = IndexView
    create_view_class = CreateView
    edit_view_class = EditView
    inspect_view_class = InspectView
    delete_view_class = DeleteView
    choose_parent_view_class = ChooseParentView
    index_template_name = ''
    create_template_name = ''
    edit_template_name = ''
    inspect_template_name = ''
    delete_template_name = ''
    choose_parent_template_name = ''
    search_handler_class = DjangoORMSearchHandler
    extra_search_kwargs = {}
    permission_helper_class = None
    url_helper_class = None
    button_helper_class = None
    index_view_extra_css = []
    index_view_extra_js = []
    inspect_view_extra_css = []
    inspect_view_extra_js = []
    form_view_extra_css = []
    form_view_extra_js = []
    form_fields_exclude = []



class StoreNativeAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = []
    list_display_links = []
    list_filter = []
    search_fields = []

'''