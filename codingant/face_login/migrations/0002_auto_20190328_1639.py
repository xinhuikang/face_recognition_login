# Generated by Django 2.1 on 2019-03-28 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face_login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faces',
            name='face_encode',
            field=models.FileField(upload_to=''),
        ),
    ]
