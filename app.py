import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

# --- Comparação entre produtos financeiros ---
st.subheader("Comparação entre Produtos Financeiros")

# Transformar o dicionário em DataFrame para facilitar a visualização
produtos_df = pd.DataFrame(produtos_financeiros).T  # .T para transpor e deixar cada produto como linha

st.dataframe(produtos_df)

# Selecionar produtos para comparar
selecionados = st.multiselect("Escolha produtos para comparar:", produtos_df.index)

if len(selecionados) > 0:
    st.write("Comparando:", ", ".join(selecionados))
    comparacao = produtos_df.loc[selecionados]

    # Mostrar tabela comparativa
    st.table(comparacao)

    # Exemplo: gráfico de barras comparando rentabilidade (se existir essa coluna)
    if "rentabilidade" in produtos_df.columns:
        fig, ax = plt.subplots()
        comparacao["rentabilidade"].plot(kind="bar", ax=ax)
        ax.set_title("Comparação de Rentabilidade")
        ax.set_ylabel("Rentabilidade (%)")
        st.pyplot(fig)

    # Exemplo: gráfico de barras comparando risco (se existir essa coluna)
    if "risco" in produtos_df.columns:
        fig, ax = plt.subplots()
        comparacao["risco"].plot(kind="bar", ax=ax, color="orange")
        ax.set_title("Comparação de Risco")
        ax.set_ylabel("Nível de Risco")
        st.pyplot(fig)
