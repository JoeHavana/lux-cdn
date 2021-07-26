from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_CHOICES = [
	('S', 'Stripe'), # 'value', 'name'
	('P', 'PayPal'),
]


class CheckoutForm(forms.Form):
	shipping_address = forms.CharField(required=False)
	shipping_address2 = forms.CharField(required=False)
	shipping_country = CountryField(blank_label='(select country)').formfield(
		required=False,
		widget=CountrySelectWidget(attrs={
			'class': 'custom-select d-block w-100',
		}))
	shipping_zip = forms.CharField(required=False)

	billing_address = forms.CharField(required=False)
	billing_address2 = forms.CharField(required=False)
	billing_country = CountryField(blank_label='(select country)').formfield(
		required=False,
		widget=CountrySelectWidget(attrs={
			'class': 'custom-select d-block w-100',
		}))
	billing_zip = forms.CharField(required=False)

	same_billing_address = forms.BooleanField(required=False)
	set_default_shipping = forms.BooleanField(required=False)
	use_default_shipping = forms.BooleanField(required=False)
	set_default_billing = forms.BooleanField(required=False)
	use_default_billing = forms.BooleanField(required=False)

	payment_options = forms.ChoiceField(widget=forms.RadioSelect(attrs={
			'name':'payment_options',
		}), choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
	code = forms.CharField(widget=forms.TextInput(attrs={
		'class':'form-control',
		'placeholder':'Promo Code',
		'aria-label':"Recipient\'s username",
		'aria-describedby':"basic-addon2"
	}))
	

class RefundForm(forms.Form):
	ref_code = forms.CharField(widget=forms.TextInput(attrs={
	 	'class':'form-control mb-3',
		}))
	message = forms.CharField(widget=forms.Textarea(attrs={
	 	'class':'form-control mt-0 mb-3',
	 	'rows':7
		}))
	email = forms.EmailField(widget=forms.TextInput(attrs={
	 	'class':'form-control mt-0',
		}))


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)