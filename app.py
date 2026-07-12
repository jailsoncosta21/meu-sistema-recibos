import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# ... (restante do código)

def conectar_planilha():
    # Carrega as credenciais direto do Secrets
    creds_dict = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(creds_dict)
    
    # Define os escopos necessários
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_with_scopes = creds.with_scopes(scopes)
    
    gc = gspread.authorize(creds_with_scopes)
    return gc

# No seu botão de gerar, use:
# gc = conectar_planilha()
# sh = gc.open("Sistema de Gestão Imobiliária Completo VFinal")
