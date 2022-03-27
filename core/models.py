from django.db import models


class Projeto(models.Model):
    id = models.AutoField(primary_key=True)
    idProjeto = models.IntegerField(null=True)
    tipo_projeto = models.CharField(max_length=50)
    titulo_projeto = models.TextField()
    id_unidade_projeto = models.IntegerField(null=True)
    sigla_unidade_projeto = models.CharField(max_length=50)
    nome_unidade_projeto = models.CharField(max_length=255)
    coordenacao_projeto = models.CharField(max_length=255)
    resumo_projeto = models.TextField()
