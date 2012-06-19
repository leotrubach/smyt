from django.db import models
from django.conf import settings
from django.contrib import admin
import yaml
from os.path import dirname, abspath, join


FIELD_TYPE_CLASSES = {
    'int': (models.IntegerField, {}),
    'char': (models.CharField, {'max_length': 50}),
    'date': (models.DateField, {}),
    'datetime': (models.DateTimeField, {})
}

def generate_field(field_scheme):
    type = field_scheme['type']
    field_class, kwargs = FIELD_TYPE_CLASSES[type]
    if 'title' in field_scheme:
        kwargs['verbose_name'] = field_scheme['title']
    return field_scheme['id'], field_class(**kwargs)

def generate_model(model_name, model_settings):

    class Meta:
        pass

    if 'title' in model_settings:
        Meta.verbose_name = model_settings['title']

    kwargs = {'Meta': Meta, '__module__': generate_model.__module__}
    fields = dict([generate_field(f)
                   for f in model_settings['fields']])
    kwargs.update(fields)
    return type(model_name, (models.Model,), kwargs)


def load_scheme():
    dyn_vars = globals()
    scheme_file = join(dirname(abspath(__file__)), settings.MODEL_SCHEME)
    scheme = yaml.load(open(scheme_file).read())

    for lower_model_name, model_settings in scheme.iteritems():
        model_name = lower_model_name[:1].upper() + lower_model_name[1:]
        model_class = generate_model(model_name, model_settings)
        dyn_vars[model_name] = model_class
        admin.site.register(model_class)

load_scheme()
