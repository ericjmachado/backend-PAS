from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import TemplateView

from core.models import Projeto
from core.helpers import get_word_clouds


class ProjetoView(TemplateView):
    template_name = "projeto.html"

    def get_context_data(self, **kwargs):
        context = super(ProjetoView, self).get_context_data(**kwargs)
        projeto = Projeto.objects.all()
        params = self.request.GET
        busca = params.get("busca")
        if params.get("unidade"):
            projeto = projeto.filter(sigla_unidade_projeto=params.get("unidade"))

        if params.get("tipo"):
            projeto = projeto.filter(tipo_projeto=params.get("tipo"))
        if busca:
            projeto = projeto.filter(
                Q(titulo_projeto__icontains=busca) | Q(resumo_projeto__icontains=busca)
            )
        limit = params.get("limit", 100)
        paginator = Paginator(projeto, limit)
        page_number = params.get("page")
        page = paginator.get_page(page_number)
        context["projetos"] = page
        ids = [obj.pk for obj in page.object_list]
        projetos = Projeto.objects.filter(pk__in=ids)
        context["wordcloud"] = get_word_clouds(projetos, 100)
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
