from django.shortcuts import render
from django.contrib.auth.views import logout, login
from django.views.generic import ListView, TemplateView, DetailView, UpdateView, CreateView
from django.views.generic.base import ContextMixin
#from django.views.generic.edit import ProcessFormView
from attendance.models import Musician, Job, AttendanceRecord
from attendance.forms import JobForm, ChecklistForm
#from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy

# Create your views here.
def index(request):
	if not request.user.is_authenticated():
		return render(request, 'attendance/index.html')
	else:
		# Calculates the year ranges
		# If no data, defaults to current fiscal year
		return render(request, 'attendance/welcome.html', {"active": "home"})

def login_view(request):
	# return render(request, 'attendance/login.html')
	return login(request, template_name='attendance/login.html')

def logout_view(request):
	return logout(request, next_page='/')

class LoginRequiredMixin(object):
	@classmethod
	def as_view(cls, **initkwargs):
		view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
		return login_required(view)

class JobMixin(ContextMixin):
	def get_context_data(self, **kwargs):
		context = super(JobMixin, self).get_context_data(**kwargs)
		context['active'] = 'jobs'
		return context

class MusicianMixin(ContextMixin):
	def get_context_data(self, **kwargs):
		context = super(MusicianMixin, self).get_context_data(**kwargs)
		context['active'] = 'musicians'
		return context

class AnalyticsMixin(ContextMixin):
	def get_context_data(self, **kwargs):
		context = super(AnalyticsMixin, self).get_context_data(**kwargs)
		context['active'] = 'analytics'
		return context

class TimesMixin(ContextMixin):
	def get_context_data(self, **kwargs):
		context = super(TimesMixin, self).get_context_data(**kwargs)
		context['active'] = 'times'
		return context

class AddMixin(ContextMixin):
	def get_context_data(self, **kwargs):
		context = super(AddMixin, self).get_context_data(**kwargs)
		context['active'] = 'add'
		return context

class MusicianList(ListView, LoginRequiredMixin, MusicianMixin):
	model = Musician
	template_name = "attendance/musicians.html"
	context_object_name = "musicians"

class TimeList(ListView, LoginRequiredMixin, TimesMixin):
	template_name = "attendance/times.html"
	queryset = Job.objects.filter(start_date__year=2014).order_by('start_date')
	context_object_name = "jobs"

	def get_context_data(self, **kwargs):
		context = super(TimeList, self).get_context_data(**kwargs)
		musicians = Musician.objects.all()
		context['musicians'] = musicians

		for job in self.queryset:
			context[job] = job.attendance_record.musicians_present.all()

		return context

class JobList(ListView, LoginRequiredMixin, JobMixin):
	model = Job
	template_name = "attendance/jobs.html"
	context_object_name = "jobs"

class JobView(DetailView, LoginRequiredMixin, JobMixin):
	model = Job
	context_object_name = 'job'
	template_name = "attendance/job.html"

	def get_context_data(self, **kwargs):
		context = super(JobView, self).get_context_data(**kwargs)
		musicians = Musician.objects.all()
		context['musicians'] = musicians
		return context

class MusicianView(DetailView, LoginRequiredMixin, MusicianMixin):
	model = Musician
	context_object_name = "musician"
	template_name = "attendance/musician.html"

	def get_context_data(self, **kwargs):
		context = super(MusicianView, self).get_context_data(**kwargs)
		musicians = Musician.objects.all()
		context['total_rehearsals'] = Job.objects.filter(job_type=0).count()
		context['total_gigs'] = Job.objects.exclude(job_type=0).count()
		return context

class AddJobView(CreateView, LoginRequiredMixin, AddMixin):
	template_name = 'attendance/addjob.html'
	#model = Job
	form_class = JobForm
	context_object_name = "job"

class AddRehearsalView(CreateView, LoginRequiredMixin, AddMixin):
	template_name = 'attendance/addjob.html'
	context_object_name = 'job'
	#model = Job
	form_class = JobForm
	initial = {
		'name': 'Rehearsal',
		'location': 'Fort York Armoury',
		'call_time': '19:45'}

class AddRosterView(DetailView, LoginRequiredMixin, AddMixin):
	model = Job
	context_object_name = 'job'
	template_name = 'attendance/add_attendance.html'

	def get_context_data(self, **kwargs):
		context = super(AddRosterView, self).get_context_data(**kwargs)
		context['title'] = 'Roster'
		return context

class AddAttendanceView(UpdateView, LoginRequiredMixin, AddMixin):
	model = AttendanceRecord
	context_object_name = 'attendance_record'
	template_name = 'attendance/add_attendance.html'
	form_class = ChecklistForm
	# success_url = get_object().job.get_absolute_url()

	def get_context_data(self, **kwargs):
		context = super(AddAttendanceView, self).get_context_data(**kwargs)
		context['title'] = 'Attendance'
		context['job'] = self.get_object().job
		return context

class AddAttendanceListView(ListView, LoginRequiredMixin, AddMixin):
	template_name = 'attendance/add_attendance_list.html'
	queryset = Job.objects.filter(attendance_record__musicians_present=None)
	context_object_name = 'no_jobs'

	def get_context_data(self, **kwargs):
		context = super(AddAttendanceListView, self).get_context_data(**kwargs)
		jobs = Job.objects.exclude(attendance_record__musicians_present=None)
		context['jobs'] = jobs
		return context

class Analytics(TemplateView, LoginRequiredMixin, AnalyticsMixin):
	template_name = "attendance/analytics.html"
