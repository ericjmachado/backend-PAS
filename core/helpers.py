import base64
from django.conf import settings
import requests
from django.utils import timezone
import math
from wordcloud import WordCloud, STOPWORDS


def generate_base64_token(key, password):
    token = base64.b64encode(bytes(f"{key}:{password}", "utf-8")).decode("utf-8")
    return f"Basic {token}"


def get_bearer_token():
    basic = settings.BASIC_TOKEN
    headers = {"Authorization": basic}
    data = {"grant_type": "client_credentials"}
    response = requests.post(
        f"{settings.URL_UFG_API}/token", headers=headers, data=data, verify=False
    )
    token = response.json().get("access_token")
    return f"Bearer {token}"


def get_bearer_token_from_updated():
    def _default_setup():
        settings.BEARER_TOKEN = get_bearer_token()
        settings.BEARER_REFRESH_AT = timezone.now()
        return settings.BEARER_TOKEN

    refreshed_at = settings.BEARER_REFRESH_AT
    if refreshed_at is not None:
        if (timezone.now() - refreshed_at).seconds > 3600:
            return _default_setup()
        else:
            return settings.BEARER_TOKEN
    else:
        return _default_setup()


def humanizar_ano(ano: float):
    if not math.isnan(ano) and ano:
        ano_inteiro = int(ano)
        meses = int((ano - ano_inteiro) * 365 / 30)
        sufixo = ""
        if meses != 0:
            sufixo = f" e {meses} meses"
        return f"{ano_inteiro} anos{sufixo}"
    else:
        return "0 anos"


def dict_float_to_percent(data: dict):
    return {key: value * 100 for key, value in data.items()}


def get_word_clouds(qs, size=None):
    if size is None:
        size = 50
    texto = ""
    dados = list(qs.values_list("titulo_projeto", "resumo_projeto"))
    stop = [
        "e",
        "o",
        "é",
        "ver",
        "principal",
        "essa",
        "vez",
        "nas",
        "mas",
        "qual",
        "principal",
        "ele",
        "ter",
        "doença",
        "pois",
        "este",
        "vez",
        "ver principal",
        "artigo principal",
        "já",
        "aos",
        "pode",
        "outro",
        "artigo",
        "desse",
        "alguns",
        "meio",
        "entre",
        "das",
        "podem",
        "esse",
        "seu",
        "também",
        "são",
        "quando",
        "de",
        "que",
        "em",
        "os",
        "as",
        "da",
        "como",
        "dos",
        "ou",
        "se",
        "um",
        "uma",
        "para",
        "na",
        "ao",
        "mais",
        "por",
        "não",
        "ainda",
        "muito",
        "sua",
        "até",
        "foram",
        "sobre",
        "pelo",
    ] + list(STOPWORDS)
    for titulo, resumo in dados:
        texto = f"{texto} {titulo} {resumo}"

    wordcloud = WordCloud(stopwords=stop, collocations=True)
    dados = list(wordcloud.process_text(texto).items())[:size]
    return [{"name": chave, "weight": peso} for chave, peso in dados]
