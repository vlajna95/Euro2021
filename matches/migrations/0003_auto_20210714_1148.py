# Generated by Django 3.2.4 on 2021-07-14 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0002_remove_team_thumbnail'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['pk'], 'verbose_name': 'Grupa', 'verbose_name_plural': 'Grupe'},
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ['group', '-points', '-goals_scored', 'goals_received', 'name'], 'verbose_name': 'Tim', 'verbose_name_plural': 'Timovi'},
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Tim'),
        ),
    ]
