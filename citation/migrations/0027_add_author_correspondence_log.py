# Generated by Django 2.1.8 on 2019-04-05 22:30

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('citation', '0026_replace_string_category_with_foreign_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorCorrespondenceLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_responded', models.DateTimeField(null=True)),
                ('status', models.CharField(choices=[('NOT_AVAILABLE', 'Code not available'), ('NOT_IN_ARCHIVE', 'Code has a currently active URL but not in a trusted digital repository'), ('ARCHIVED', 'Code available in archive')], max_length=64)),
                ('content', models.TextField(blank=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('email_delivery_status', models.CharField(max_length=50)),
                ('publication', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='citation.Publication')),
            ],
        ),
        migrations.RemoveField(
            model_name='authorcorrespondence',
            name='author',
        ),
        migrations.RemoveField(
            model_name='authorcorrespondence',
            name='template',
        ),
        migrations.DeleteModel(
            name='AuthorCorrespondence',
        ),
        migrations.DeleteModel(
            name='AuthorCorrespondenceTemplate',
        ),
    ]
