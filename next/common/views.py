from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'common/index.html'


class ComingSoonView(TemplateView):
    template_name = 'common/coming-soon.html'
