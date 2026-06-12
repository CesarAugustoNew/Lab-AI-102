import json
from flask import Flask, render_template, request, jsonify
from openai import AzureOpenAI

app = Flask(__name__)

# =========================
# AZURE OPENAI CONFIG
# =========================
endpoint = ""
api_key = ""
deployment = "gpt-4o"


client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-02-15-preview"
)

# =========================
# PROMPT CHEF (ESTRUTURA IA)
# =========================
prompt_chef = """
Você é um Chef Executivo especialista em gastronomia.

Sua missão é criar receitas profissionais e identificar falhas na execução.

Retorne EXCLUSIVAMENTE JSON com:

- score_receita_estimado: 0 a 100
- resumo_receita: texto
- receita_otimizada: { nome_prato, passo_a_passo_chef }
- ingredientes_categorias: { proteinas, carboidratos, temperos, outros }
- tecnicas_necessarias: []
- erros_comuns: []
- perguntas_investigativas: []
- feedback_final: texto
"""

# =========================
# FRONTEND
# =========================
@app.route("/")
def home():
    return render_template("index.html")

# =========================
# API - GERAR RECEITA (FASE 1)
# =========================
@app.route("/receita", methods=["POST"])
def gerar_receita():

    data = request.get_json()

    ingredientes = data.get("ingredientes", "")
    equipamentos = data.get("equipamentos", "")
    nivel = data.get("nivel", "")

    prompt = f"""
Ingredientes: {ingredientes}
Equipamentos: {equipamentos}
Nível: {nivel}
"""

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": prompt_chef},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.6
    )

    return jsonify(json.loads(response.choices[0].message.content))


# =========================
# API - REFINAR RECEITA (FASE 2)
# =========================
@app.route("/refinar", methods=["POST"])
def refinar():

    data = request.get_json()

    receita = data.get("receita", {})
    respostas = data.get("respostas", "")

    prompt = f"""
Receita original:
{json.dumps(receita, ensure_ascii=False)}

Respostas do usuário:
{respostas}
"""

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": prompt_chef},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.3
    )

    return jsonify(json.loads(response.choices[0].message.content))


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    print("🔥 Chef AI rodando em http://127.0.0.1:5000")
    app.run(debug=True)