import streamlit as st
import gspread
from fpdf import FPDF
from google.oauth2.service_account import Credentials
from babel.numbers import format_currency
from num2words import num2words
import datetime

# 1. Função de Conexão (Usa o Secrets do Streamlit)
def conectar_planilha():
    creds_dict = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(creds_dict)
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = creds.with_scopes(scopes)
    return gspread.authorize(creds)

# 2. Interface do App
st.title("🏠 Sistema de Recibos")
unidade = st.text_input("Digite a Unidade (ex: C04):")

if st.button("Gerar Recibo"):
    if not unidade:
        st.warning("Por favor, digite a unidade.")
    else:
        try:
            gc = conectar_planilha()
            sh = gc.open("Sistema de Gestão Imobiliária Completo VFinal")
            aba = sh.worksheet("Cadastro")
            dados_planilha = aba.get_all_values()
            
            # Buscar linha correspondente
            registro = next((l for l in dados_planilha if l[0].strip() == unidade.strip()), None)
            
            if registro:
                st.success(f"Dados encontrados para {registro[1]}!")
                
                # --- AQUI VOCÊ COLA A LÓGICA DO FPDF QUE JÁ TEMOS ---
                # Exemplo simplificado de geração:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt=f"Recibo - Unidade: {registro[0]}", ln=True, align='C')
                pdf.cell(200, 10, txt=f"Locatario: {registro[5]}", ln=True)
                
                # Salvar em bytes para oferecer download
                pdf_output = pdf.output(dest='S').encode('latin-1')
                
                st.download_button(
                    label="📥 Baixar PDF do Recibo",
                    data=pdf_output,
                    file_name=f"Recibo_{unidade}.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("Unidade não encontrada na planilha.")
                
        except Exception as e:
            st.error(f"Erro ao processar: {e}")
