from django import forms
from .models import User
# from journals.models import Journal

class Login_Form(forms.Form):
    username = forms.CharField(
        widget   = forms.TextInput(
            attrs = {
                'placeholder' : 'Username',
                'class'       : 'form-control',
                'id'          : 'username',
                'required'    : 'True',
            }
        ),
    )
     
    password = forms.CharField(
        widget   = forms.PasswordInput(
            attrs = {
                'placeholder' : 'Password',
                'class'       : 'form-control',
                'id'          : 'password',
                'required'    : 'True',
            }
        ),
    )

class Validation_Form(forms.Form):
    validation_code = forms.CharField(
        label    = '', 
        widget   = forms.TextInput(
            attrs = {
                'placeholder' : 'Registration Validation Code',
                'class'       : 'form-control',
                'id'          : 'validation_code',
                'maxlength'   : 9,
                'type'        : 'text',
                'required'    : 'True',
            }
        ),
    )
    
class Registration_Form(forms.Form):

    username = forms.CharField(
        label    = '', 
        widget   = forms.TextInput(
            attrs = {
                'placeholder' : 'Username',
                'class'       : 'form-control',
                'id'          : 'username',
                'maxlength'   : 50,
                'type'        : 'text',
                'required'    : 'True',
            }
        ),
    )    
    
    password = forms.CharField(
        label    = '',
        widget   = forms.PasswordInput(
            attrs = {
                'placeholder' : 'Password',
                'class'       : 'form-control',
                'id'          : 'password',
                'maxlength'   : 30,
                'type'        : 'password',
                'required'    : 'True',
            }
        ),
    )
    
    confirm_password = forms.CharField(
        label    = '',
        widget   = forms.PasswordInput(
            attrs = {
                'placeholder' : 'Confirm Password',
                'class'       : 'form-control',
                'id'          : 'confirm_password',
                'maxlength'   : 30,
                'type'        : 'password',
                'required'    : 'True',
            }
        ),
    )
    
    email_address = forms.EmailField(
        label    = '', 
        widget   = forms.TextInput(
            attrs = {
                'placeholder' : 'E-mail Address',
                'class'       : 'form-control',
                'id'          : 'email_address',
                'maxlength'   : 50,
                'type'        : 'email',
                'required'    : 'True',
            }
        ),
    )
    
    first_name = forms.CharField(
        label    = '', 
        widget   = forms.TextInput(
            attrs = {
                'placeholder' : 'Firstname',
                'class'       : 'form-control',
                'id'          : 'first_name',
                'maxlength'   : 50,
                'type'        : 'text',
                'required'    : 'True',
            }
        ),
    )
    
    middle_name = forms.CharField(
        label    = '', 
        widget   = forms.TextInput(
            attrs = {
                'placeholder' : 'Middlename',
                'class'       : 'form-control',
                'id'          : 'middle_name',
                'maxlength'   : 50,
                'type'        : 'text',
                'required'    : 'True',
            }
        ),
    )
    
    last_name = forms.CharField(
        label    = '', 
        widget   = forms.TextInput(
            attrs = {
                'placeholder' : 'Lastname',
                'class'       : 'form-control',
                'id'          : 'last_name',
                'maxlength'   : 50,
                'type'        : 'text',
                'required'    : 'True',
            }
        ),
    )
    
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    gender = forms.ChoiceField(
        label = '',
        choices = GENDER,
        widget   = forms.Select(
            attrs = {
                'placeholder' : 'Gender',
                'class'       : 'form-control',
                'id'          : 'gender',
                'maxlength'   : 50,
                'type'        : 'text',
                'required'    : 'True',
            }
        ),
    )
    
    address = forms.CharField(
        label    = '', 
        widget   = forms.TextInput(
            attrs = {
                'placeholder' : 'Address',
                'class'       : 'form-control',
                'id'          : 'address',
                'maxlength'   : 150,
                'type'        : 'text',
                'required'    : 'True',
            }
        ),
    )
    
    contact_no = forms.CharField(
        label    = '', 
        widget   = forms.TextInput(
            attrs = {
                'placeholder' : 'Contact Number',
                'class'       : 'form-control',
                'id'          : 'contact_no',
                'maxlength'   : 50,
                'type'        : 'text',
                'required'    : 'True',
            }
        ),
    )

    # affiliation     = forms.CharField(
    #     label    = '', 
    #     widget   = forms.TextInput(
    #         attrs = {
    #             'placeholder' : 'Affiliation',
    #             'class'       : 'form-control',
    #             'id'          : 'affiliation',
    #             'maxlength'   : 70,
    #             'type'        : 'text',
    #             'required'    : 'True',
    #         }
    #     ),
    # )

    department      = forms.CharField(
        label    = '', 
        widget   = forms.TextInput(
            attrs = {
                'placeholder' : 'Department',
                'class'       : 'form-control',
                'id'          : 'department',
                'maxlength'   : 70,
                'type'        : 'text',
                'required'    : 'True',
            }
        ),
    )

    TITLE = (
        ('Prof', 'Professor'),
        ('Engr', 'Engineer'),
        ('Dr', 'Doctor'),
        ('Atty', 'Attorney')
    )

    title = forms.ChoiceField(
        label = '',
        choices = TITLE,
        widget   = forms.Select(
            attrs = {
                'placeholder' : 'Title',
                'class'       : 'form-control',
                'id'          : 'title',
                'maxlength'   : 50,
                'type'        : 'text',
                'required'    : 'True',
            }
        ),
    )

class Author_Form(forms.Form):
    
    email = forms.EmailField(required=False,
        widget   = forms.TextInput(
            attrs = {
                'placeholder' : 'E-mail Address',
                'class'       : 'form-control',
                'id'          : 'email',
                'maxlength'   : 50,
                'type'        : 'email',
            }
        ),
    )
    
    first_name = forms.CharField(
        widget   = forms.TextInput(
            attrs = {
                'placeholder' : 'Firstname',
                'class'       : 'form-control',
                'id'          : 'first_name',
                'maxlength'   : 50,
                'type'        : 'text',
                'required'    : 'True',
            }
        ),
    )
    
    middle_name = forms.CharField( required=False,
        widget   = forms.TextInput(
            attrs = {
                'placeholder' : 'Middlename',
                'class'       : 'form-control',
                'id'          : 'middle_name',
                'maxlength'   : 50,
                'type'        : 'text',
                'required'    : 'True',
            }
        ),
    )
    
    last_name = forms.CharField(
        widget   = forms.TextInput(
            attrs = {
                'placeholder' : 'Lastname',
                'class'       : 'form-control',
                'id'          : 'last_name',
                'maxlength'   : 50,
                'type'        : 'text',
                'required'    : 'True',
            }
        ),
    )
    
    address = forms.CharField(
        widget   = forms.TextInput(
            attrs = {
                'placeholder' : 'Address',
                'class'       : 'form-control',
                'id'          : 'address',
                'maxlength'   : 150,
                'type'        : 'text',
                'required'    : 'True',
            }
        ),
    )
    
    contact_no = forms.CharField(required=False,
        widget   = forms.TextInput(
            attrs = {
                'placeholder' : 'Contact Number',
                'class'       : 'form-control',
                'id'          : 'contact_no',
                'maxlength'   : 50,
                'type'        : 'text',
                
            }
        ),
    )

    # affiliation   = forms.CharField(required=False,
    #     widget   = forms.TextInput(
    #         attrs = {
    #             'placeholder' : 'Affiliation',
    #             'class'       : 'form-control',
    #             'id'          : 'affiliation',
    #             'maxlength'   : 70,
    #             'type'        : 'text',
    #         }
    #     ),
    # )

    department      = forms.CharField(
        widget   = forms.TextInput(
            attrs = {
                'placeholder' : 'Department',
                'class'       : 'form-control',
                'id'          : 'department',
                'maxlength'   : 70,
                'type'        : 'text',
                'required'    : 'True',
            }
        ),
    )

    position_title      = forms.CharField(
        widget   = forms.TextInput(
            attrs = {
                'placeholder' : 'Position Title',
                'class'       : 'form-control',
                'id'          : 'position_title',
                'maxlength'   : 70,
                'type'        : 'text',
                'required'    : 'True',
            }
        ),
    )

    # POSITION_TITLE = (
    #     ('Prof', 'Professor'),
    #     ('Engr', 'Engineer'),
    #     ('Dir', 'Director'),
    #     ('Atty', 'Attorney'),
    #     ('Dean','Dean')
    # )

    # position_title = forms.ChoiceField(
    #     label = '',
    #     choices = POSITION_TITLE,
    #     widget   = forms.Select(
    #         attrs = {
    #             'placeholder' : 'Title',
    #             'class'       : 'form-control',
    #             'id'          : 'position_title',
    #             'maxlength'   : 50,
    #             'type'        : 'text',
    #             'required'    : 'True',
    #         }
    #     ),
    # )