from django.shortcuts import render
from django.contrib.auth.views import logout, login
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.base import ContextMixin
from attendance.models import Musician, Job
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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

class JobList(ListView, LoginRequiredMixin, JobMixin):
	model = Job
	template_name = "attendance/jobs.html"
	context_object_name = "jobs"

class JobView(DetailView, LoginRequiredMixin, JobMixin):
	model = Job
	context_object_name = 'job'
	template_name = "attendance/job.html"

	# def get_context_data(self, **kwargs):
	# 	context = super(JobView, self).get_context_data(**kwargs)
		
	# 	context['active'] = 'add'
	# 	return context

class Analytics(TemplateView, LoginRequiredMixin, AnalyticsMixin):
	template_name = "attendance/analytics.html"
