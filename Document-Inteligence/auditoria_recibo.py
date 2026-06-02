import os
import sys
from dotenv import load_dotenv
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

ENDPOINT = os.getenv("DOC_INTEL_ENDPOINT")
CHAVE = os.getenv("DOC_INTEL_KEY")

cliente_documentos = DocumentAnalysisClient(
    endpoint=ENDPOINT,
    credential=AzureKeyCredential(CHAVE)
)


print("-------------------------")
print("Sistema de Auditoria Recibo")

caminho_arquivo = "meu_recibo.jpg"

try:

    with open(caminho_arquivo, "rb") as documento_fisico:
        print("Enviando documento para análise na Azure...")

        operacao = cliente_documentos.begin_analyze_document(
            model_id="prebuilt-receipt",
            document=documento_fisico
        )

    recibo_extraido = operacao.result()

    for recibo in recibo_extraido.documents:
        nome_loja = recibo.fields.get("MerchantName")
        total_gasto = recibo.fields.get("Total")
        data_compra = recibo.fields.get("TransactionDate")

        print("\nRESULTADOS DA EXTRAÇÃO:")

        if nome_loja:
            print(f"Fornecedor: {nome_loja.value}")

        if data_compra:
            print(f"Data da compra: {data_compra.value}")

        if total_gasto:
            print(f"Total a reembolsar: R$ {total_gasto.value}")

except FileNotFoundError:
    print(f"\n[ERRO]: Arquivo não encontrado: {caminho_arquivo}")

except Exception as erro:
    print(f"\n[ERRO NA LEITURA DA NUVEM]: {erro}")