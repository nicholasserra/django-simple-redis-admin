import django


def get_library():
    if django.VERSION >= (1, 9):
        from django.template.library import Library
    else:
        from django.template.base import Library
    return Library


if django.VERSION < (1, 5):
    from django.templatetags.future import url
else:
    from django.template.defaulttags import url
