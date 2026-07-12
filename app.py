import streamlit as st
import gspread
from fpdf import FPDF
from google.oauth2.service_account import Credentials

# --- FUNÇÃO DE CONEXÃO (SEGURA) ---
def conectar_planilha():
    # Carrega diretamente o dicionário do Secrets configurado no Streamlit Cloud
    creds_dict = st.secrets["gcp_service_account"]
    
    # Cria as credenciais e define o escopo de acesso
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
            # 1. Conecta na planilha
            gc = conectar_planilha()
            sh = gc.open("Sistema de Gestão Imobiliária Completo VFinal")
            aba = sh.worksheet("Cadastro")
            registros = aba.get_all_values()
            
            # 2. Busca o registro pelo número da unidade
            dados = next((l for l in registros if l[0].strip() == unidade.strip()), None)
            
            if dados:
                # 3. Gera o PDF em memória
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(200, 10, txt="RECIBO DE PAGAMENTO", ln=True, align='C')
                pdf.ln(10)
                
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt=f"Unidade: {dados[0]}", ln=True)
                pdf.cell(200, 10, txt=f"Locatario: {dados[5]}", ln=True)
                pdf.cell(200, 10, txt=f"Valor: {dados[3]}", ln=True)
                
                # Gera o arquivo como bytes para não salvar no servidor
                pdf_output = pdf.output(dest='S').encode('latin-1')
                
                st.success(f"Recibo gerado para {dados[5]}!")
                st.download_button(
                    label="📥 Baixar PDF do Recibo",
                    data=pdf_output,
                    file_name=f"Recibo_{unidade}.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("Unidade não encontrada na planilha.")
                
        except Exception as e:
            st.error(f"Erro ao acessar Google Sheets: {str(e)}")

# Rodapé simples
st.sidebar.markdown("---")
st.sidebar.info("Sistema de Geração de Recibos v1.0")
