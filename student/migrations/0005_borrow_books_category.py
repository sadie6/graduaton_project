# Generated by Django 2.0.7 on 2019-01-14 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_remove_student_info__class'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrow_books',
            name='category',
            field=models.CharField(default='null', max_length=30),
            preserve_default=False,
        ),
    ]
