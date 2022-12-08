# Generated by Django 4.1.3 on 2022-12-08 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0021_alter_tasklist_board'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='board',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='labels', to='workspaces.board'),
        ),
    ]
