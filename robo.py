import streamlit as st

st.set_page_config(page_title="Auditor Fiscal - Painel Profissional", layout="wide")

# --- LOGIN FIXO - VAI ENTRAR DE CERTEZA ---
USER_CORRETO = "joap_admin"
SENHA_CORRETA = "123456"

st.title("Auditor Fiscal - Painel Profissional")

if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.subheader("Login")
    usuario = st.text_input("Usuário", value="joap_admin")
    senha = st.text_input("Senha", type="password")
    
    if st.button("Entrar", type="primary"):
        if usuario == USER_CORRETO and senha == SENHA_CORRETA:
            st.session_state.logado = True
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")
    st.stop()

# --- AQUI COMEÇA SEU PAINEL ---
st.success(f"Bem-vindo, {USER_CORRETO}!")
st.write("Seu robô está no ar. Pode importar a NFS-e.")

if st.button("Sair"):
    st.session_state.logado = False
    st.rerun()

# COLA O RESTO DO SEU CÓDIGO AQUI EMBAIXO SE TIVER MAIS COISA

