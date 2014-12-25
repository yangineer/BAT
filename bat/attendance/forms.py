from django.forms import ModelForm
from attendance.models import Job

class JobForm(ModelForm):

	class Meta:
		model = Job
		fields = ['name', 'start_date', 'end_date', 'call_time', 'location', 'uniform', 'job_type']