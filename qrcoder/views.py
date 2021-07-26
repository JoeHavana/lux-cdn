from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from qrcoder.models import *
from datetime import date


@login_required
def qr_view_all(request):
	try:
		user_qr_codes = QRCoder.objects.all()
		context = {
			'all_qrcodes':user_qr_codes,
			#'route':user_qr_codes.save_img_as,
			'image_tag_1':f'<img alt="QR Code image" src="../../../media/QRImgCodes/',
			'image_tag_2':f'.jpg"/>',
			'download_1':f'<a class="btn" download href="../../../media/QRImgCodes/',
			'download_2':f'.jpg">',
			'year':date.today().year,

		}
		return render(request, 'qrcoder/data.html', context)
	except:
		context = {
			'error':"user_qr_codes doesn't match ",
			'year':date.today().year,
		}
		return render(request, 'qrcoder/data.html', context)
