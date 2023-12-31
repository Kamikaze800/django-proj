# Generated by Django 4.2.1 on 2023-06-02 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20230525_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='venue',
            field=models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.CASCADE, to='events.venue'),
        ),
        migrations.AlterField(
            model_name='myclubuser',
            name='firstName',
            field=models.CharField(max_length=200, verbose_name='firstName'),
        ),
        migrations.AlterField(
            model_name='myclubuser',
            name='secondName',
            field=models.CharField(blank=True, max_length=200, verbose_name='secondName'),
        ),
    ]
