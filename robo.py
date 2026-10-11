import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Robô Auditor NFS-e PRO", page_icon="🤖", layout="wide")

# --- SEU NEGÓCIO - EDITE AQUI ---
PIX = "8399940-6651 - JOAO BATISTA FERREIRA LIMA"
VALOR = "R$ 250,00 / mês"
SENHAS = {"contador1": "1234", "admin": "admin2026", "joao": "auditor", "demo": "demo123"}

# --- LOGIN ---
if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.title("🤖 Robô Auditor NFS-e - Acesso Restrito")
    st.warning(f"Para liberar: Faça PIX de {VALOR} para {PIX} e peça seu usuário")
    u = st.text_input("Usuário")
    s = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if u in SENHAS and SENHAS[u] == s:
            st.session_state.logado = True
            st.session_state.user = u
            st.rerun()
        else:
            st.error("Não liberado. Faça o PIX e me chame no WhatsApp!")
    st.stop()

# --- SISTEMA ---
st.sidebar.success(f"Logado: {st.session_state.user}")
if st.sidebar.button("Sair"):
    st.session_state.logado = False
    st.rerun()

st.title("🤖 ROBÔ DE AUDITORIA PRO - VERSÃO FINAL")
st.caption(f"Logado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

arquivo = st.file_uploader("Arraste a planilha da NFS-e aqui", type=["csv","xlsx","xls"])

if arquivo:
    if arquivo.name.endswith(".csv"):
        df = pd.read_csv(arquivo)
    else:
        df = pd.read_excel(arquivo)

    st.success(f"✅ {len(df)} vendas carregadas!")
    st.write("Colunas:", list(df.columns))

    # Achar coluna de valor
    col_valor = None
    for c in df.columns:
        if "valor" in c.lower() or "total" in c.lower() or "vlr" in c.lower() or "valentia" in c.lower():
            col_valor = c
            break
    if not col_valor:
        col_valor = st.selectbox("Qual coluna é o VALOR?", df.columns)

    limite = st.number_input("Marcar como suspeito acima de R$", value=5000.0)
    supostas = df[df[col_valor] > limite].copy()

    st.error(f"⚠️ {len(supostas)} vendas suspeitas acima de R$ {limite:,.2f}")
    st.dataframe(supostas)

    # Resumo por vendedor
    if "vendedor" in [c.lower() for c in df.columns]:
        col_vend = [c for c in df.columns if "vendedor" in c.lower()][0]
        resumo = supostas.groupby(col_vend)[col_valor].agg(qtd="count", total_risco="sum").sort_values("total_risco", ascending=False)
        st.write("### Resumo por vendedor")
        st.dataframe(resumo)

    csv = supostas.to_csv(index=False).encode('utf-8')
    st.download_button("📥 BAIXAR RELATÓRIO", csv, "relatorio_auditoria.csv", "text/csv")
else:
    st.info("👆 Faça upload da planilha para começar a auditar")
