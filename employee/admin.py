from __future__ import unicode_literals
import re

from django import forms
from django.db import transaction
from django.contrib import admin
from django.conf import settings

# from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.core import validators
from django.utils.http import urlquote
from django.contrib import messages


from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.html import escape
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from employee.models import User

csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())

class CustomUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }

    username = forms.RegexField(label=_("Username"), max_length=30,
                                regex=r'^[\w.@+-]+$',
                                help_text=_("Required. 30 characters or fewer. Letters, digits and "
                                            "@/./+/-/_ only."),
                                error_messages={
        'invalid': _("This value may contain only letters, numbers and "
                     "@/./+/-/_ characters.")})
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    class Meta:
        # Point to our CustomUser here instead of default `User`
        model = User
        fields = ("username",)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            # Refer to our CustomUser here instead of default `User`
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        # Make sure we pass back in our CustomUserCreationForm and not the
        # default `UserCreationForm`
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    username = forms.RegexField(
        label=_("Username"), max_length=30, regex=r"^[\w.@+-]+$",
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                    "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    password = ReadOnlyPasswordHashField(label=_("Password"),
                                         help_text=_("Raw passwords are not stored, so there is noasdas way to see "
                                                     "this user's password, but you can change the password "
                                                     "using <a href=\"password/\">this form</a>."))

    class Meta:
        # Point to our CustomUser here instead of default `User`
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        # Make sure we pass back in our CustomUserChangeForm and not the
        # default `UserChangeForm`
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


# unable to save/edit data usinng the class below you may seach for appropriate code
class CustomUserAdmin(BaseUserAdmin):
	# form = UserChangeForm
	form = CustomUserChangeForm
	add_form = CustomUserCreationForm
	
	
	list_display = ('username','email','first_name','last_name', 'contact_no', 'user_type')
	
	list_filter =('is_staff', 'is_superuser', 'is_active', 'groups')
	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		('Personal info', {'fields': ( 'first_name','last_name','user_type', 'gender' )}),
		('Biography', {'fields': ('affiliation', 'department','position_title', 'degree','research_interest')}),
		('Contact Details', {'fields': ('contact_no', 'address', 'fax_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser','groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
	)
	
	add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
		),
	)
	search_fields = ('username', 'first_name', 'last_name', 'email')
	
	change_password_form = AdminPasswordChangeForm

	def get_fieldsets(self, request, obj=None):
		if not obj:
			return self.add_fieldsets
		return super(CustomUserAdmin, self).get_fieldsets(request, obj)
	
	def get_form(self, request, obj=None, **kwargs):
		"""
			Use special form during user creation
		"""
		defaults = {}
		if obj is None:
			defaults.update({
				'form': self.add_form,
			})
		defaults.update(kwargs)
		return super(CustomUserAdmin, self).get_form(request, obj, **defaults)

	def lookup_allowed(self, lookup, value):
		# See #20078: we don't want to allow any lookups involving passwords.
		if lookup.startswith('password'):
			return False
		return super(CustomUserAdmin, self).lookup_allowed(lookup, value)

	@sensitive_post_parameters_m
	@csrf_protect_m
	@transaction.atomic
	def add_view(self, request, form_url='', extra_context=None):
	# It's an error for a user to have add permission but NOT change
	# permission for users. If we allowed such users to add users, they
	# could create superusers, which would mean they would essentially have
	# the permission to change users. To avoid the problem entirely, we
	# disallow users from adding users if they don't have change
	# permission.
		if not self.has_change_permission(request):
			if self.has_add_permission(request) and settings.DEBUG:
				# Raise Http404 in debug mode so that the user gets a helpful
				# error message.
				raise Http404(
					'Your user does not have the "Change user" permission. In '
					'order to add users, Django requires that your user '
					'account have both the "Add user" and "Change user" '
					'permissions set.')
			raise PermissionDenied
		if extra_context is None:
			extra_context = {}
		
		defaults = {
			'auto_populated_fields': (),
		}
		extra_context.update(defaults)
		return super(CustomUserAdmin, self).add_view(request, form_url,
	                                             extra_context)
	def response_add(self, request, obj, post_url_continue=None):
		"""
		Determines the HttpResponse for the add_view stage. It mostly defers to
		its superclass implementation but is customized because the User model
		has a slightly different workflow.
		"""
		# We should allow further modification of the user just added i.e. the
		# 'Save' button should behave like the 'Save and continue editing'
		# button except in two scenarios:
		# * The user has pressed the 'Save and add another' button
		# * We are adding a user in a popup
		if '_addanother' not in request.POST and '_popup' not in request.POST:
			request.POST['_continue'] = 1
		return super(CustomUserAdmin, self).response_add(request, obj,
															post_url_continue)

admin.site.register(User, CustomUserAdmin)
