import pandas as pd
from datetime import datetime

print("🤖 ROBÔ DE AUDITORIA PRO - VERSÃO FINAL!")

df = pd.read_csv("vendas_10k.csv")
print(f"Total: {len(df)} vendas")
print(f"Colunas: {list(df.columns)}")

col_valor = 'valor'
col_vendedor = 'vendedor'

# FILTRO
suspeitas = df[df[col_valor] > 5000].copy()
print(f"⚠️ {len(suspeitas)} vendas acima de R$ 5.000")

# RESUMO POR VENDEDOR (agora certo!)
resumo = suspeitas.groupby(col_vendedor)[col_valor].agg(
    qtd_suspeitas='count',
    total_risco='sum',
    ticket_medio='mean'
).sort_values(by='total_risco', ascending=False).reset_index()

total_risco = suspeitas[col_valor].sum()

# SALVA
nome_final = f"auditoria_final_{datetime.now().strftime('%d-%m_%Hh%M')}.xlsx"

with pd.ExcelWriter(nome_final, engine='openpyxl') as writer:
    suspeitas.to_excel(writer, sheet_name='Vendas_Suspeitas', index=False)
    resumo.to_excel(writer, sheet_name='Resumo_Por_Vendedor', index=False)

print(f"💰 Total em risco: R$ {total_risco:,.2f}")
print(f"✅ Salvei: {nome_final}")
print("\n🏆 TOP 5 VENDEDORES EM RISCO:")
print(resumo.head(5).to_string(index=False))