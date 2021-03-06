# Generated by Django 2.0.10 on 2019-02-20 17:24
import re
from enum import Enum
from pprint import pprint

from django.db import migrations

import logging

from urllib3.util import parse_url

logger = logging.getLogger(__name__)


class Match:
    @classmethod
    def always(cls):
        return cls(True)

    @classmethod
    def never(cls):
        return cls(False)

    def __init__(self, value):
        self.value = value

    def match(self, string):
        return self.value

    def __bool__(self):
        return self.value


def patterns_with_matchers(model):
    qs = model.objects.exclude(regex_host_matcher='', regex_path_matcher='')
    patterns = list(qs)
    for pattern in patterns:
        pattern.host_matcher = re.compile(pattern.regex_host_matcher) if pattern.regex_host_matcher else Match.always()
        pattern.path_matcher = re.compile(pattern.regex_path_matcher) if pattern.regex_path_matcher else Match.always()
    return patterns


def categorize_url(url, patterns, fallback_category):
    parsed_url = parse_url(url)
    host = parsed_url.host
    path = parsed_url.path

    for pattern in patterns:
        host_matcher = pattern.host_matcher
        path_matcher = pattern.path_matcher

        if host_matcher.match(host) and path_matcher.match(path):
            logger.info('Categorized url %s as %s', url, pattern.category)
            return pattern.category
    logger.info('Categorized url %s as %s', url, fallback_category)
    return fallback_category


def migrate_categories(apps, schema_editor):
    CodeArchiveUrl = apps.get_model('citation', 'CodeArchiveUrl')
    CodeArchiveUrlCategory = apps.get_model('citation', 'CodeArchiveUrlCategory')
    CodeArchiveUrlPattern = apps.get_model('citation', 'CodeArchiveUrlPattern')

    old_to_new_category = {'JOURNAL': CodeArchiveUrlCategory.objects.get(category='Journal'),
                           'COMSES': CodeArchiveUrlCategory.objects.get(subcategory='CoMSES')}

    patterns = patterns_with_matchers(CodeArchiveUrlPattern)
    unknown = CodeArchiveUrlCategory.objects.get(category='Unknown')

    code_archive_url_categories = CodeArchiveUrlCategory.objects.all()
    category_model_natural_key_to_pk = {}
    for category in code_archive_url_categories:
        category_model_natural_key_to_pk[(category.category, category.subcategory)] = category.pk
    pprint(category_model_natural_key_to_pk)

    code_archive_urls = CodeArchiveUrl.objects.filter(category_model__isnull=True).exclude(category='')
    for code_archive_url in code_archive_urls:
        if code_archive_url.category in old_to_new_category:
            new_category = old_to_new_category[code_archive_url.category]
        else:
            new_category = categorize_url(code_archive_url.url, patterns, unknown)

        logger.info('migrating category old: %s, new: %s,', code_archive_url.category,
                    (new_category.category, new_category.subcategory))
        code_archive_url.system_overridable_category = False
        code_archive_url.category_model = new_category
        code_archive_url.save()
    CodeArchiveUrl.objects.filter(category='').update(category_model=unknown)


class Migration(migrations.Migration):
    dependencies = [
        ('citation', '0024_codearchiveurl_category_model'),
    ]

    operations = [
        migrations.RunPython(code=migrate_categories)
    ]
