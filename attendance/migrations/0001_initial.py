# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('status', models.CharField(choices=[('O', 'On-time'), ('L', 'Late'), ('A', 'Absent')], max_length=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BookingRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('status', models.CharField(choices=[('Y', 'Yes'), ('N', 'No'), ('M', 'Maybe'), ('R', 'Yet to Reply')], max_length=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('start_date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Gig',
            fields=[
                ('job_ptr', models.OneToOneField(to='attendance.Job', parent_link=True, serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('end_date', models.DateField(blank=True, default=None)),
                ('call_time', models.TimeField(blank=True, null=True)),
                ('location', models.CharField(max_length=80)),
                ('job_type', models.CharField(choices=[('C', 'Concert'), ('P', 'Parade')], max_length=1)),
            ],
            options={
            },
            bases=('attendance.job',),
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, default=None)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Musician',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('rank', models.CharField(choices=[('00', 'Musn'), ('10', 'Pte'), ('20', 'Cpl'), ('30', 'MCpl'), ('40', 'Sgt'), ('50', 'CSgt'), ('60', 'WO'), ('65', 'DM'), ('70', 'Lt'), ('80', 'Capt'), ('90', 'Maj')], max_length=2)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('instrument_section', models.CharField(choices=[('0LEAD', 'Leaders'), ('1FLPC', 'Flutes & Piccolos'), ('2CLAR', 'Clarinets'), ('3OBBS', 'Oboes & Bassoons'), ('4SAXS', 'Saxophones'), ('5FRHN', 'French Horns'), ('6TRPT', 'Trumpets'), ('7TRBN', 'Trombones'), ('8EUTB', 'Euphoniums & Tubas & String Basses'), ('9PERC', 'Percussions')], max_length=5)),
                ('is_retired', models.BooleanField(default=False)),
                ('is_on_strength', models.BooleanField(default=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, blank=True, null=True)),
            ],
            options={
                'ordering': ['instrument_section', 'is_retired', '-is_on_strength', '-rank'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rehearsal',
            fields=[
                ('job_ptr', models.OneToOneField(to='attendance.Job', parent_link=True, serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=('attendance.job',),
        ),
        migrations.CreateModel(
            name='Uniform',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('headdress', models.CharField(choices=[('BS', 'Bearskin'), ('FC', 'Flat Cap'), ('BE', 'Beret'), ('FO', 'FFO'), ('BF', 'Bearskin & Flat Cap')], max_length=2)),
                ('tunic', models.CharField(choices=[('SC', 'Scarlet'), ('WH', 'Whites'), ('1A', 'DEU 1A'), ('3B', 'DEU 3B')], max_length=2)),
                ('kit', models.CharField(choices=[('MS', 'Music Stand'), ('LY', 'Lyre'), ('ML', 'Music Stand & Lyre')], max_length=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='leave',
            name='musician',
            field=models.ForeignKey(to='attendance.Musician'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='musicians_attending',
            field=models.ManyToManyField(related_name='attending', to='attendance.Musician', through='attendance.AttendanceRecord'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gig',
            name='musicians_contacted',
            field=models.ManyToManyField(related_name='contacted', to='attendance.Musician', through='attendance.BookingRecord'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gig',
            name='uniform',
            field=models.ForeignKey(to='attendance.Uniform', blank=True, default=None, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bookingrecord',
            name='gig',
            field=models.ForeignKey(to='attendance.Gig'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bookingrecord',
            name='musician',
            field=models.ForeignKey(related_name='booked', to='attendance.Musician'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attendancerecord',
            name='job',
            field=models.ForeignKey(to='attendance.Job'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attendancerecord',
            name='musician',
            field=models.ForeignKey(related_name='attended', to='attendance.Musician'),
            preserve_default=True,
        ),
    ]
