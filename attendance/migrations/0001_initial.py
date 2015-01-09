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
            name='ActiveRoster',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('date', models.DateField(unique_for_year=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AttendanceRecord',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(default=None, blank=True)),
                ('call_time', models.TimeField(blank=True, null=True)),
                ('location', models.CharField(max_length=50)),
                ('job_type', models.IntegerField(choices=[(0, 'Rehearsal'), (1, 'Parade'), (2, 'Concert')], default=0)),
                ('attendance_record', models.OneToOneField(to='attendance.AttendanceRecord', blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Musician',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
            name='Roster',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('musicians_booked', models.ManyToManyField(default=None, blank=True, null=True, to='attendance.Musician')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Uniform',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
            model_name='job',
            name='roster',
            field=models.OneToOneField(to='attendance.Roster', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='uniform',
            field=models.ForeignKey(default=None, to='attendance.Uniform', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attendancerecord',
            name='musicians_present',
            field=models.ManyToManyField(to='attendance.Musician', default=None, null=True, related_name='present'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activeroster',
            name='musicians_active',
            field=models.ManyToManyField(to='attendance.Musician', default=None, null=True, related_name='active'),
            preserve_default=True,
        ),
    ]
