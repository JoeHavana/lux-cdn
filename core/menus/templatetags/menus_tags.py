from django import template
from ..models import *

register = template.Library()

@register.simple_tag()
def get_menu(slug):
	return Menu.objects.get(slug=slug)

@register.simple_tag()
def menu_type(menu_type):
	menus = Menu.objects.filter(menu_type=menu_type).distinct()
	return menus.all

@register.simple_tag()
def single_menu(menu_type):
	menus = SingleMenuItem.objects.filter(menu_type=menu_type).distinct()
	return menus.all