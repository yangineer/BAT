from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Q

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

	def present_rehearsals(self):
		return Rehearsal.objects.filter(
			Q(rehearsalattendance__musician=self), 
			Q(rehearsalattendance__status='O') | Q(rehearsalattendance__status='L')
		)

	def present_gigs(self):
		return Gig.objects.filter(
			Q(gigattendance__musician=self), 
			Q(gigattendance__status='O') | Q(gigattendance__status='L')
		)

	def num_present_rehearsals(self):
		return self.rehearsalattendance_record.exclude(Q(status='A') | Q(status='E')).count()

	def num_present_gigs(self):
		return self.gigattendance_record.exclude(status='A').count()

	def num_total_rehearsals(self):
		return self.rehearsalattendance_record.count()

	def num_total_gigs(self):
		return self.num_contacted_gigs()

	def percent_present_rehearsals(self):
		total = self.num_total_rehearsals()
		if total == 0:
			return 100
		else:
			return 100 * self.num_present_rehearsals() / total

	def num_contacted_gigs(self):
		return self.booking.count()

	def percent_present_gigs(self):
		total = self.num_contacted_gigs()
		if total == 0:
			return 100
		else:
			return 100 * self.num_present_gigs() / total

	class Meta:
		ordering = ['instrument_section', 'is_retired','-is_on_strength', '-rank']

class Leave(models.Model):
	""" Represents a leave of absense, ex. ED&T, CG Tasking, Borden, etc. """

	reason = models.CharField(max_length=80)
	musician = models.ForeignKey(Musician)
	start_date = models.DateField()
	end_date = models.DateField(blank=True, default=None)

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

class AttendanceRecord(models.Model):
	""" Represents an abstract attendance record """

	STATUS_CHOICES = (
		('O', 'On-time'),
		('L', 'Late'),
		('A', 'Absent'),
		('E', 'Exempt'),
	)

	musician = models.ForeignKey(Musician, related_name='%(class)s_record')
	status = models.CharField(max_length=1, choices = STATUS_CHOICES)
	reason = models.TextField(blank=True, null=True)

	class Meta:
		abstract = True

class RehearsalAttendance(AttendanceRecord):
	job = models.ForeignKey('Rehearsal')

class GigAttendance(AttendanceRecord):
	job = models.ForeignKey('Gig')

class BookingRecord(models.Model):
	""" Represents the booking record for gigs only"""

	STATUS_CHOICES = (
		('Y', 'Yes'),
		('N', 'No'),
		('M', 'Maybe'),
		('R', 'Yet to Reply'),
		('Z', 'Not Contacted'),
	)

	musician = models.ForeignKey(Musician, related_name='booking')
	gig = models.ForeignKey('Gig')
	status = models.CharField(max_length=1, choices=STATUS_CHOICES)

class Rehearsal(models.Model):
	""" Represents a regular rehearsal """

	start_date = models.DateField()
	musicians_attending = models.ManyToManyField(Musician, related_name='rehearsals_attending', through=RehearsalAttendance)

	def name(self):
		return "Rehearsal"

	def location(self):
		return "Fort York Armoury"

	def uniform(self):
		return "Civis"

	def __str__(self):
		return 'Rehearsal on %s' % (self.start_date)

	def num_present(self):
		return self.rehearsalattendance_set.filter(Q(status='O') | Q(status='L')).count()

	def num_on_strength_present(self):
		attendances = self.rehearsalattendance_set.filter(Q(status='O') | Q(status='L')).select_related('musicians')
		on_str_musicians = [x.musician for x in attendances if x.musician.is_on_strength]
		return len(on_str_musicians)

	def num_booked(self):
		return self.rehearsalattendance_set.exclude(status='E').count()

	def num_on_strength_booked(self):
		attendances = self.rehearsalattendance_set.exclude(status='E').select_related('musicians')
		on_str_musicians = [x.musician for x in attendances if x.musician.is_on_strength]
		return len(on_str_musicians)

	def has_attendance(self):
		return self.num_present()

	def attendance(self):
		return RehearsalAttendance

class Gig(models.Model):
	""" Represents an engagement job """

	TYPE_CHOICES = (
		('C', 'Concert'),
		('P', 'Parade'),
	)

	start_date = models.DateField()
	musicians_attending = models.ManyToManyField(Musician, related_name='gigs_attending', through=GigAttendance)

	name = models.CharField(max_length=80)
	end_date = models.DateField(blank=True, default=None)
	call_time = models.TimeField(blank=True, null=True)
	location = models.CharField(max_length=80)
	uniform = models.ForeignKey(Uniform, blank=True, null=True, default=None)
	job_type = models.CharField(max_length=1, choices=TYPE_CHOICES)

	musicians_contacted = models.ManyToManyField(Musician, related_name='contacted', through='BookingRecord')

	def __str__(self):
		return '%s at %s on %s' % (self.name, self.location, self.start_date)

	def get_absolute_url(self):
		return reverse('attendance:jobview', kwargs={'pk': self.pk})

	def save(self, *args, **kwargs):
		""" Sets the end date to start date by default """
		if not self.end_date:
			self.end_date = self.start_date

		super(Gig, self).save(*args, **kwargs)

	def num_booked(self):
		#return self.roster.musicians_booked.count()
		return Musician.objects.count()

	def num_on_strength_booked(self):
		#return self.roster.num_on_strength()
		return Musician.objects.filter(is_on_strength=True).count()

	def has_booking(self):
		return self.musicians_contacted.count()

	def num_present(self):
		return self.musicians_attending.count()

	def num_on_strength_present(self):
		return self.musicians_attending.filter(is_on_strength=True).count()

	def has_attendance(self):
		return self.num_present()

	def attendance(self):
		return GigAttendance
