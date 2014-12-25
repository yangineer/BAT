from django.conf.urls import url, patterns
from attendance.views import index, login_view, logout_view
from attendance.views import MusicianList, JobList, TimeList, Analytics, JobView, MusicianView, AddJobView, AddAttendanceListView

urlpatterns = patterns('',
	url(r'^$', index, name='index'),
	url(r'^login/$', login_view, name='login'),
	url(r'^logout/$', logout_view, name='logout'),
	url(r'^musicians/$', MusicianList.as_view(), name='musicians'),
	url(r'^times/$', TimeList.as_view(), name='times'),
	url(r'^jobs/$', JobList.as_view(), name='jobs'),
	url(r'^jobs/(?P<pk>\d+)/$', JobView.as_view(), name='jobview'),
	url(r'^musicians/(?P<pk>\d+)/$', MusicianView.as_view(), name='musicianview'),
	url(r'^analytics/$', Analytics.as_view(), name='analytics'),
	url(r'^addjob/$', AddJobView.as_view(), name='addjob'),
	url(r'^addattendance/$', AddAttendanceListView.as_view(), name='add_attendance_list'),
)