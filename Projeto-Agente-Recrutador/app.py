# 2. CREDENCIAIS DIRETAS
endpoint = ""
api_key = ""
deployment = "gpt-4o"

# 3. Inicialização do Cliente Azure OpenAI
ai_client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-02-15-preview"
)

# ======================================================================
# BLOCO 3: PROMPT DO GESTOR DE CARREIRA E ESPECIALISTA EM ATS
# ======================================================================
prompt_mentor_avancado = """Você é um Tech Recruiter Sênior especialista em otimização de currículos para sistemas ATS (Applicant Tracking Systems).
Sua missão é transformar relatos informais em currículos de alto impacto para a área de tecnologia.

REGRAS DE FORMATAÇÃO E ESCRITA:
1. Use a fórmula XYZ do Google para os bullet points: "Realizei [X], medido por [Y], fazendo [Z]".
2. Se o candidato não fornecer métricas ou dados quantificáveis, insira placeholders como "[Insira métrica aqui]" ou "[Insira impacto aqui]" para forçá-lo a pensar no impacto técnico.
3. Classifique as Hard Skills rigorosamente em categorias estruturadas.

Retorne EXCLUSIVAMENTE em formato JSON com as seguintes chaves:
- "score_ats_estimado": Um número de 0 a 100 avaliando a qualidade e profundidade dos dados originais.
- "resumo_profissional": Um parágrafo de impacto vendendo o perfil técnico.
- "experiencias_otimizadas": Uma lista [Array] de objetos com chaves "titulo_cargo" e "bullet_points_xyz".
- "hard_skills": Um objeto contendo listas separadas para "Linguagens", "Frameworks" e "Ferramentas".
- "soft_skills": Uma lista [Array] com as 3 principais competências comportamentais deduzidas do texto.
- "perguntas_investigativas": Uma lista [Array] com perguntas cruciais que faltam para o currículo ficar perfeito.
- "feedback_final": Um parágrafo construtivo dando uma dica de recrutador sobre como o candidato pode melhorar o currículo, o que estudar a seguir, ou como se portar na entrevista baseado no perfil dele."""

#Motor do sistema

print("======================================")
print("SISTEMA DE OTIMIZAÇÃO DE CURRICULO PARA ATS")
print("Digite 'sair' a qualquer momento para encerrar")
print("======================================\n")

while True:
  print("\n-------- NOVA ANALISE ----------")

  nome = input("SISTEMA: Digite seu nome completo: ")
  if nome.lower().strip() == 'sair':
    break
  
  cargo_alvo = input("SISTEMA: Qual o cargo exato da vaga alvo? (ex: Desenvolvedor Fullstack Junior): ")
  if cargo_alvo.lower().strip() == 'sair'
    break

  print("\nSISTEMA: Cole o texto bruto das suas experiências, projetos de portifólio e tecnologias usadas.")
  relato_bruto = input("CANDIDATO: ")
  if relato_bruto().strip() == 'sair'
    break
  
  print("\n[SISTEMA] Processando analise ATS...\n")

  perfil_para_ia = f"Nome: {nome}\nVaga Alvo: {cargo_alvo}\nDados Brutos: {relato_bruto}"

  try:
    response = ai_client.chat.conpletions.create(
        model = deployment,
        messages = [
            {"role": "system", "content": prompt_mentor_avancado},
            {"role": "user", "content": perfil_para_ia}
        ],
        max_tokens = 1000,
        temperature = 0.3,
        response_format ={"type": "json_object"}
    )

    curriculo_fase1 = json.loads(response.choises[0].message.content)

    print("================= GAP ANALYSIS (FALHAS ENCONTRADAS) =================")
    perguntas = curriculo_fase1.get('perguntas_investigativas', [])

    if not perguntas:
      print("Seu relato inicial já estava excelente! Nenhuma informação crítica faltando.")
      curriculo_final1 = curriculo_fase1
    else:
      print("Para seu curriculo não ser barrado na triagem técnica, preencha estas lacuna obrigatórias:\n")
      for i, pergunta in enumerate(perguntas):
        print(f"{i+1}. {pergunta}")

