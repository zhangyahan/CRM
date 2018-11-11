from django import template

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
        column_data = getattr(obj, column)
        row_ele += "<td>{}<td>".format(column_data)
    pass