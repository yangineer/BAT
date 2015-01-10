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
            name='BookingRecord',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('status', models.CharField(choices=[('Y', 'Yes'), ('N', 'No'), ('M', 'Maybe'), ('R', 'Yet to Reply')], max_length=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Gig',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('start_date', models.DateField()),
                ('name', models.CharField(max_length=80)),
                ('end_date', models.DateField(blank=True, default=None)),
                ('call_time', models.TimeField(blank=True, null=True)),
                ('location', models.CharField(max_length=80)),
                ('job_type', models.CharField(choices=[('C', 'Concert'), ('P', 'Parade')], max_length=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GigAttendance',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('status', models.CharField(choices=[('O', 'On-time'), ('L', 'Late'), ('A', 'Absent')], max_length=1)),
                ('reason', models.TextField(blank=True, null=True)),
                ('job', models.ForeignKey(to='attendance.Gig')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('rank', models.CharField(choices=[('00', 'Musn'), ('10', 'Pte'), ('20', 'Cpl'), ('30', 'MCpl'), ('40', 'Sgt'), ('50', 'CSgt'), ('60', 'WO'), ('65', 'DM'), ('70', 'Lt'), ('80', 'Capt'), ('90', 'Maj')], max_length=2)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('instrument_section', models.CharField(choices=[('0LEAD', 'Leaders'), ('1FLPC', 'Flutes & Piccolos'), ('2CLAR', 'Clarinets'), ('3OBBS', 'Oboes & Bassoons'), ('4SAXS', 'Saxophones'), ('5FRHN', 'French Horns'), ('6TRPT', 'Trumpets'), ('7TRBN', 'Trombones'), ('8EUTB', 'Euphoniums & Tubas & String Basses'), ('9PERC', 'Percussions')], max_length=5)),
                ('is_retired', models.BooleanField(default=False)),
                ('is_on_strength', models.BooleanField(default=False)),
                ('user', models.OneToOneField(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['instrument_section', 'is_retired', '-is_on_strength', '-rank'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rehearsal',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('start_date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RehearsalAttendance',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('status', models.CharField(choices=[('O', 'On-time'), ('L', 'Late'), ('A', 'Absent')], max_length=1)),
                ('reason', models.TextField(blank=True, null=True)),
                ('job', models.ForeignKey(to='attendance.Rehearsal')),
                ('musician', models.ForeignKey(to='attendance.Musician', related_name='rehearsalattendance_attendance')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Uniform',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
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
            model_name='rehearsal',
            name='musicians_attending',
            field=models.ManyToManyField(to='attendance.Musician', related_name='rehearsals_attending', through='attendance.RehearsalAttendance'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='leave',
            name='musician',
            field=models.ForeignKey(to='attendance.Musician'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gigattendance',
            name='musician',
            field=models.ForeignKey(to='attendance.Musician', related_name='gigattendance_attendance'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gig',
            name='musicians_attending',
            field=models.ManyToManyField(to='attendance.Musician', related_name='gigs_attending', through='attendance.GigAttendance'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gig',
            name='musicians_contacted',
            field=models.ManyToManyField(to='attendance.Musician', related_name='contacted', through='attendance.BookingRecord'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gig',
            name='uniform',
            field=models.ForeignKey(blank=True, default=None, to='attendance.Uniform', null=True),
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
            field=models.ForeignKey(to='attendance.Musician', related_name='booking'),
            preserve_default=True,
        ),
    ]
