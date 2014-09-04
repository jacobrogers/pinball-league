from django import forms

input_class = {'class': 'form-control'}

class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30, widget=forms.TextInput(attrs=input_class))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs=input_class))

class AccountConfirmationForm(forms.Form):
    first_name = forms.CharField(label="First Name", max_length=30, widget=forms.TextInput(attrs=input_class))
    last_name = forms.CharField(label="Last Name", max_length=30, widget=forms.TextInput(attrs=input_class))
    ifpa_id = forms.IntegerField(label="IFPA ID", widget=forms.TextInput(attrs=input_class))
    signature = forms.CharField(label="Game Signature", max_length=3, widget=forms.TextInput(attrs=input_class))
    password = forms.CharField(label="Password", max_length=128, widget=forms.PasswordInput(attrs=input_class))
    confirm_password = forms.CharField(label="Confirm Password", max_length=128, widget=forms.PasswordInput(attrs=input_class))