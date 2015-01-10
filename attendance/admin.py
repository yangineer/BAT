from django.contrib import admin
from attendance.models import Rehearsal, Gig, Musician, Uniform, RehearsalAttendance

# Register your models here.

@admin.register(Musician)
class MusicianAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'instrument_section', 'is_on_strength', 'is_retired')
	#list_editable = ('instrument_section', 'is_on_strength', 'is_retired') 
	list_filter = ('is_retired', 'is_on_strength')

# @admin.register(Uniform)
# class UniformAdmin(admin.ModelAdmin):
# 	list_display = ('__str__', 'name', 'headdress', 'tunic', 'kit')
# 	list_editable = ('name', 'headdress', 'tunic', 'kit')
	
admin.site.register(Rehearsal)
admin.site.register(Gig)
#admin.site.register(RehearsalAttendance)
#admin.site.register(Job)