from django.conf.urls import url, patterns
from attendance import views
from attendance.views import MusicianList, JobList, TimeList, Analytics, JobView

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^login/$', views.login_view, name='login'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^musicians/$', MusicianList.as_view(), name='musicians'),
	url(r'^times/$', TimeList.as_view(), name='times'),
	url(r'^jobs/$', JobList.as_view(), name='jobs'),
	url(r'^jobs/(?P<pk>\d+)/$', JobView.as_view(), name='jobview'),
	url(r'^analytics/$', Analytics.as_view(), name='analytics'),
)