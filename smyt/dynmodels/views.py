import json
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.db.models import get_models
from django.contrib.contenttypes.models import ContentType


class HomeView(TemplateView):
    template_name = 'home.html'

def list_models(request):
    models = [['%s.%s' % (m._meta.app_label, m.__name__),
               unicode(m._meta.verbose_name)]
               for m in get_models()
               if m._meta.app_label == 'dynmodels']
    return HttpResponse(
            json.dumps(models),
            content_type = 'application/javascript; charset=utf8')

def model_data(request):

    if request.method == 'GET':
        resp_dict = {}
        app_label, model_name = request.GET['id'].split('.')
        model_name = model_name[:1].lower() + model_name[1:]
        model_class = ContentType.objects.get(
            app_label=app_label,
            model=model_name).model_class()

        resp_dict['header'] = [f.verbose_name
                               for f in model_class._meta.fields]
        fields = [f.name for f in model_class._meta.fields]
        instances = model_class.objects.all()
        resp_dict['body'] = [[getattr(i, f) for f in fields] for i in instances]
        return HttpResponse(
                json.dumps(resp_dict),
                content_type = 'application/javascript; charset=utf8')