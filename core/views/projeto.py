from django.core.paginator import Paginator
from django.views.generic import TemplateView

from core.models import Projeto


class ProjetoView(TemplateView):
    template_name = "projeto.html"

    def get_context_data(self, **kwargs):
        context = super(ProjetoView, self).get_context_data(**kwargs)
        projeto = Projeto.objects.all()
        params = self.request.GET
        if params.get("unidade"):
            projeto = projeto.filter(sigla_unidade_projeto=params.get("unidade"))

        if params.get("tipo"):
            projeto = projeto.filter(tipo_projeto=params.get("tipo"))
        paginator = Paginator(projeto, params.get("limit", 100))
        page_number = params.get("page")
        context["projetos"] = paginator.get_page(page_number)
        context["tipos_projeto"] = list(
            Projeto.objects.distinct("tipo_projeto").values_list(
                "tipo_projeto", flat=True
            )
        )
        context["unidades_projeto"] = list(
            Projeto.objects.exclude(sigla_unidade_projeto="")
            .distinct("sigla_unidade_projeto")
            .values_list("sigla_unidade_projeto", flat=True)
        )
        return context
