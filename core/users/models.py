from django.contrib.auth.models import (AbstractUser, AbstractBaseUser, BaseUserManager, User)
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.db import models
#from core.clienthandle.models import *
# TODO: IMPORT REGULAR-EXPRESSIONS from Python
#from core.store.models import *

GENDER_CHOICE = [
	('m', 'MALE',),
	('f', 'FEMALE'),
	('c', 'CUSTOM'),
]

# phone_regex = RegexValidator(regex=r"^\+(?:[0-9]?){6,14}[0-9]$", message=_("Enter a valid international phone number, please"))
# phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True, editable=True)

class User(AbstractUser):
	avatar_user = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)
	phone = models.CharField(max_length=17, blank=True, null=True, editable=True)
	website = models.CharField(max_length=100, blank=True, null=True, editable=True)

	street = models.CharField(max_length=50, blank=True, null=True)
	suite = models.CharField(max_length=50, blank=True, null=True) # Apartment
	city = models.CharField(max_length=50, blank=True, null=True)
	zipcode = models.CharField(max_length=50, blank=True, null=True)
	country = CountryField(multiple=False, default='United States', blank=True, null=True)
	user_latitude_location = models.CharField(blank=True, null=True, max_length=50, editable=False)
	user_longitude_location = models.CharField(blank=True, null=True, max_length=50, editable=False)
	continent = models.CharField(max_length=15, editable=True, blank=True, null=True)

	gender = models.CharField(max_length=1, choices=GENDER_CHOICE, blank=True, null=True)
	date_of_birth = models.DateField(blank=True, null=True)
	amount_spended = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, editable=False, help_text="Defines how much money this user has spended.")
	
	ocupation = models.CharField(max_length=100, blank=True, null=True, editable=True)
	#company_id = models.ForeignKey(Company, related_name="+", on_delete=models.CASCADE)
	is_a_good_user = models.BooleanField(default=True, help_text="This defines if the user must to be blocked or not. Default is 'True'.")
	hobbies = models.TextField(blank=True, null=True, editable=True, help_text="Separate the hobbies by commas.")
	is_subscribed = models.BooleanField(default=False)
	is_lead = models.BooleanField(default=False)
	is_client = models.BooleanField(default=False)
	is_super_client = models.BooleanField(default=False)
	is_affiliated = models.BooleanField(default=False)
	is_colaborator = models.BooleanField(default=False)
	is_donating = models.BooleanField(default=False)
	is_honest = models.BooleanField(default=False, editable=False)
	email_verified = models.BooleanField(default=False)
	accepted_privacy_terms = models.BooleanField(default=False)
	#pages_visited = models.ForeignKey('AppPages', on_delete=models.SET_NULL)


	def __str__(self):
		return self.username

	def get_image(self):
		if self.avatar_user:
			return f'{MEDIA_URL}{self.avatar_user}'
		return '{}{}'.format(STATIC_URL, 'img/empty.png')

# DEFAULT VALUES FOR USER
# "id		password	 last_login		is_superuser	 username	 first_name 	email 	is_staff 	is_active 	date_joined 	last_name"

# AbstractUser
# "get_full_name, get_short_name, email_user"
# objects = UserManager(), EMAIL_FIELD = 'email', USERNAME_FIELD = 'username', REQUIRED_FIELDS = ['email']

"""
	username = models.CharField(
		_('username'),
		max_length=150,
		unique=True,
		help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
		validators=[username_validator],
		error_messages={
			'unique': _("A user with that username already exists."),
		},
	)
	first_name = models.CharField(_('first name'), max_length=150, blank=True)
	last_name = models.CharField(_('last name'), max_length=150, blank=True)
	email = models.EmailField(_('email address'), blank=True)
	is_staff = models.BooleanField(
		 _('staff status'),
		 default=False,
		 help_text=_('Designates whether the user can log into this admin site.'),
	)
	is_active = models.BooleanField(
		_('active'),
		default=True,
		help_text=_(
			'Designates whether this user should be treated as active. '
			'Unselect this instead of deleting accounts.'
		),
	)
	date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

"""