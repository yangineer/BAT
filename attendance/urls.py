from django.conf.urls import url, patterns
from attendance.views import index, login_view, logout_view
from attendance.views import MusicianList, RehearsalList, GigList, TimeList, Analytics, RehearsalView, GigView, MusicianView, AddJobView, AddRosterView, AddRehearsalView, RehearsalYearView, GigYearView, AddAttendanceView, AddAttendanceListView

urlpatterns = patterns('',
	url(r'^$', index, name='index'),
	url(r'^login/$', login_view, name='login'),
	url(r'^logout/$', logout_view, name='logout'),
	url(r'^musicians/$', MusicianList.as_view(), name='musicians'),
	# url(r'^times/$', TimeList.as_view(), name='times'),
	url(r'^times/rehearsal/$', RehearsalYearView.as_view(), name='times_rehearsal'),
	url(r'^times/gig/$', GigYearView.as_view(), name='times_gig'),
	
	url(r'^rehearsals/$', RehearsalList.as_view(), name='rehearsals'),
	url(r'^rehearsals/(?P<pk>\d+)/$', RehearsalView.as_view(), name='rehearsalview'),
	url(r'^gigs/$', GigList.as_view(), name='gigs'),
	url(r'^gigs/(?P<pk>\d+)/$', GigView.as_view(), name='gigview'),

	url(r'^musicians/(?P<pk>\d+)/$', MusicianView.as_view(), name='musicianview'),
	url(r'^analytics/$', Analytics.as_view(), name='analytics'),
	url(r'^addjob/$', AddJobView.as_view(), name='addjob'),
	url(r'^addrehearsal/$', AddRehearsalView.as_view(), name='addrehearsal'),
 	url(r'^addattendance/$', AddAttendanceListView.as_view(), name='add_attendance_list'),
	url(r'^addattendance/(?P<pk>\d+)/$', AddAttendanceView.as_view(), name='add_attendance'),
	url(r'^addroster/(?P<pk>\d+)/$', AddRosterView.as_view(), name='add_roster'),

)