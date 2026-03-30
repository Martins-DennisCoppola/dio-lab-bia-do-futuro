import streamlit as st
import pandas as pd
import json
import requests

# --- Configuração inicial ---
st.set_page_config(page_title="Lumi - Agente Financeiro Inteligente", layout="wide")
st.title("💡 Lumi - Agente Financeiro Inteligente")

# --- Carregar base de conhecimento ---
transacoes = pd.read_csv("data/transacoes.csv")
with open("data/perfil_investidor.json", "r", encoding="utf-8") as f:
    perfil_investidor = json.load(f)
with open("data/produtos_financeiros.json", "r", encoding="utf-8") as f:
    produtos_financeiros = json.load(f)
with open("data/conhecimento_mercado.json", "r", encoding="utf-8") as f:
    conhecimento_mercado = json.load(f)

# --- Configuração Hugging Face ---
HF_API_TOKEN = st.secrets["HF_API_TOKEN"]
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-v0.1"

headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

def gerar_resposta(prompt):
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 300}}
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return "⚠️ Erro ao consultar modelo Hugging Face."

# --- System Prompt ---
SYSTEM_PROMPT = """
Você é Lumi, um agente financeiro inteligente e consultivo.
Seu papel é:
- Antecipar necessidades do cliente
- Personalizar sugestões com base no perfil e transações
- Cocriar soluções financeiras de forma clara e segura
- Nunca inventar dados: use apenas a base de conhecimento fornecida
- Se não souber, explique que não há informação disponível
"""

# --- Histórico de chat ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": SYSTEM_PROMPT}]

# --- Interface de chat ---
st.subheader("💬 Chat com Lumi")

for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f"**Você:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**Lumi:** {msg['content']}")

user_input = st.text_input("Digite sua pergunta ou solicitação:")

if st.button("Enviar") and user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})

    contexto = f"""
    Perfil do investidor: {perfil_investidor}
    Produtos financeiros disponíveis: {produtos_financeiros}
    Conhecimento de mercado: {conhecimento_mercado}
    Histórico de transações: {transacoes.head(10).to_dict()}
    """

    prompt = SYSTEM_PROMPT + "\n\nContexto:\n" + contexto + "\n\nUsuário: " + user_input + "\nLumi:"
    resposta = gerar_resposta(prompt)

    st.session_state["messages"].append({"role": "assistant", "content": resposta})
    st.rerun()
