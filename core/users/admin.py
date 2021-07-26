from django.contrib import admin
from wagtail.contrib.modeladmin.options import ( ModelAdmin, ModelAdminGroup, modeladmin_register, )
from django.contrib.auth.admin import UserAdmin
#from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from core.users.models import User

@admin.register(User)
class DjangoUserAdmin(admin.ModelAdmin):
	pass

class WagtailUserAdmin(ModelAdmin): # UserAdmin class
	model = User
	menu_label = "Users XTD"
	menu_icon = "fa-user"
	menu_order = 189
	list_per_page = 100
	add_to_settings_menu = False
	exclude_from_explorer = False
	list_display = ['username', 'email', 'first_name', 'last_login']
	list_display_links = [ 'email', 'username', 'first_name', 'last_login', 'username','first_name','last_name','city','country','continent','gender','ocupation','hobbies']
	search_fields = ['email', 'username', 'first_name', 'last_name', 'last_login']
	list_filter = ['country','continent','is_a_good_user', 'is_subscribed', 'gender', 'is_subscribed','is_lead','is_client','is_super_client','is_affiliated','is_colaborator','is_donating','email_verified']
	empty_value_display = '------'
	list_select_related = True
	list_export = (
		'id',
		'last_login',
		'is_superuser',
		'username',
		'first_name',
		'email',
		'is_staff',
		'is_active',
		'date_joined',
		'last_name',
		'date_of_birth',
		'city',
		'country',
		'user_latitude_location',
		'user_longitude_location',
		'continent',
		'user_address',
		'is_a_good_user',
		'amount_spended',
		'gender',
		'ocupation',
		'hobbies',
		'is_subscribed',
		'is_lead',
		'is_client',
		'is_super_client',
		'is_affiliated',
		'is_colaborator',
		'is_donating',
		'is_honest',
		'email_verified',
		'accepted_privacy_terms',
    )


modeladmin_register(WagtailUserAdmin)
'''
	add_form = UserCreationForm
	form = UserChangeForm
	
	add_fieldsets = UserAdmin.add_fieldsets + (
		(None, {'fields':('email', 'username', 'password')})
	)
	fieldsets = UserAdmin.fieldsets
'''
# DEFAULT VALUES FOR USER
# "id		password	 last_login		is_superuser	 username	 first_name 	email 	is_staff 	is_active 	date_joined 	last_name"
