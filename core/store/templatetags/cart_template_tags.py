from django.utils.safestring import SafeString
from django import template
from django.template.defaultfilters import stringfilter
from core.store.models import Order

register = template.Library()

@register.filter
def cart_item_count(user):

	if user.is_authenticated:
		qs = Order.objects.filter(user=user, ordered=False)

		if qs.exists():
			return qs[0].items.count()

	return 0

@register.filter(name='replace', is_safe=True)
@stringfilter
def replace(value, arg):
	return value.replace(arg,' ')

'''

@stringfilter -> Va a convertia a String antes de ser pasado a la funcion

@register.simple_tag() -> This function takes a function that accepts any number of arguments

@register.inclusion_tag('my_template.html', takes_context=True)  -> displays some data by rendering another template

'''