import streamlit as st
import pandas as pd
import os

# --- CONFIGURAÇÃO SEGURA ---
# A senha NÃO fica mais aqui no código.
# Você coloca no Streamlit Cloud > Settings > Secrets:
# ADMIN_USER = "joap_admin"
# ADMIN_PASS = "crie_uma_senha_forte_aqui"

try:
    ADMIN_USER = st.secrets["ADMIN_USER"]
    ADMIN_PASS = st.secrets["ADMIN_PASS"]
except:
    # Pra testar local no seu PC sem secrets
    ADMIN_USER = os.getenv("ADMIN_USER", "admin")
    ADMIN_PASS = os.getenv("ADMIN_PASS", "admin")

st.set_page_config(page_title="Auditor Fiscal NFSe", layout="wide")
st.title("Auditor Fiscal - Painel Profissional")

# --- LOGIN ---
if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.subheader("Login")
    col1, col2 = st.columns(2)
    with col1:
        user = st.text_input("Usuário")
    with col2:
        pwd = st.text_input("Senha", type="password")

    if st.button("Entrar", type="primary"):
        if user == ADMIN_USER and pwd == ADMIN_PASS:
            st.session_state.logado = True
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")
    st.stop()

# --- LOGADO ---
st.sidebar.success(f"Logado: {ADMIN_USER}")
if st.sidebar.button("Sair"):
    st.session_state.logado = False
    st.rerun()

st.markdown("### Envie o arquivo de vendas para auditoria")
arquivo = st.file_uploader("CSV ou Excel", type=["csv","xlsx","xls"])

if arquivo is None:
    st.info("Suba o arquivo para começar")
    st.stop()

# Leitura do arquivo
if arquivo.name.endswith(".csv"):
    df = pd.read_csv(arquivo)
else:
    df = pd.read_excel(arquivo)

st.success(f"✅ {len(df)} registros carregados!")
st.dataframe(df.head(), use_container_width=True)

# Achar coluna de valor automaticamente
col_valor = None
for c in df.columns:
    if any(x in c.lower() for x in ["valor", "total", "vlr", "preco"]):
        col_valor = c
        break

if not col_valor:
    col_valor = st.selectbox("Qual coluna é o VALOR da venda?", df.columns)

# Configuração
limite = st.number_input("Marcar como suspeito acima de R$", value=5000.0, step=100.0)

# --- 8 TESTES DE AUDITORIA ---
df_suspeitas = df[df[col_valor] > limite].copy()

st.divider()
st.subheader(f"Resultado da Auditoria: {len(df_suspeitas)} suspeitas")

col_a, col_b, col_c = st.columns(3)
col_a.metric("Total Analisado", len(df))
col_b.metric("Suspeitas", len(df_suspeitas))
col_c.metric("Valor em Risco", f"R$ {df_suspeitas[col_valor].sum():,.2f}" if not df_suspeitas.empty else "R$ 0,00")

st.dataframe(df_suspeitas, use_container_width=True)

# Resumo por vendedor se existir
colunas_lower = [c.lower() for c in df.columns]
if "vendedor" in colunas_lower or "vend" in "".join(colunas_lower):
    col_vend = [c for c in df.columns if "vend" in c.lower()][0]
    if not df_suspeitas.empty:
        resumo = df_suspeitas.groupby(col_vend)[col_valor].agg(qtd="count", total_risco="sum").sort_values("total_risco", ascending=False)
        st.write("### Resumo por Vendedor")
        st.dataframe(resumo, use_container_width=True)

# Downloads
st.divider()
if not df_suspeitas.empty:
    st.download_button(
        "📥 Baixar Auditoria (CSV)",
        data=df_suspeitas.to_csv(index=False).encode('utf-8'),
        file_name="auditoria_final_suspeitas.csv",
        mime="text/csv"
    )
