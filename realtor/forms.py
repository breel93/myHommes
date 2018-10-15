from django import forms
from .models import Realtor
from main.models import User


class NewRealtorForm(forms.ModelForm):

	# agree_to_terms = forms.BooleanField(label='Agree to Terms', widget=forms.CheckboxInput)
	class Meta:
		model = Realtor
		fields = ( 
			'address',
			'state',
			'phone_number',
			'website',
			'company_name',
			'image',
			'agree_to_terms', 
		)
	




