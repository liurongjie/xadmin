# Generated by Django 2.0.9 on 2019-04-16 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dajia', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order', to='dajia.Comment'),
        ),
    ]
