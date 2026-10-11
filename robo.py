import streamlit as st
import pandas as pd

st.set_page_config(page_title="Auditor Fiscal - Painel Profissional", layout="wide")

USER = "joap_admin"
SENHA = "123456"

st.title("Auditor Fiscal - Painel Profissional")

if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.subheader("Login do Auditor")
    u = st.text_input("Usuário", value="joap_admin")
    s = st.text_input("Senha", type="password")
    if st.button("Entrar", type="primary"):
        if u == USER and s == SENHA:
            st.session_state.logado = True
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")
    st.stop()

st.success(f"Bem-vindo, {USER}! Seu robô está no ar. Pode importar a NFS-e.")

if st.button("Sair"):
    st.session_state.logado = False
    st.rerun()

st.divider()
st.subheader("📊 Importar Planilha de NFS-e de João Pessoa")

arquivo = st.file_uploader("Arraste aqui o Excel ou CSV da Prefeitura", type=["xlsx","xls","csv"])

if arquivo:
    if arquivo.name.endswith(".csv"):
        df = pd.read_csv(arquivo)
    else:
        df = pd.read_excel(arquivo)
    
    st.success(f"Carregado! {len(df)} notas encontradas.")
    st.dataframe(df, use_container_width=True)
    
    st.download_button("📥 Baixar Relatório Auditado", df.to_csv(index=False).encode('utf-8'), "relatorio_auditado.csv", "text/csv")
else:
    st.info("Aguardando sua planilha... assim que soltar aqui já vai auditar.")

