# Generated by Django 3.2.16 on 2023-05-26 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizcreation',
            name='status',
            field=models.CharField(blank=True, choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Finished', 'Finished')], max_length=25, null=True),
        ),
    ]
