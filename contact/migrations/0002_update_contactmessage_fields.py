from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactmessage',
            name='name',
        ),
        migrations.RemoveField(
            model_name='contactmessage',
            name='subject',
        ),
        migrations.AddField(
            model_name='contactmessage',
            name='first_name',
            field=models.CharField(default='', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contactmessage',
            name='last_name',
            field=models.CharField(default='', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contactmessage',
            name='phone_number',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
