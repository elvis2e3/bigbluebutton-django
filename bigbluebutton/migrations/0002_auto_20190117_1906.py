# Generated by Django 2.1.5 on 2019-01-17 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bigbluebutton', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bbbmeeting',
            old_name='attendee_pw',
            new_name='attendeePW',
        ),
        migrations.RenameField(
            model_name='bbbmeeting',
            old_name='meeting_id',
            new_name='meetingID',
        ),
        migrations.RenameField(
            model_name='bbbmeeting',
            old_name='moderator_pw',
            new_name='moderatorPW',
        ),
    ]
