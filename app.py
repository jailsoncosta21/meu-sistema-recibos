import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.title("Teste de Conexão")

def conectar_planilha():
    # Carrega as credenciais do Secrets
    creds_dict = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(creds_dict)
    
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds_with_scopes = creds.with_scopes(scopes)
    
    gc = gspread.authorize(creds_with_scopes)
    return gc

try:
    st.write("Tentando conectar à planilha...")
    gc = conectar_planilha()
    sh = gc.open("Sistema de Gestão Imobiliária Completo VFinal")
    st.success("Conexão realizada com sucesso!")
    st.write(f"Planilha encontrada: {sh.title}")
except Exception as e:
    st.error(f"Erro ao conectar: {e}")
