import streamlit as st
import gspread
import json
from fpdf import FPDF
from google.oauth2.service_account import Credentials

# --- FUNÇÃO DE CONEXÃO (À PROVA DE ERROS) ---
def conectar_planilha():
    # 1. Tenta carregar do Secrets (Cloud) ou do arquivo (Local)
    if "gcp_service_account" in st.secrets:
        creds_dict = dict(st.secrets["gcp_service_account"])
    else:
        with open('credenciais.json') as f:
            creds_dict = json.load(f)
            
    # 2. Correção forçada para o erro InvalidByte/PEM
    # Remove espaços extras e garante que o \n seja lido corretamente pelo Python
    if "private_key" in creds_dict:
        raw_key = creds_dict["private_key"]
        creds_dict["private_key"] = raw_key.replace("\\n", "\n")

    # 3. Cria as credenciais
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
            # Conecta na planilha
            gc = conectar_planilha()
            sh = gc.open("Sistema de Gestão Imobiliária Completo VFinal")
            aba = sh.worksheet("Cadastro")
            registros = aba.get_all_values()
            
            # Busca o registro
            dados = next((l for l in registros if l[0].strip() == unidade.strip()), None)
            
            if dados:
                # Gera PDF
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
            st.error(f"Erro ao acessar Google Sheets: {str(e)}")
