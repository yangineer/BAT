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

	class Meta:
		ordering = ['instrument_section', '-rank']

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

class Job(models.Model):
	""" Represents an engagement job """
	name = models.CharField(max_length=30)
	start_date = models.DateField()
	end_date = models.DateField(blank=True, default=None)
	call_time = models.TimeField(blank=True, null=True)
	location = models.CharField(max_length=30)
	uniform = models.ForeignKey(Uniform, null=True, default=None)

	def __str__(self):
		return '%s at %s on %s' % (self.name, self.location, self.start_date)

	def save(self, *args, **kwargs):
		""" Sets the end date to start date by default """
		if not self.end_date:
			self.end_date = self.start_date
		super(Job, self).save(*args, **kwargs)

class Attendance(models.Model):
	""" Represents the attendance """
	#musicians_present = models.ManyToManyField(Musician, related_name='present')
	musicians_absent = models.ManyToManyField(Musician, related_name='absent', null=True, default=None)
	job = models.OneToOneField(Job, null=True, default=None)

class Roster(models.Model):
	""" Represents the booking roster """
	musicians_booked = models.ManyToManyField(Musician)
	job = models.OneToOneField(Job, null=True, default=None)
