import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OAI_KEY"),
    api_version="2024-02-15-preview"
)

deployment_name = os.getenv("AZURE_OIA_DEPLOYMENT")

system_message = """
Você é o assistente virtual da 'BurgerByte', uma hamburgueria artesanal com temática tecnológica. 
Seu objetivo é conduzir o cliente a fechar um pedido de forma rápida, sendo extremamente educado, amigável e focado em vendas (upsell).
Se o cliente estiver indeciso, sugira o 'Stack Proteico' (três hambúrgueres artesanais de 150g, queijo e ovo, ideal para quem precisa de bater a meta de proteínas do dia e focar na manutenção da massa muscular). 
Você deve sempre tentar confirmar três informações antes de encerrar: 1) o hambúrguer escolhido, 2) o acompanhamento/bebida e 3) se é para entrega ou retirada. 
Nunca saia do per
sonagem, mesmo que o usuário faça perguntas fora do contexto de comida
"""

messages = [{"role":"system", "content": system_message}]

print("---SISTEMA DA BUGERBYTE -- Aguardando Cliente... Digite 'sair' para encerrar")
while True:
    user_input = input("\nCliente: ")
    if user_input.lower() == "sair":
        print("\nSistema Encerrado")
        break

    messages.append({"role": "user", "content":user_input})
    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,

        temperature=0.7,
        max_tokens=400
    )

    reply = response.choices[0].message.content
    print(f"\n BurgerByte: {reply}")