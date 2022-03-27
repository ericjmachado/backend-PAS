from django.core.paginator import Paginator
from django.views.generic import TemplateView

from core.models import Projeto


class ProjetoView(TemplateView):
    template_name = "projeto.html"

    def get_context_data(self, **kwargs):
        context = super(ProjetoView, self).get_context_data(**kwargs)
        projeto = Projeto.objects.all()
        paginator = Paginator(
            projeto, self.request.GET.get("limit", 100)
        )
        page_number = self.request.GET.get("page")
        context["projetos"] = paginator.get_page(page_number)
        return context
