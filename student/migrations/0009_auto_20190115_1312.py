# Generated by Django 2.0.7 on 2019-01-15 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_remove_student_grade_grade_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internet_data',
            name='exit_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='internet_data',
            name='login_time',
            field=models.DateTimeField(),
        ),
    ]
