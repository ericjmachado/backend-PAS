from django.views.generic import TemplateView
import pandas as pd
from django.conf import settings
import os

from core.helpers import humanizar_ano, dict_float_to_percent


class CursoView(TemplateView):
    template_name = "curso.html"

    def get_context_data(self, **kwargs):
        context = super(CursoView, self).get_context_data(**kwargs)
        context["cursos"] = self.get_dados_estatisticos()
        return context

    def get_dados_estatisticos(self):
        data = []
        df = pd.read_csv(
            os.path.join(settings.BASE_DIR, "core", "data", "relacao_estudante.csv")
        )
        for chave, curso_df in df.groupby("curso"):
            media = float(
                curso_df["media_global"]
                .replace(",", ".", regex=True)
                .astype(float)
                .mean(skipna=True)
            )
            cdfg = curso_df[curso_df.status == "Graduado"]
            ano_ingresso, semestre_ingresso, ano_desvinculo, semestre_desvinculo = cdfg[
                [
                    "ano_ingresso",
                    "semestre_ingresso",
                    "ano_desvinculo",
                    "semestro_desvinculo",
                ]
            ].mean()
            ano_resultado = (
                ano_desvinculo
                - ano_ingresso
                + ((semestre_desvinculo - semestre_ingresso) / 2)
            )
            ano_resultado = humanizar_ano(ano_resultado)
            sexos = curso_df["sexo"].value_counts(normalize=True)
            desvinculo = curso_df["motivo_desvinculo"].value_counts(normalize=True)
            cotas = curso_df["lei_cotas"].value_counts(normalize=True)
            data.append(
                {
                    "nome": chave,
                    "media": media,
                    "tempo_medio_desvinculo": ano_resultado,
                    "sexo": dict_float_to_percent(sexos.to_dict()),
                    "desvinculo": dict_float_to_percent(desvinculo.to_dict()),
                    "cotas": dict_float_to_percent(cotas.to_dict()),
                }
            )
        return data
