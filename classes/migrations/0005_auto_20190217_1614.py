# Generated by Django 2.1.5 on 2019-02-17 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0004_auto_20190217_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='date_of_birth',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('GENDER', 'Gender'), ('MALE', 'Male'), ('FEMALE', 'Female')], default='GENDER', max_length=6),
        ),
    ]
