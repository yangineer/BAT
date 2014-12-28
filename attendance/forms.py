from django.forms.extras.widgets import SelectDateWidget
from django import forms
from attendance.models import Job, Musician, AttendanceRecord

class JobForm(forms.ModelForm):

	class Meta:
		model = Job
		fields = ['name', 'start_date', 'location', 'job_type']
		widgets = {'start_date': SelectDateWidget()}


class ChecklistForm(forms.ModelForm):
	#present = forms.BooleanField(widget=forms.CheckboxInput)
	#musicians_present = forms.ModelMultipleChoiceField(queryset=Musician.objects.all(), widget=forms.CheckboxSelectMultiple)

	class Meta:
		model = AttendanceRecord
		fields = ['musicians_present']
		widgets = {'musicians_present': forms.CheckboxSelectMultiple}