import streamlit as st
import gspread
from fpdf import FPDF
import datetime
import os
from babel.numbers import format_currency
from num2words import num2words

# Configuração da Página
st.set_page_config(page_title="Gestão de Recibos", page_icon="🏠")

st.title("🏠 Sistema de Recibos")
st.subheader("Geração via Celular")

# Configuração do caminho (Ajuste para o ambiente onde rodar)
caminho_base = r'C:\Users\jails\OneDrive\Área de Trabalho\Recibo' # No Streamlit Cloud, mudaremos isso
caminho_cred = os.path.join(caminho_base, 'credenciais.json')

# Input para o usuário escolher a unidade
unidade_selecionada = st.text_input("Digite a Unidade (ex: C04):", "C04")

if st.button("🚀 Gerar Recibo"):
    with st.spinner('Gerando PDF...'):
        try:
            # LÓGICA DO SEU CÓDIGO CONSOLIDADO
            gc = gspread.service_account(filename=caminho_cred)
            sh = gc.open("Sistema de Gestão Imobiliária Completo VFinal")
            
            aba_cadastro = sh.worksheet("Cadastro")
            lista_cadastro = aba_cadastro.get_all_values()
            
            # Busca os dados baseada no input do usuário
            dados = next(( {'unidade': l[0], 'nome': l[1], 'endereco': l[2], 'valor': l[3], 
                            'periodo': l[4], 'locatario': l[5]} for l in lista_cadastro[1:] 
                            if l[0].strip() == unidade_selecionada), None)
            
            if not dados:
                st.error("Unidade não encontrada!")
            else:
                # [AQUI VAI O SEU CÓDIGO DE GERAÇÃO PDF QUE JÁ VALIDAMOS]
                # ... (Lógica do FPDF)
                
                st.success(f"Recibo de {dados['locatario']} gerado com sucesso!")
                st.balloons()
        
        except Exception as e:
            st.error(f"Erro: {e}")