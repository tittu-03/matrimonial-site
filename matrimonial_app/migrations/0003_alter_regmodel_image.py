# Generated by Django 4.0.5 on 2022-08-23 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimonial_app', '0002_rename_photo_regmodel_image_regmodel_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regmodel',
            name='image',
            field=models.ImageField(upload_to='matrimonial_app/static'),
        ),
    ]
