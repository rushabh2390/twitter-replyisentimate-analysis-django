# Generated by Django 3.2.13 on 2022-06-30 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweetsreplyanalysis', '0002_rename_twitter_negective_percentage_twitterdata_twitter_negative_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitterdata',
            name='analysis_updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]