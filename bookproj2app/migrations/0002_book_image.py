# Generated by Django 4.2.16 on 2024-09-19 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookproj2app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(default=1234, upload_to='book_media'),
            preserve_default=False,
        ),
    ]
