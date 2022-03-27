from django.views.generic import TemplateView
from django.conf import settings
import pandas as pd
import os


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["dados"] = self.get_dados_estatisticos()
        return context

    def get_dados_estatisticos(self):
        data = {}
        df = pd.read_csv(os.path.join(settings.BASE_DIR, "core", "data", "relacao_estudante.csv"))
        ingressos_totais = df.groupby("ano_ingresso").size().to_dict()
        ingressos_por_unidade = df.groupby(["ano_ingresso", "unidade"]).size().to_dict()
        df_egressos = df[df.status == "Graduado"]
        egressos_totais = df_egressos.groupby("ano_desvinculo").size().to_dict()
        egressos_por_unidade = df_egressos.groupby(["ano_desvinculo", "unidade"]).size().to_dict()
        data["ingressos_totais"] = ingressos_totais
        data["ingressos_por_unidade"] = self._tratar_dados_por_unidade(ingressos_por_unidade)

        data["egressos_totais"] = egressos_totais
        data["egressos_por_unidade"] = self._tratar_dados_por_unidade(egressos_por_unidade)
        return data

    def _tratar_dados_por_unidade(self, dados):
        data = {}
        anos = list(set([buff[0] for buff in list(dados.keys())]))
        anos.sort()
        unidades = list(set([buff[1] for buff in list(dados.keys())]))
        unidades.sort()
        for unidade in unidades:
            unidade_data = {}
            for ano in anos:
                unidade_data[ano] = dados.get((ano, unidade), 0)
            data[unidade] = unidade_data
        return data