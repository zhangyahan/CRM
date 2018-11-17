import datetime
import time

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def render_app_name(admin_class):
    return admin_class.model._meta.verbose_name


@register.simple_tag
def get_query_sets(admin_class):
    return admin_class.model.objects.all()


@register.simple_tag
def build_table_row(obj, admin_class):
    row_ele = ''
    for column in admin_class.list_display:
        field_obj = obj._meta.get_field(column)
        if field_obj.choices:
            column_data = getattr(obj, 'get_{}_display'.format(column))()
            row_ele += "<td>{}".format(column_data)
        else:
            column_data = getattr(obj, column)
            row_ele += "<td>{}".format(column_data)
    return mark_safe(row_ele)


@register.simple_tag
def build_filter_ele(filter_column, admin_class):
    column_obj = admin_class.model._meta.get_field(filter_column)
    try:
        filter_ele = '<select name="%s">' % filter_column
        for choice in column_obj.get_choices():
            selected = ''
            if filter_column in admin_class.filter_conditions:
                if str(choice[0]) == admin_class.filter_conditions.get(filter_column):
                    selected = 'selected'
            option = '<option value="%s" %s>%s</option>' % (choice[0], selected, choice[1])
            filter_ele += option
    except AttributeError as a:
        filter_ele = '<select name="%s__gte">' % filter_column
        if column_obj.get_internal_type() in ('DateField', 'DateTimeField'):
            time_obj = datetime.datetime.now()
            time_list = [
                ['', '------------'],
                [time_obj, 'Today'],
                [time_obj - datetime.timedelta(7), '七天内'],
                [time_obj.replace(day=1), '本月'],
                [time_obj - datetime.timedelta(90), '三个月内'],
                [time_obj.replace(month=1, day=1), 'YearToday(YTD)'],
                ['', 'ALL'],
            ]

            for i in time_list:
                selected = ''
                time_to_str = '' if not i[0] else '%s-%s-%s' % (i[0].year, i[0].month, i[0].day)
                if "%s__gte" % filter_column in admin_class.filter_conditions:
                    if time_to_str == admin_class.filter_conditions.get("%s__gte" % filter_column):
                        selected = 'selected'
                option = '<option value="%s" %s>%s</option>' % (time_to_str,
                                                                selected,
                                                                i[1])
                filter_ele += option

    filter_ele += "</select>"
    return mark_safe(filter_ele)


