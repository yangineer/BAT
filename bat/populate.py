import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bat.settings')
import csv
from datetime import datetime
import django
django.setup()
from attendance.models import Musician, Job, Roster, AttendanceRecord

def populate():
	with open('RehearsalAttend.csv') as csvfile:
		attendance_reader = csv.reader(csvfile)
		iterator = iter(attendance_reader)
		gigs = iterator.__next__() 
		create_gigs(gigs)
		for row in iterator:
			#print(row)

			# Empty string means instrumentation
			if row[0]:
				section = row[0]
				#print("Instrument is " + section)
			else:
				rank = row[1]
				name = row[2]
				musician = create_musician(rank, name, section)
				for index, attendance_data in enumerate(row[3:]):
					update_roster(gigs[index + 3], musician)
					_attendance = create_attendance(gigs[index + 3])
					if attendance_data == '1':
						#print("attendance")
						update_attendance(_attendance, musician)
					else:
						
						if attendance_data == '0':
							#print("absent")
							pass
						else:
							#print("absent due to " + attendance_data)
							pass


def update_roster(date_string, musician):
	date = datetime.strptime(date_string, "%d-%b-%y").date()
	job = Job.objects.get(start_date=date)
	roster = Roster.objects.get_or_create(job=job)[0]
	roster.job = job
	roster.musicians_booked.add(musician)

def create_attendance(date_string):
	date = datetime.strptime(date_string, "%d-%b-%y").date()
	job = Job.objects.get(start_date=date)
	_attendance = AttendanceRecord.objects.get_or_create(job=job)[0]
	return _attendance

def update_attendance(_attendance, musician):
	_attendance.musicians_present.add(musician)

def create_gigs(gig_string):
	for rehearsal_date in gig_string[3:]:
		date = datetime.strptime(rehearsal_date, "%d-%b-%y").date()
		#print ("Creating a rehearsal for " + date.isoformat())
		name = 'rehearsal'
		location = 'Fort York Armoury'
		Job.objects.get_or_create(name=name, location=location, start_date=date)

def create_musician(rank, full_name, section):
	names = full_name.split(sep=', ')
	last_name = names[0]
	first_name = names[1]

	matching_rank = [x for x in Musician.RANK_CHOICES if rank.find(x[1]) >= 0]
	rank_tuple = matching_rank[-1]
	rank_id = rank_tuple[0]
	if rank.find("ret") >= 0:
		retired = True
	else:
		retired = False
	#print("Section is %s" % (section.split()[0]))
	matching_section = [x for x in Musician.INSTRUMENT_SECTION_CHOICES if x[1].find(section.split()[0]) >= 0][-1]
	section_id = matching_section[0]
	return Musician.objects.get_or_create(rank=rank_id, last_name=last_name, first_name=first_name, instrument_section=section_id, is_retired=retired)[0]
	#print("Attendance for %s - %s - %s from section %s and retired is %s" % (rank_tuple[1], last_name, first_name, matching_section[-1], retired))

if __name__ == '__main__':
	print('Starting BAT population script...')
	populate()
	print('Done!')