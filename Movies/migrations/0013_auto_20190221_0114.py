# Generated by Django 2.1.5 on 2019-02-20 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movies', '0012_auto_20160726_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='Poster',
            field=models.FileField(upload_to=''),
        ),
    ]
