from django import forms
from crispy_forms.helper import FormHelper
from .models import *


class NewsletterUserSignUpForm(forms.ModelForm):
	helper = FormHelper()
	helper.form_show_labels = False

	class Meta:
		model = NewsletterUser
		fields = ['name', 'email']	# 'name'

		def clean_email(self):
			email = self.cleaned_data.get('email')

			return email


class NewsletterCreationForm(forms.ModelForm):

	class Meta:
		model = Newsletter
		fields = ['subject', 'body', 'action']