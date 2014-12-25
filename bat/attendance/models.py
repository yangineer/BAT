from django.db import models
from django.conf import settings

# Create your models here.
class Musician(models.Model):
	""" Represents a musician """
	INSTRUMENT_SECTION_CHOICES = (
		('0LEAD', 'Leaders'),
		('1FLPC', 'Flutes & Piccolos'),
		('2CLAR', 'Clarinets'),
		('3OBBS', 'Oboes & Bassoons'),
		('4SAXS', 'Saxophones'),
		('5FRHN', 'French Horns'),
		('6TRPT', 'Trumpets'),
		('7TRBN', 'Trombones'),
		('8EUTB', 'Euphoniums & Tubas & String Basses'),
		('9PERC', 'Percussions'),
	)
	RANK_CHOICES = (
		('00', 'Musn'),
		('10', 'Pte'),
		('20', 'Cpl'),
		('30', 'MCpl'),
		('40', 'Sgt'),
		('50', 'CSgt'),
		('60', 'WO'),
		('65', 'DM'),
		('70', 'Lt'),
		('80', 'Capt'),
		('90', 'Maj'),
	)
	rank = models.CharField(max_length=2, choices=RANK_CHOICES)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	instrument_section = models.CharField(max_length=5, choices=INSTRUMENT_SECTION_CHOICES)
	user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)
	is_retired = models.BooleanField(default=False)
	is_on_strength = models.BooleanField(default=False)

	def __str__(self):
		return '%s %s, %s' % (self.get_rank_display(), self.last_name, self.first_name)

	def name(self):
		return self.last_name + ", " + self.first_name

	def present_jobs(self):
		"""returns a list of jobs that the user is present in """
		attendances = self.present.filter(musicians_present__id=self.pk).select_related('job')
		return [x.job for x in attendances]

	class Meta:
		ordering = ['instrument_section', 'is_retired','-is_on_strength', '-rank']

# class On_Str_Musician(Musician):
# 	""" Represents an on-strength musician """
# 	service_number = models.CharField(max_length=9, blank=True)

# 	def on_str(self):
# 		return True

# 	class Meta:
# 		verbose_name = 'On Strength Musician'

class Uniform(models.Model):
	""" Represents the different uniform/kit options """
	HEADDRESS_CHOICES = (
		('BS', 'Bearskin'),
		('FC', 'Flat Cap'),
		('BE', 'Beret'),
		('FO', 'FFO'),
		('BF', 'Bearskin & Flat Cap'),
	)

	TUNIC_CHOICES = (
		('SC', 'Scarlet'),
		('WH', 'Whites'),
		('1A', 'DEU 1A'),
		('3B', 'DEU 3B'),
	)

	KIT_CHOICES = (
		('MS', 'Music Stand'),
		('LY', 'Lyre'),
		('ML', 'Music Stand & Lyre'),
	)
	name = models.CharField(max_length=30)
	headdress = models.CharField(max_length=2, choices=HEADDRESS_CHOICES)
	tunic = models.CharField(max_length=2, choices=TUNIC_CHOICES)
	kit = models.CharField(max_length=2, choices=KIT_CHOICES)
	def __str__(self):
		return '%s: %s/%s/%s' % (self.name, self.get_headdress_display(), self.get_tunic_display(), self.get_kit_display())

class Roster(models.Model):
	""" Represents the booking roster """
	musicians_booked = models.ManyToManyField(Musician, blank=True, null=True, default=None)

	def __str__(self):
		return 'Roster for %s' % (self.job)

	def num_on_strength(self):
		return self.musicians_booked.filter(is_on_strength=True).count()

class AttendanceRecord(models.Model):
	""" Represents the attendance """
	musicians_present = models.ManyToManyField(Musician, related_name='present', null=True, default=None)
	#musicians_absent = models.ManyToManyField(Musician, related_name='absent', null=True, default=None)

	def __str__(self):
		return 'Attendance for %s' % (self.job)

	def num_on_strength(self):
		return self.musicians_present.filter(is_on_strength=True).count()

class Job(models.Model):
	""" Represents an engagement job """

	TYPE_CHOICES = list(enumerate([
		'Rehearsal',
		'Parade',
		'Concert',
	]))

	name = models.CharField(max_length=50)
	start_date = models.DateField()
	end_date = models.DateField(blank=True, default=None)
	call_time = models.TimeField(blank=True, null=True)
	location = models.CharField(max_length=50)
	uniform = models.ForeignKey(Uniform, blank=True, null=True, default=None)
	job_type = models.IntegerField(default=0, choices=TYPE_CHOICES)
	roster = models.OneToOneField(Roster, blank=True, null=True)
	attendance_record = models.OneToOneField(AttendanceRecord, blank=True, null=True)

	def __str__(self):
		return '%s at %s on %s' % (self.name, self.location, self.start_date)

	def save(self, *args, **kwargs):
		""" Sets the end date to start date by default """
		if not self.end_date:
			self.end_date = self.start_date

		if not self.roster:
			roster = Roster()
			roster.save()
			self.roster = roster 

		if not self.attendance_record:
			attendance_record = AttendanceRecord()
			attendance_record.save()
			self.attendance_record = attendance_record

		super(Job, self).save(*args, **kwargs)

	def num_present(self):
		return self.attendance_record.musicians_present.count()

	def num_booked(self):
		return self.roster.musicians_booked.count()

	def num_on_strength_booked(self):
		return self.roster.num_on_strength()

	def num_on_strength_present(self):
		return self.attendance_record.num_on_strength()

	def is_rehearsal(self):
		return self.job_type == 0

	def no_attendance(self):
		return self.attendance_record.musicians_present == None

class ActiveRoster(models.Model):
	""" Represents the active roster for a given year """
	date = models.DateField(unique_for_year=True)
	musicians_active = models.ManyToManyField(Musician, related_name='active', null=True, default=None)

	def fiscal_year():
		""" Return the fiscal year of the date for the active roster """
		if self.date.month < 4:
			return date.year - 1
		else:
			return date.year 