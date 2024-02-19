import os
import time
import datetime
import pdfplumber
import pandas as pd

# Função para extrair dados do PDF
def extrair_dados_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Suponha que as informações que você deseja estão na primeira página do PDF
            primeira_pagina = pdf.pages[0]
            texto = primeira_pagina.extract_text()

            # Extrair o número do Invoice
            invoice_number = texto.split("Invoice #")[1].split()[0]

            # Extrair a data do Invoice
            invoice_date = texto.split("Invoice Date:")[1].split()[0]

            # Extrair o valor total
            total_index = texto.find("Grand Total")
            total = texto[total_index+12:total_index+20]

            return invoice_number, invoice_date, total
    except Exception as e:
        print("Erro ao extrair dados do PDF:", e)
        return None, None, None

# Diretório onde o script está localizado
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
pasta_origem = os.path.join(diretorio_atual, "Documentos a processar")
arquivo_excel_path = os.path.join(diretorio_atual, "dados_lidos.xlsx")

# Verificar se o arquivo Excel já existe
if not os.path.exists(arquivo_excel_path):
    # Se não existe, criar um DataFrame vazio
    df = pd.DataFrame(columns=["Invoice Number", "Invoice Date", "Grand Total"])
    df.to_excel(arquivo_excel_path, index=False)

# Loop para verificar a pasta a cada 5 minutos
while True:
    for filename in os.listdir(pasta_origem):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pasta_origem, filename)
            invoice_number, invoice_date, total = extrair_dados_pdf(pdf_path)
            if invoice_number and invoice_date and total:
                print("Arquivo PDF encontrado:", filename)
                print("Invoice Number:", invoice_number)
                print("Invoice Date:", invoice_date)
                print("Grand Total:", total)
                print("------------------------")

                # Abrir arquivo Excel e adicionar dados
                df = pd.read_excel(arquivo_excel_path)
                novo_dado = {"Invoice Number": invoice_number,
                             "Invoice Date": invoice_date,
                             "Grand Total": total}
                df = df.append(novo_dado, ignore_index=True)                
                df.to_excel(arquivo_excel_path, index=False)
                print("Dados adicionados ao arquivo Excel")

                # Mover o arquivo PDF para a pasta de destino
                arquivo_destino = os.path.join(diretorio_atual, "Documentos_processados", filename)
                os.makedirs(os.path.dirname(arquivo_destino), exist_ok=True)
                os.replace(pdf_path, arquivo_destino)
                print("Arquivo movido para:", arquivo_destino)

            else:
                print("Falha ao extrair dados do arquivo PDF:", filename)
    # Aguardar 5 minutos antes da próxima verificação
    time.sleep(300)