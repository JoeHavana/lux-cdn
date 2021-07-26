from django.contrib import admin
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from .models import *
from core.store.models import (
	UserProfile, 
	ItemImages, 
	ItemCategory,
	ItemTag,
	Item,
	Address,
	Payment,
	Coupon,
	Refund,
	OrderItem,
	Order,

)

# Next could be declarated at the URLs
admin.site.index_title=f'Coastline Games Administrator'
admin.site.site_header=f'Control Panel'
admin.site.site_title=f'Administrator'


def make_refund_accepted(modeladmin, request, queryset):
	queryset.update(refund_requested=False, refund_granted=True)

make_refund_accepted.short_description = 'Update orders to refund granted'

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug' : ('title',)}
	#exclude = ('slug', 'updated_at',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_per_page = 20
	list_display = [
		'user', 
		'ordered', 
		'being_delivered', 
		'received', 
		'refund_requested', 
		'refund_granted',
		'billing_address',
		'shipping_address', 
		'payment', 
		'coupon'
	]
	list_display_links = [
        'user',
		'billing_address',
		'shipping_address',  
		'payment', 
		'coupon',
	]
	list_filter = [
		'user', 'ordered', 
		'being_delivered', 
		'received', 
		'refund_requested', 
		'refund_granted'
	]
	search_fields = [
		'user__username', 
		'ref_code'
	]
	actions = [make_refund_accepted]

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
	list_per_page = 20
	list_display = [
		'user',
		'street_address',
		'city_address',
		'country',
		'zipfield',
		'address_type',
		'default',
	]
	list_filter = [
		'address_type',
		'default',
		'country',
	]
	search_fields = [
		'user',
		'street_address',
		'city_address',
		'zipfield',
	]

######## Wagtail Admin #####
class ItemCategoryAdmin(ModelAdmin):

    model = ItemCategory
    menu_label = "Item Categories"
    menu_icon = "fa-list"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("category_name", "priority", "will_be_recomended")
    search_fields = ("category_name", "priority", "will_be_recomended")
    list_filter = ("category_name", "priority", "will_be_recomended")
    empty_value_display = '------'
    list_select_related = True
    list_per_page = 50
    prepopulated_fields = {'slug' : ('category_name',)}


class ItemTagAdmin(ModelAdmin):

    model = ItemTag
    menu_label = "Item Tags"
    menu_icon = "fa-list"
    menu_order = 295
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("tag_name", "active")
    search_fields = ("tag_name", "active")
    list_filter = ("tag_name", "active")
    empty_value_display = '------'
    list_select_related = True
    list_per_page = 50
    prepopulated_fields = {'slug' : ('tag_name',)}


class ItemAdmin(ModelAdmin):
    """Item admin."""

    model = Item
    menu_label = "Items"
    menu_icon = "pick"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_export = ("title", "real_price","real_rating_by_users","rated_by","real_rate_average")
    list_display = ("title", "real_price", "previos_price")
    search_fields = ("is_available", "real_price", "previos_price")
    list_filter = ("is_available", "real_price", "previos_price","real_rating_by_users","rated_by","real_rate_average")
    empty_value_display = '------'
    list_select_related = True
    list_per_page = 50
    prepopulated_fields = {'slug' : ('title',)}


class CouponAdmin(ModelAdmin):
    """Item admin."""

    model = Coupon
    menu_label = "Discount Coupons"
    menu_icon = "fa-file"
    menu_order = 305
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("code", "amount", "percent", "type_of_discount", "last_date_of_the_coupon_live", "disable")
    search_fields = ("code", "amount", "percent", "type_of_discount", "last_date_of_the_coupon_live", "disable")
    list_filter = ("code", "amount", "percent", "type_of_discount", "last_date_of_the_coupon_live", "disable")
    empty_value_display = '------'
    list_select_related = True
    list_per_page = 50


class StoreGroup(ModelAdminGroup):
    menu_label = "Store"
    menu_icon = "fa-money"
    menu_order = 110
    items = (ItemCategoryAdmin, ItemAdmin, CouponAdmin)


modeladmin_register(StoreGroup)