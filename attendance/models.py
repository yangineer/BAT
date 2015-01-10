from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

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
		return []

	def present_gigs(self):
		return []

	def num_present_rehearsals(self):
		return len(self.present_rehearsals())

	def num_present_gigs(self):
		return len(self.present_gigs())

	def percent_present_rehearsals(self):
		return 100 * self.num_present_rehearsals() / Rehearsal.objects.count()

	def percent_present_gigs(self):
		return 100 * self.num_present_gigs() / Gig.objects.count()

	class Meta:
		ordering = ['instrument_section', 'is_retired','-is_on_strength', '-rank']

class Leave(models.Model):
	""" Represents a leave of absense, ex. ED&T, CG Tasking, Borden, etc. """

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
	""" Represents the attendance record """
	STATUS_CHOICES = (
		('O', 'On-time'),
		('L', 'Late'),
		('A', 'Absent'),
	)

	musician = models.ForeignKey(Musician, related_name='attended')
	job = models.ForeignKey('Job')
	status = models.CharField(max_length=1, choices = STATUS_CHOICES)
	reason = models.TextField(blank=True, null=True)

class BookingRecord(models.Model):
	""" Represents the booking record """

	STATUS_CHOICES = (
		('Y', 'Yes'),
		('N', 'No'),
		('M', 'Maybe'),
		('R', 'Yet to Reply'),
	)

	musician = models.ForeignKey(Musician, related_name='booked')
	gig = models.ForeignKey('Gig')
	status = models.CharField(max_length=1, choices=STATUS_CHOICES)

class Job(models.Model):
	""" Reresents a generic job """
	start_date = models.DateField()
	musicians_attending = models.ManyToManyField(Musician, related_name='attending', through='AttendanceRecord')

	def num_present(self):
		return self.musicians_attending.count()

	def num_on_strength_present(self):
		return self.musicians_attending.filter(is_on_strength=True).count()

	def has_attendance(self):
		return self.num_present()

class Rehearsal(Job):
	""" Represents a regular rehearsal """

	def name(self):
		return "Rehearsal"

	def location(self):
		return "Fort York Armoury"

	def uniform(self):
		return "Civis"

	def __str__(self):
		return 'Rehearsal on %s' % (self.start_date)

class Gig(Job):
	""" Represents an engagement job """

	TYPE_CHOICES = (
		('C', 'Concert'),
		('P', 'Parade'),
	)

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
