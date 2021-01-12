from django import forms
from cle.models import Caractere

class CaractereForm(forms.ModelForm):
	 
	 class Meta:
			model = Caractere
			fields = '__all__'

