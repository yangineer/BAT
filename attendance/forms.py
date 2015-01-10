from django.forms.extras.widgets import SelectDateWidget
from django import forms
from attendance.models import Gig, Musician, Rehearsal

class GigForm(forms.ModelForm):

	class Meta:
		model = Gig
		fields = ['name', 'start_date', 'location', 'job_type']
		widgets = {'start_date': SelectDateWidget()}


class ChecklistForm(forms.ModelForm):
	
	class Meta:
		model = Rehearsal
		fields = ['musicians_attending']
		widgets = {'musicians_attending': forms.CheckboxSelectMultiple}