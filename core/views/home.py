from django.views.generic import TemplateView
from django.conf import settings


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["token"] = settings.BEARER_TOKEN
        return context
