from openai import AzureOpenAI
import json

endpoint = ""
api_key = ""
deployment = "gpt-4o"

# Criando a ponte (client) de comunicacao com a nuvem da Azure
ai_client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-02-15-preview"
)

prompt_tutor = """Você é um Instrutor de Treinamento Profissional especialista em Microsoft Azure.
Seu objetivo é ajudar alunos a se prepararem para exames de certificação.
O aluno fornecerá um tema. Você deve gerar um material de estudo rápido e uma questão de múltipla escolha.
Sua abordagem deve ser didática, prática e visual (como um simulador gamificado).

Retorne EXCLUSIVAMENTE em formato JSON com as seguintes chaves:
- "resumo_tema": Uma explicação clara e concisa (máximo 3 linhas) sobre o tema pedido.
- "nivel_dificuldade": "FUNDAMENTOS", "ASSOCIADO" ou "ESPECIALISTA".
- "pergunta": Uma pergunta de múltipla escolha (estilo exame de certificação) sobre o tema.
- "opcoes": Uma lista [Array] contendo 4 alternativas curtas (A, B, C e D).
- "resposta_correta": Apenas a letra da alternativa correta (ex: "B").
- "explicacao_resposta": O motivo técnico detalhado pelo qual essa alternativa é a correta."""

#Motor do Aplicativo

print("================================================")
print("TUTOR INTELIGENTE DE CERTIFICAÇÕES AZURE")
print("Digite 'sair' a qualquer momento para encerrar.")
print("================================================\n")

while True:
  tema_escudo = input("ALUNO, QUAL TEMA VOCÊ QUER ESTUDAR HOJE?(ex: Redes Virtuais): ")

  #Condições de parada
  if tema_escudo.lower().strip() == 'sair':
    print("\nSISTEMA: Sessão de estudos encerrada. Bons estudos!")
    break
  
  #Previne mensagens vazias
  if not tema_escudo.strip():
    continue
  
  print("\n[Tutor gerando material de estudos...]\n")

  try:
    #Envia a solicitção para a Azure
    response = ai_client.chat.completions.create(
        model = deployment,
        messages = [
            {"role": "system", "content": prompt_tutor},
            {"role": "user", "content": f"Quero estudar sobre: {tema_escudo}"}
        ],
        max_tokens=400,
        temperature=0.3,
        response_format={"type":"json_object"}
    )
    #Converte em dicionário python
    dados_estudo = json.loads(response.choices[0].message.content)

    #Exibe informações teoricas
    print("--------------------------------------------------")
    print(f"RESUME RÁPIDO: {dados_estudo.get('resumo_tema')}")
    print(f"NIVEL: {dados_estudo.get('nivel_dificuldade')}")
    print("--------------------------------------------------")

    #Inicia a interface do simulado
    print("DESAFIO PRATICO:")
    print(dados_estudo.get('pergunta'))

    #Imprimir as alternativas
    opcoes = dados_estudo.get('opcoes', [])
    for opcao in opcoes:
      print(f" {opcao}")
    
    print("\n--------------------------------------------------")

    palpite = input("SUA RESPOSTA (Digite a letra):")

    if palpite.lower().strip() == 'sair':
      print("\nSISTEMA: Sessão de estudos encerrada. Bons estudos!")
      break 

    resposta_certa = dados_estudo.get('resposta_correta', '')

    print("\n============ GABARITO ============")

    if palpite.lower().strip() == resposta_certa.lower().strip():
      print(f"RESULTADO: CORRETO! A resposta era {resposta_certa}.")
    else:
      print(f"RESULTADO: INCORRETO. A resposta correta era {resposta_certa}")

    print(f"EXPLICAÇÃO:{dados_estudo.get('explicacao_resposta')}")
    print("====================================================\n")
  except Exception as e:
    print(f"\n[ERRO NO SERVIDOR DE ESTUDOS]? {e}\n")

