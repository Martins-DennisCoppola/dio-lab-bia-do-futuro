import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

st.title("Lumi - Wealth Guardian")

# --- Carregar dados ---
transacoes = pd.read_csv("Dados/transacoes.csv")

with open("Dados/perfil_investidor.json", "r", encoding="utf-8") as f:
    perfil_investidor = json.load(f)

with open("Dados/produtos_financeiros.json", "r", encoding="utf-8") as f:
    produtos_financeiros = json.load(f)

with open("Dados/conhecimento_mercado.json", "r", encoding="utf-8") as f:
    conhecimento_mercado = json.load(f)

# --- Exibir dados ---
st.subheader("Histórico de Transações")
st.dataframe(transacoes)

st.subheader("Perfil do Investidor")
st.json(perfil_investidor)

st.subheader("Produtos Financeiros")
st.json(produtos_financeiros)

st.subheader("Conhecimento de Mercado")
st.json(conhecimento_mercado)

# --- Gráfico de transações ---
st.subheader("Gráfico de Transações")
if "valor" in transacoes.columns and "data" in transacoes.columns:
    transacoes["data"] = pd.to_datetime(transacoes["data"])
    fig, ax = plt.subplots()
    ax.plot(transacoes["data"], transacoes["valor"], marker="o")
    ax.set_title("Evolução dos valores")
    ax.set_xlabel("Data")
    ax.set_ylabel("Valor (R$)")
    st.pyplot(fig)

# --- Estatísticas rápidas ---
st.subheader("Estatísticas")
if "tipo" in transacoes.columns:
    entradas = transacoes[transacoes["tipo"] == "entrada"]["valor"].sum()
    saidas = transacoes[transacoes["tipo"] == "saida"]["valor"].sum()
    st.write("Valor total de entradas:", entradas)
    st.write("Valor total de saídas:", saidas)
    st.write("Saldo líquido:", entradas - saidas)

# --- Análise por categoria ---
st.subheader("Distribuição por Categoria")
if "categoria" in transacoes.columns:
    categoria_totais = transacoes.groupby("categoria")["valor"].sum()
    st.bar_chart(categoria_totais)

# --- Análise por tipo de pagamento ---
st.subheader("Distribuição por Forma de Pagamento")
if "pagamento" in transacoes.columns:
    pagamento_totais = transacoes.groupby("pagamento")["valor"].sum()
    st.bar_chart(pagamento_totais)

# --- Comparação entre produtos financeiros ---
st.subheader("Comparação entre Produtos Financeiros")
produtos_df = pd.DataFrame(produtos_financeiros).T
st.dataframe(produtos_df)

# Filtrar produtos de acordo com perfil
st.subheader("Produtos Recomendados para o Perfil")
tolerancia_risco = perfil_investidor.get("tolerancia_risco", 3)
prazo_maximo = perfil_investidor["preferencias"].get("prazo_maximo_dias", 365)

# Filtragem simples: risco <= tolerancia e liquidez diária ou prazo aceitável
recomendados = produtos_df[
    (produtos_df["risco"] <= tolerancia_risco) &
    ((produtos_df["liquidez"] == "diaria") | (produtos_df["liquidez"] == "prazo determinado"))
]

st.table(recomendados)

# Comparação manual
selecionados = st.multiselect("Escolha produtos para comparar:", produtos_df.index)
if len(selecionados) > 0:
    comparacao = produtos_df.loc[selecionados]
    st.table(comparacao)

    if "rentabilidade" in produtos_df.columns:
        st.bar_chart(comparacao["rentabilidade"])

    if "risco" in produtos_df.columns:
        st.bar_chart(comparacao["risco"])

# --- Interatividade ---
st.subheader("Simulação de Investimento")
valor = st.number_input("Digite o valor a investir:", min_value=0.0, step=100.0)
produto = st.selectbox("Escolha um produto:", list(produtos_financeiros.keys()))

if st.button("Simular"):
    st.success(f"Você investiria R$ {valor:.2f} em {produto}.")
