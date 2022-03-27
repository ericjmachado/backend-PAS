import csv
import os

from django.conf import settings
from django.views.generic import TemplateView


class EmpresaView(TemplateView):
    template_name = "empresa.html"

    def get_context_data(self, **kwargs):
        context = super(EmpresaView, self).get_context_data(**kwargs)
        empresas = []
        empresa_csv_path = os.path.join(
            settings.BASE_DIR, "core", "data", "empresas_egressos.csv"
        )
        file = open(empresa_csv_path, "r")
        empresas_csv = csv.DictReader(file)
        for empresa in empresas_csv:
            empresas.append(empresa)
        file.close()
        funcionarios_empresas = {
            empresa.get("razao_social"): int(empresa.get("empregados", 0))
            if empresa.get("empregados", 0)
            else 0
            for empresa in empresas
        }
        context["empresas"] = empresas
        context["funcionarios_empresas"] = funcionarios_empresas
        return context
