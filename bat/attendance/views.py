from django.shortcuts import render
from django.contrib.auth.views import logout, login
from django.views.generic import ListView, TemplateView
from attendance.models import Musician, Job

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

class MusicianList(ListView):
	model = Musician
	template_name = "attendance/musicians.html"
	context_object_name = "musicians"

	def get_context_data(self, **kwargs):
		context = super(MusicianList, self).get_context_data(**kwargs)
		context['active'] = 'musicians'
		return context

class TimeList(TemplateView):
	template_name = "attendance/times.html"

	def get_context_data(self, **kwargs):
		context = super(TimeList, self).get_context_data(**kwargs)
		context['active'] = 'times'
		return context

class JobList(ListView):
	model = Job
	template_name = "attendance/jobs.html"
	context_object_name = "jobs"

	def get_context_data(self, **kwargs):
		context = super(JobList, self).get_context_data(**kwargs)
		context['active'] = 'jobs'
		return context

class Analytics(TemplateView):
	template_name = "attendance/analytics.html"

	def get_context_data(self, **kwargs):
		context = super(Analytics, self).get_context_data(**kwargs)
		context['active'] = 'analytics'
		return context