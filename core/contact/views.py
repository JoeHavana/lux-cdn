from django.shortcuts import render, redirect, HttpResponse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import HttpResponseRedirect, JsonResponse
from core.site_settings.models import Brand


def contact_thank(request):
	return render(request, 'contact/contact_page_thank.html')
	
def contact_failed(request):
	return render(request, 'contact/contact_page_failed.html')

def user_messages(request):

	if request.method == 'POST':
		username = request.POST['name']
		usermail = request.POST['email']
		subject = request.POST['subject']
		message = request.POST['message']
		full_msg = f'Username: {username}\nMessage:\n{message}'
		if subject and message and usermail:
			try:
				publicmail = Brand.objects.first()
				send_mail(subject=subject, from_email=usermail, recipient_list=[publicmail.public_email], message=full_msg, fail_silently=False)
			except:
				return  HttpResponseRedirect('/contact/failed/')
			return HttpResponseRedirect('/contact/thanks/')
		else:
			return HttpResponse('Make sure all fields are entered and valid.')

	else:
		return HttpResponseRedirect('/contact/failed/')
