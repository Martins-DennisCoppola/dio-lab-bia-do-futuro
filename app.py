import json
import pandas as pd 
import requests
import streamlit as st

# === CONFIG UI === #
st.set_page_config(page_title="Lumi", layout="centered")

st.title("💡 Lumi, está na área !!!")
st.markdown("Seu agente inteligente que ajudar a organizar a sua vida financeira.")

# === MENSAGEM INICIAL === #
if "inicio" not in st.session_state:
    st.session_state.inicio = True
    st.chat_message("assistant").write(
        "Olá! 👋 Como posso te ajudar hoje?"
    )

# === MEMÓRIA === #
if "messages" not in st.session_state:
    st.session_state.messages = []

# === MOSTRAR HISTÓRICO === #
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# === CONFIGURAÇÃO === #
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "phi3:mini"

# === CARREGAR DADOS === #
@st.cache_data
def carregar_dados():
    perfil = json.load(open('./data/perfil_investidor.json'))
    transacoes = pd.read_csv('./data/transacoes.csv')
    historico = pd.read_csv('./data/historico_atendimento.csv')
    produtos = json.load(open('./data/produtos_financeiros.json'))
    return perfil, transacoes, historico, produtos

perfil, transacoes, historico, produtos = carregar_dados()

# === CONTEXTO === #
@st.cache_data
def montar_contexto(perfil, transacoes, historico, produtos):
    return f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} 

TRANSAÇÕES RECENTES:
{transacoes.tail(3).to_dict(orient="records")}

ATENDIMENTOS ANTERIORES:
{historico.tail(2).to_dict(orient="records")}

PRODUTOS DISPONÍVEIS:
{list(produtos.keys())}
"""

contexto = montar_contexto(perfil, transacoes, historico, produtos)

# === SYSTEM PROMPT === #
SYSTEM_PROMPT = """Você é Lumi, assistente financeiro.

Objetivo: garantir aporte mensal de R$500 (10%) para dobrar a renda passiva.

Regras:
- Use os dados fornecidos para personalizar respostas;
- Pode usar conhecimento geral de finanças para orientar;
- Nunca invente dados do cliente;
- Se faltar informação do cliente, diga e dê orientação geral;
- Priorize gastos essenciais (Aluguel, Energia, Gás);
- Só valide lazer após confirmar aporte;
- Perfil moderado → evitar alto risco;
- Responda apenas sobre finanças;
- Seja direto (máx 3 parágrafos curtos).
"""

# === FUNÇÃO SAUDAÇÃO === #
def eh_saudacao(msg):
    saudacoes = ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite"]
    msg = msg.lower()
    return any(s in msg for s in saudacoes)

# === FUNÇÃO PERGUNTAR (COM MEMÓRIA) === #
def perguntar(msg):
    historico_texto = ""

    for m in st.session_state.messages:
        if m["role"] == "user":
            historico_texto += f"Usuário: {m['content']}\n"
        else:
            historico_texto += f"Lumi: {m['content']}\n"

    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    HISTÓRICO DA CONVERSA:
    {historico_texto}

    Usuário: {msg}
    Lumi:"""

    r = requests.post(
        OLLAMA_URL,
        json={
            "model": MODELO,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 120,
                "temperature": 0.2,
                "top_k": 40
            }
        }
    )

    return r.json()["response"]

# === INPUT DO USUÁRIO === #
if user_input := st.chat_input("Sua dúvida sobre finanças...", key="input_principal"):
    
    # salvar user
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # resposta
    if eh_saudacao(user_input):
        resposta = "Olá! 👋 Em que posso te ajudar hoje com suas finanças?"
    else:
        with st.spinner("Pensando..."):
            resposta = perguntar(user_input)

    # salvar resposta
    st.session_state.messages.append({"role": "assistant", "content": resposta})
    st.chat_message("assistant").write(resposta)

    # limitar memória (performance)
    st.session_state.messages = st.session_state.messages[-6:]
