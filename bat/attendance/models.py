from django.db import models
from django.conf import settings

# Create your models here.
class Musician(models.Model):
	""" Represents a musician """
	INSTRUMENT_SECTION_CHOICES = (
		('LEAD', 'Leaders'),
		('FLPC', 'Flutes & Piccolos'),
		('CLAR', 'Clarinets'),
		('OBBS', 'Oboes & Bassoons'),
		('SAXS', 'Saxophones'),
		('FRHN', 'French Horns'),
		('TRPT', 'Trumpets'),
		('TRBN', 'Trombones'),
		('EUTB', 'Euphoniums & Tubas & String Basses'),
		('PERC', 'Percussions'),
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
	instrument_section = models.CharField(max_length=4, choices=INSTRUMENT_SECTION_CHOICES)
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	is_retired = models.BooleanField(default=False)

	class Meta:
		ordering = ['-rank']

class On_Str_Musician(Musician):
	""" Represents an on-strength musician """
	service_number = models.CharField(max_length=9)

class Attendance(models.Model):
	""" Represents the attendance """
	musicians_present = models.ManyToManyField(Musician, related_name='present')
	musicians_absent = models.ManyToManyField(Musician, related_name='absent')

class Roster(models.Model):
	""" Represents the booking roster """
	musicians_booked = models.ManyToManyField(Musician)

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

	headdress = models.CharField(max_length=2, choices=HEADDRESS_CHOICES)
	tunic = models.CharField(max_length=2, choices=TUNIC_CHOICES)

class Job(models.Model):
	""" Represents an engagement job """
	name = models.CharField(max_length=30)
	start_date = models.DateField()
	end_date = models.DateField()
	call_time = models.TimeField()
	location = models.TextField()
	uniform = models.OneToOneField(Uniform)
	roster = models.OneToOneField(Roster)
	attendance = models.OneToOneField(Attendance)
