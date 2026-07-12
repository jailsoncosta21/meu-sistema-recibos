import streamlit as st
import gspread
import json
import os
from fpdf import FPDF
from google.oauth2.service_account import Credentials
from babel.numbers import format_currency

# Função de Conexão Inteligente
def conectar_planilha():
    try:
        # Tenta carregar do Secrets (Streamlit Cloud)
        creds_dict = st.secrets["gcp_service_account"]
    except:
        # Tenta carregar do arquivo local (Codespaces)
        with open('credenciais.json') as f:
            creds_dict = json.load(f)
    
    creds = Credentials.from_service_account_info(creds_dict)
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = creds.with_scopes(scopes)
    return gspread.authorize(creds)

# Interface
st.title("🏠 Gerador de Recibos")
unidade = st.text_input("Digite a Unidade (ex: C04):")

if st.button("Gerar Recibo"):
    if not unidade:
        st.warning("Por favor, digite a unidade.")
    else:
        try:
            gc = conectar_planilha()
            sh = gc.open("Sistema de Gestão Imobiliária Completo VFinal")
            aba = sh.worksheet("Cadastro")
            registros = aba.get_all_values()
            
            # Localizar linha
            dados = next((l for l in registros if l[0].strip() == unidade.strip()), None)
            
            if dados:
                # --- AQUI VAI A SUA LÓGICA DE PDF ---
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(200, 10, txt="RECIBO DE PAGAMENTO", ln=True, align='C')
                pdf.ln(10)
                
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt=f"Unidade: {dados[0]}", ln=True)
                pdf.cell(200, 10, txt=f"Locatario: {dados[5]}", ln=True)
                pdf.cell(200, 10, txt=f"Valor: {dados[3]}", ln=True)
                
                # Gerar em bytes
                pdf_output = pdf.output(dest='S').encode('latin-1')
                
                st.success("Recibo gerado!")
                st.download_button(
                    label="📥 Baixar PDF",
                    data=pdf_output,
                    file_name=f"Recibo_{unidade}.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("Unidade não encontrada!")
        except Exception as e:
            st.error(f"Erro: {e}")
