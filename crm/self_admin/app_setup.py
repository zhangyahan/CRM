from django import conf


def self_admin_auth_discover():
    for app_name in conf.settings.INSTALLED_APPS:
        try:
            md = __import__('{}.self_admin'.format(app_name))
            print(md.self_admin)
        except ImportError:
            pass
