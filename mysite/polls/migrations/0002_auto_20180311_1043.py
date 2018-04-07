# Generated by Django 2.0.3 on 2018-03-11 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=200)),
                ('inputText', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SimResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outputText', models.TextField()),
                ('outputURL', models.SlugField(max_length=100)),
                ('query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Query')),
            ],
        ),
        migrations.AddField(
            model_name='choice',
            name='input_text',
            field=models.TextField(default='default'),
            preserve_default=False,
        ),
    ]