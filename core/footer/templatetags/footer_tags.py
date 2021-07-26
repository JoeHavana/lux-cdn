from django import template
from ..models import *

register = template.Library()

@register.simple_tag()
def get_footer_column(slug):
	return FooterColumns.objects.get(slug=slug)

@register.simple_tag()
def menu_type(menu_type):
	menus = FooterColumns.objects.filter(menu_type=menu_type).distinct()
	return menus.all

@register.simple_tag()
def brand_info(menu_type): # Brand Info
	brandinfo = BrandInfo.objects.first()
	return brandinfo