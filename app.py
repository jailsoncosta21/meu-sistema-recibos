import streamlit as st
import gspread
import json
from fpdf import FPDF
from google.oauth2.service_account import Credentials

# --- FUNÇÃO DE CONEXÃO ---
def conectar_planilha():
    # Carrega do Secrets (Cloud) ou do arquivo local
    if "gcp_service_account" in st.secrets:
        creds_dict = dict(st.secrets["gcp_service_account"])
    else:
        with open('credenciais.json') as f:
            creds_dict = json.load(f)
            
    # Cria as credenciais usando a biblioteca oficial do Google
    # Ela lida nativamente com o formato da 'private_key' sem precisar de manipulação
    creds = Credentials.from_service_account_info(creds_dict)
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = creds.with_scopes(scopes)
    
    return gspread.authorize(creds)

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gerador de Recibos", page_icon="🏠")
st.title("🏠 Gerador de Recibos")

unidade = st.text_input("Digite a Unidade (ex: C04):")

if st.button("Gerar Recibo"):
    if not unidade:
        st.warning("Por favor, digite a unidade.")
    else:
        try:
            # 1. Conecta
            gc = conectar_planilha()
            sh = gc.open("Sistema de Gestão Imobiliária Completo VFinal")
            aba = sh.worksheet("Cadastro")
            registros = aba.get_all_values()
            
            # 2. Busca o registro
            dados = next((l for l in registros if l[0].strip() == unidade.strip()), None)
            
            if dados:
                # 3. Gera PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(200, 10, txt="RECIBO DE PAGAMENTO", ln=True, align='C')
                pdf.ln(10)
                
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt=f"Unidade: {dados[0]}", ln=True)
                pdf.cell(200, 10, txt=f"Locatário: {dados[5]}", ln=True)
                pdf.cell(200, 10, txt=f"Valor: {dados[3]}", ln=True)
                
                pdf_output = pdf.output(dest='S').encode('latin-1')
                
                st.success(f"Recibo gerado para {dados[5]}!")
                st.download_button("📥 Baixar PDF", data=pdf_output, file_name=f"Recibo_{unidade}.pdf", mime="application/pdf")
            else:
                st.error("Unidade não encontrada na planilha.")
        except Exception as e:
            st.error(f"Erro de conexão: {str(e)}")
