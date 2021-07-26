import random
import qrcode
from django.db import models
from datetime import date
from django.contrib.auth.models import User
#from io import BytesIO
#from django.core.files import File
#from PIL import Image, ImageDraw

date = date.today()
year = date.today().year



# x = random.randint(100000, 999999E150)   Unusable in this moment


class QRCoder(models.Model):
	name = models.CharField(max_length=200, unique=True, help_text="Give a unique name for each of your QR-Codes")
	subject = models.CharField(max_length=200, help_text="Give a human readable subject for your QR-Code", blank=True, null=True)
	data =  models.CharField(max_length=200, help_text="Give a value for your QR-Code", blank=True, null=True)
	#qr_code_img = models.ImageField(upload_to='QRImgCodes/%Y/%m/%d', blank=True, help_text="This image will be generated automatically, you only need to give a 'name'")
	slug = models.CharField(max_length=200, unique=True)
	save_img_as = models.CharField(max_length=250, unique=True, blank=True, null=True, editable=False)

	def __str__(self):
		return str(self.name)

	def save(self, *args, **kwargs):
		qr = qrcode.QRCode(
			version = 6,  # Controls the size of the QR, it's between 1 - 40
			error_correction = qrcode.constants.ERROR_CORRECT_M, # _L = 7%; _M = 15% (default); _Q = 25%; _H = 30%
			box_size = 5, # Controls the QR dimention size
			border = 1, # (default)
		)

		qr.add_data(f'{self.subject}\n{self.data}')
		qr.make(fit=True) # Fits the dimension
		img = qr.make_image(fill='black', back_color='white')
		self.save_img_as = f'{self.slug}{date}'
		img.save(f'media/QRImgCodes/{self.save_img_as}.jpg')
		#self.qr_code_img.save(data, img)
		super().save(*args, **kwargs)

	class Meta:
		verbose_name = 'QR Code'
		verbose_name_plural = 'QR Codes'

	def get_absolute_url(self):
		return reverse("get-qrcode", kwargs={ "slug":self.slug }) # core = appname; get-qrcode is my url_name, in urls.py




'''
Original Code:

		qrcode_img = qrcode.make(self.name) # Fill the 'qr_code' field passing the name
		canvas = Image.new('RGB', (290, 290), '#fff') # Draw an image
		draw = ImageDraw.Draw(canvas) # Draw an image
		canvas.paste(qrcode_img) # Draw an image
		file_name = f'{img_name}{self.slug}.png' # Create a file => Original: f'qr_code-{self.name}.png'
		buffer = BytesIO()
		canvas.save(buffer,'PNG')
		self.qr_code_img.save(file_name, File(buffer), save=False) # Uploat the img
		canvas.close()
		super().save(*args, **kwargs)


'''

'''
	def slugify(self):
		slugged = str(self.name).replace(' ','-')
		return slugged
'''