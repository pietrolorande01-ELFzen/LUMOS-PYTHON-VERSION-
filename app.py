# ==========================================================
# LUMOS — API FLASK (Sprint 4)
# ----------------------------------------------------------
# Ponte entre a interface Web (pasta site/) e o backend Python
# (SPRINT_DSA_Completa.py). Toda regra de negocio, armazenamento,
# busca, ordenacao e estatistica acontece em Python.
#
#   Interface Web  --fetch-->  app.py (rota)  -->  funcao Python
#                  <--JSON---                  <--  resultado
#
# Como rodar:   pip install flask
#               python app.py
#               abra http://localhost:5000
# ==========================================================

import os
import time
import random
from datetime import datetime, timedelta

from flask import Flask, jsonify, request, send_file, send_from_directory

import SPRINT_DSA_Completa as lumos

PASTA_SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
app = Flask(__name__, static_folder=PASTA_SITE, static_url_path="")

# Lista em memoria com todas as sessoes (a mesma estrutura do terminal).
# Carregada do JSON ao iniciar e salva a cada alteracao.
sessoes = lumos.carregar_sessoes()

# Mapeia o nome do pagamento usado no site para o codigo do Python.
PAGAMENTO_SITE = {"pix": "1", "boleto": "2", "tag": "3", "cartao": "4", "creditos": "5"}

CRITERIOS = {"id", "energia_kwh", "valor_total", "duracao_min"}


def log(msg):
    """Mostra no terminal o que o backend esta fazendo (bom para o video)."""
    print(f"[LUMOS API][{lumos.ts()}] {msg}", flush=True)


def resumo(s):
    """Campos que a interface precisa para listar uma sessao."""
    return {k: s.get(k) for k in (
        "id", "usuario", "data", "inicio", "fim", "duracao_min", "marca_carro",
        "bateria_inicial", "bateria_final", "bateria_lynx", "fonte", "bandeira",
        "potencia_kw", "energia_kwh", "tarifa", "taxa_fixa", "valor_energia",
        "valor_total", "co2_evitado_kg", "pagamento_nome", "avisos")}


# ---------------------------- PAGINAS ----------------------------

@app.route("/")
def raiz():
    return send_from_directory(PASTA_SITE, "index.html")


# ---------------------------- SESSOES ----------------------------

@app.get("/api/sessoes")
def listar_sessoes():
    """Listagem: devolve a lista de sessoes como esta guardada em Python."""
    log(f"GET /api/sessoes -> {len(sessoes)} sessoes")
    return jsonify([resumo(s) for s in sessoes])


@app.post("/api/sessoes")
def nova_sessao():
    """Cadastro: o site envia os dados, o Python calcula tudo e guarda."""
    d = request.get_json(silent=True) or {}
    try:
        sessao = lumos.criar_sessao(
            sessoes,
            usuario=d.get("usuario"),
            token=d.get("token", ""),
            marca_carro=d.get("veiculo", "BYD Dolphin"),
            pagamento=PAGAMENTO_SITE.get(d.get("pagamento"), "1"),
            bateria_inicial=d.get("bateria_inicial"),
        )
    except ValueError as erro:
        log(f"POST /api/sessoes -> erro de validacao: {erro}")
        return jsonify({"erro": str(erro)}), 400

    lumos.salvar_sessoes(sessoes)
    log(f"POST /api/sessoes -> {sessao['id']} criada | {sessao['energia_kwh']} kWh "
        f"x R$ {sessao['tarifa']}/kWh + R$ {sessao['taxa_fixa']} = R$ {sessao['valor_total']} "
        f"({sessao['bandeira']}, Lynx {sessao['bateria_lynx']}%)")
    return jsonify(resumo(sessao)), 201


@app.get("/api/sessoes/busca")
def buscar():
    """Busca por ID usando busca sequencial (O(n)) ou binaria (O(log n))."""
    id_procurado = request.args.get("id", "").strip()
    algoritmo = request.args.get("algoritmo", "sequencial")
    if not id_procurado:
        return jsonify({"erro": "Informe o ID da sessao."}), 400

    contador = {}
    inicio = time.perf_counter()
    if algoritmo == "binaria":
        lista, ordenou = lumos.preparar_busca_binaria(sessoes, contador)
        idx = lumos.busca_binaria(lista, id_procurado, contador)
        nome, big_o = "Busca binária", "O(log n)"
    else:
        lista, ordenou = sessoes, False
        idx = lumos.busca_sequencial(lista, id_procurado, contador)
        nome, big_o = "Busca sequencial", "O(n)"
    ms = (time.perf_counter() - inicio) * 1000

    log(f"GET /api/sessoes/busca -> {nome} por '{id_procurado}' | n={len(sessoes)} | "
        f"{contador.get('comparacoes', 0)} comparacoes | {'achou' if idx != -1 else 'nao achou'}")
    return jsonify({
        "algoritmo": nome, "complexidade": big_o, "n": len(sessoes),
        "comparacoes": contador.get("comparacoes", 0),
        "verificacoes_ordem": contador.get("verificacoes", 0),
        "precisou_ordenar": ordenou,
        "tempo_ms": round(ms, 3),
        "encontrada": idx != -1,
        "sessao": resumo(lista[idx]) if idx != -1 else None,
    })


@app.get("/api/sessoes/ordenar")
def ordenar():
    """Ordena uma copia da lista com Bubble Sort ou Merge Sort."""
    criterio = request.args.get("criterio", "energia_kwh")
    decrescente = request.args.get("ordem", "asc") == "desc"
    alg = request.args.get("algoritmo", "bubble")
    if criterio not in CRITERIOS or alg not in lumos.ALGORITMOS_ORDENACAO:
        return jsonify({"erro": "Criterio ou algoritmo invalido."}), 400

    funcao, nome, big_o = lumos.ALGORITMOS_ORDENACAO[alg]
    copia = sessoes[:]          # a lista original continua em ordem de cadastro
    contador = {}
    inicio = time.perf_counter()
    funcao(copia, criterio, decrescente, contador)
    ms = (time.perf_counter() - inicio) * 1000

    log(f"GET /api/sessoes/ordenar -> {nome} por {criterio} "
        f"({'desc' if decrescente else 'asc'}) | n={len(copia)} | "
        f"{contador.get('comparacoes', 0)} comparacoes")
    return jsonify({
        "algoritmo": nome, "complexidade": big_o, "criterio": criterio,
        "decrescente": decrescente, "n": len(copia),
        "comparacoes": contador.get("comparacoes", 0),
        "trocas": contador.get("trocas", 0),
        "tempo_ms": round(ms, 3),
        "sessoes": [resumo(s) for s in copia],
    })


# ------------------------ ESTATISTICAS / RELATORIO ------------------------

@app.get("/api/estatisticas")
def estatisticas():
    log("GET /api/estatisticas")
    return jsonify(lumos.calcular_estatisticas(sessoes))


@app.get("/api/relatorio.txt")
def relatorio_txt():
    """Gera o relatorio .txt com a mesma funcao do terminal e envia o arquivo."""
    if not sessoes:
        return jsonify({"erro": "Nenhuma sessao para exportar."}), 400
    log("GET /api/relatorio.txt -> gerando relatorio")
    nome = lumos.exportar_relatorio_txt(sessoes)
    return send_file(os.path.abspath(nome), as_attachment=True)


# ------------------------ DADOS DE DEMONSTRACAO ------------------------

@app.post("/api/sessoes/gerar")
def gerar_teste():
    """
    Cria N sessoes ficticias para demonstrar, no video, como o numero
    de operacoes cresce quando n aumenta.
    """
    qtd = max(1, min(int((request.get_json(silent=True) or {}).get("quantidade", 20)), 2000))
    nomes = ["Ana", "Gustavo", "Julian", "Marcelo", "Maria", "Pietro", "Lucas", "Bia"]
    carros = ["BYD Dolphin", "Tesla Model 3", "Volvo XC40", "BMW iX3", "Renault Kwid E-Tech"]
    base = datetime.now() - timedelta(days=qtd)
    for i in range(qtd):
        lumos.criar_sessao(
            sessoes, usuario=random.choice(nomes), token=f"{random.randint(0, 999999):06d}",
            marca_carro=random.choice(carros), pagamento=random.choice(["1", "2", "3", "4", "5"]),
            duracao_min=random.randint(10, 90),
            momento=base + timedelta(days=i, hours=random.randint(0, 23)),
        )
    lumos.salvar_sessoes(sessoes)
    log(f"POST /api/sessoes/gerar -> +{qtd} sessoes de teste (total {len(sessoes)})")
    return jsonify({"criadas": qtd, "total": len(sessoes)})


@app.delete("/api/sessoes")
def limpar():
    sessoes.clear()
    lumos.salvar_sessoes(sessoes)
    log("DELETE /api/sessoes -> lista zerada")
    return jsonify({"total": 0})


if __name__ == "__main__":
    print("=" * 60)
    print("  LUMOS — backend Python rodando")
    print("  Abra no navegador: http://localhost:5000")
    print(f"  Sessoes carregadas do JSON: {len(sessoes)}")
    print("=" * 60)
    app.run(debug=False, port=5000)
