# Generated by Django 2.0.7 on 2019-01-14 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_student_info_educational_history'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student_info',
            name='_class',
        ),
    ]