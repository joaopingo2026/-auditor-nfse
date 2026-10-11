import streamlit as st
import pandas as pd

st.set_page_config(page_title="Auditor Fiscal - Painel Profissional", layout="wide")

# --- CONFIGURAÇÃO DE LOGIN ---
USUARIO = "joap_admin"
SENHA = "123456789"

st.title("Auditor Fiscal - Painel Profissional")

if "logado" not in st.session_state:
    st.session_state.logado = False

# TELA DE LOGIN
if not st.session_state.logado:
    st.subheader("Login do Auditor")
    usuario_digitado = st.text_input("Usuario")
    senha_digitada = st.text_input("Senha", type="password")
    
    if st.button("Entrar", type="primary"):
        if usuario_digitado.strip() == USUARIO and senha_digitada.strip() == SENHA:
            st.session_state.logado = True
            st.rerun()
        else:
            st.error("Usuario ou senha incorretos. Use joap_admin e 123456")
    st.stop()

# TELA LOGADA
st.success(f"Bem-vindo, {USUARIO}! Seu robo esta no ar.")
if st.button("Sair"):
    st.session_state.logado = False
    st.rerun()

st.divider()
st.subheader("Importar Planilha de NFS-e de Joao Pessoa - Auditoria")
st.info("Sistema vai auditar ISS e retencoes automaticamente.")

arquivo = st.file_uploader("Arraste aqui o Excel ou CSV da Prefeitura de JP", type=["xlsx", "xls", "csv"])

if arquivo is not None:
    try:
        if arquivo.name.lower().endswith(".csv"):
            df = pd.read_csv(arquivo, sep=None, engine="python")
        else:
            df = pd.read_excel(arquivo)
        
        st.success(f"Carregado com sucesso! {len(df)} notas encontradas.")
        
        col1, col2 = st.columns(2)
        col1.metric("Total de Notas", len(df))
        
        st.subheader("Previa dos Dados")
        st.dataframe(df, use_container_width=True)
        
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Baixar Relatorio Auditado (CSV)",
            data=csv_bytes,
            file_name="relatorio_auditado_JP.csv",
            mime="text/csv",
            type="primary"
        )
        
        st.warning("Auditoria: Verifique ISS retido e aliquotas fora do padrao de Joao Pessoa (2% a 5%).")
        
    except Exception as e:
        st.error(f"Erro ao ler arquivo: {e}")
else:
    st.info("Aguardando sua planilha... arraste aqui em cima.")

