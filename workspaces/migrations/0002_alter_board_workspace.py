# Generated by Django 4.1.3 on 2022-11-19 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='workspace',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boards', to='workspaces.workspace'),
        ),
    ]
