from django.shortcuts import render
from django.contrib.auth.views import logout, login

# Create your views here.
def index(request):
	if not request.user.is_authenticated():
		return render(request, 'attendance/index.html')
	else:
		return render(request, 'attendance/framed_base.html')

def login_view(request):
	# return render(request, 'attendance/login.html')
	return login(request, template_name='attendance/login.html')

def logout_view(request):
	return logout(request, next_page='/')