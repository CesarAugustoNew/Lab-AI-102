import json # Biblioteca nativa do Python para manipular dados no formato JSON
from openai import AzureOpenAI # SDK oficial para conectar com a Azure

endpoint = ""
api_key = ""
deployment = "gpt-4o"

ai_client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-02-15-preview"
)

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


print("====================================================")
print(" SISTEMA DE OTIMIZACAO DE CURRICULOS PARA ATS")
print(" Digite 'sair' a qualquer momento para encerrar.")
print("====================================================\n")

while True:
    print("\n------------------- NOVA ANALISE -------------------")

    nome = input("SISTEMA: Digite seu nome completo: ")
    if nome.lower().strip() == 'sair': break

    cargo_alvo = input("SISTEMA: Qual o cargo exato da vaga alvo? (ex: Desenvolvedor Fullstack Junior): ")
    if cargo_alvo.lower().strip() == 'sair': break

    print("\nSISTEMA: Cole o texto bruto das suas experiências, projetos de portfólio e tecnologias usadas.")
    relato_bruto = input("CANDIDATO: ")
    if relato_bruto.lower().strip() == 'sair': break

    print("\n[SISTEMA] Processando analise ATS...\n")

    perfil_para_ia = f"Nome: {nome}\nVaga Alvo: {cargo_alvo}\nDados Brutos: {relato_bruto}"

    try:
        response = ai_client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": prompt_mentor_avancado},
                {"role": "user", "content": perfil_para_ia}
            ],
            max_tokens=1000, 
            temperature=0.3, # Temperatura baixa garante respostas mais tecnicas e menos criativas/alucinadas
            response_format={"type": "json_object"} # Forca a devolucao de um JSON valido
        )
        
        curriculo_fase1 = json.loads(response.choices[0].message.content)

        print("================ GAP ANALYSIS (FALHAS ENCONTRADAS) ================")
        perguntas = curriculo_fase1.get('perguntas_investigativas', [])
        
        if not perguntas:
            print("Seu relato inicial ja estava excelente! Nenhuma informacao critica faltando.")
            curriculo_final = curriculo_fase1
        else:
            print("Para o seu curriculo nao ser barrado na triagem tecnica, preencha estas lacunas obrigatórias:\n")
            for i, pergunta in enumerate(perguntas):
                print(f"{i+1}. {pergunta}")
                
            print("\n-------------------------------------------------------------------")
            print("SISTEMA: ATENCAO! O preenchimento dessas respostas e OBRIGATORIO para gerar o curriculo.")
            
            while True:
                respostas_aluno = input("\nCANDIDATO (Responda detalhadamente): ")
                
                if respostas_aluno.lower().strip() == 'sair':
                    break
                
                if len(respostas_aluno.strip()) < 10:
                    print("SISTEMA: Resposta muito curta. Por favor, detalhe melhor as respostas para um curriculo de qualidade!")
                    continue
                    
                break # Quebra o laco secundario caso a resposta tenha mais de 10 caracteres
                
            if respostas_aluno.lower().strip() == 'sair':
                break 
                
            print("\n[SISTEMA] Reescrevendo curriculo com os dados obrigatorios...\n")
            
            perfil_para_ia += f"\n\nRespostas as perguntas investigativas para refinamento: {respostas_aluno}"
            perfil_para_ia += "\nINSTRUCAO EXTRA: Gere a versao final do curriculo preenchendo os placeholders com estes novos dados."
            
            response_final = ai_client.chat.completions.create(
                model=deployment,
                messages=[
                    {"role": "system", "content": prompt_mentor_avancado},
                    {"role": "user", "content": perfil_para_ia}
                ],
                max_tokens=1000, 
                temperature=0.2, # Reduz a temperatura para focar na aplicacao estrita das novas respostas
                response_format={"type": "json_object"}
            )
            
            curriculo_final = json.loads(response_final.choices[0].message.content)
                
        print("\n================ SEU CURRICULO OTIMIZADO ================\n")
        
        score = curriculo_final.get('score_ats_estimado', 0)
        print(f"[{'ALTO' if score >= 80 else 'MEDIO' if score >= 50 else 'BAIXO'}] SCORE ATS DESTA VERSAO: {score}/100\n")
        
        print("--- RESUMO PROFISSIONAL ---")
        print(curriculo_final.get('resumo_professional', curriculo_final.get('resumo_profissional')))
        
        print("\n--- EXPERIENCIAS REESCRITAS (FORMULA XYZ) ---")
        experiencias = curriculo_final.get('experiencias_otimizadas', [])
        for exp in experiencias:
            print(f">> {exp.get('titulo_cargo')}")
            for ponto in exp.get('bullet_points_xyz', []):
                print(f"   - {ponto}") # Indentacao para simular bullet points visuais
            print()
            
        print("--- HARD SKILLS MAPEADAS ---")
        hards = curriculo_final.get('hard_skills', {})
        for categoria, itens in hards.items():
            if itens:
                print(f"[{categoria.upper()}]: {', '.join(itens)}")
        
        print("\n--- SOFT SKILLS DEDUZIDAS ---")
        print(" | ".join(curriculo_final.get('soft_skills', [])))
        
        print("\n--- FEEDBACK DO RECRUTADOR ---")
        print(curriculo_final.get('feedback_final', 'Continue aprimorando seus conhecimentos técnicos!'))
        
        print("====================================================================\n")

    except Exception as e:
        print(f"\n[ERRO NO SISTEMA]: {e}\n")