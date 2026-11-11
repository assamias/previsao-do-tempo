import logging
import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory

load_dotenv()

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
DIST_DIR = BASE_DIR / "frontend" / "dist"

app = Flask(__name__)

API_KEY = os.environ.get("OPENWEATHER_API_KEY")
URL_CLIMA = "https://api.openweathermap.org/data/2.5/weather"
TIMEOUT_SEGUNDOS = 10

if not API_KEY:
    log.warning("OPENWEATHER_API_KEY não está definida. As buscas vão falhar.")

TEMAS = {
    "Clear": "sol",
    "Clouds": "nublado",
    "Rain": "chuva",
    "Drizzle": "chuva",
    "Thunderstorm": "tempestade",
    "Snow": "neve",
}


def montar_clima(dados):
    """Converte o JSON da OpenWeatherMap no formato usado pelo front."""
    clima_atual = dados["weather"][0]
    return {
        "nome": dados["name"],
        "pais": dados["sys"]["country"],
        "temperatura": round(dados["main"]["temp"]),
        "sensacao": round(dados["main"]["feels_like"]),
        "umidade": dados["main"]["humidity"],
        "pressao": dados["main"]["pressure"],
        "vento": round(dados["wind"]["speed"] * 3.6),
        "descricao": clima_atual["description"].capitalize(),
        "icone": clima_atual["icon"],
        "tema": TEMAS.get(clima_atual["main"], "neutro"),
    }


def buscar_clima(cidade):
    """Retorna (clima, erro, status_http)."""
    if not API_KEY:
        return None, "Erro de configuração no servidor.", 500

    try:
        resposta = requests.get(
            URL_CLIMA,
            params={"q": cidade, "appid": API_KEY, "lang": "pt_br", "units": "metric"},
            timeout=TIMEOUT_SEGUNDOS,
        )
    except requests.RequestException:
        log.exception("Falha de conexão com a OpenWeatherMap")
        return None, "Não foi possível conectar ao serviço de clima.", 503

    if resposta.status_code == 200:
        try:
            return montar_clima(resposta.json()), None, 200
        except (KeyError, IndexError, TypeError, ValueError):
            log.exception("Formato inesperado na resposta da OpenWeatherMap")
            return None, "O serviço de clima devolveu uma resposta inesperada.", 502

    if resposta.status_code == 401:
        # Problema de configuração do servidor, não de quem fez a busca
        log.error("OpenWeatherMap recusou a chave (401)")
        return None, "Erro de configuração no servidor.", 500

    if resposta.status_code == 404:
        return None, "Cidade não encontrada. Verifique se o nome está correto.", 404

    log.error("OpenWeatherMap respondeu com status %s", resposta.status_code)
    return None, "O serviço de clima está indisponível no momento.", 502


@app.route("/api/clima")
def api_clima():
    cidade = request.args.get("cidade", "").strip()
    if not cidade:
        return jsonify({"erro": "Digite o nome de uma cidade."}), 400

    clima, erro, status = buscar_clima(cidade)
    if erro:
        return jsonify({"erro": erro}), status
    return jsonify(clima), 200


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/", defaults={"caminho": ""})
@app.route("/<path:caminho>")
def frontend(caminho):
    """Em produção, entrega o build do React. Em dev, o Vite cuida disso."""
    if caminho and (DIST_DIR / caminho).is_file():
        return send_from_directory(DIST_DIR, caminho)
    if (DIST_DIR / "index.html").is_file():
        return send_from_directory(DIST_DIR, "index.html")
    return jsonify({"status": "API no ar. Rode 'npm run build' em frontend/ para ver a interface."})


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")