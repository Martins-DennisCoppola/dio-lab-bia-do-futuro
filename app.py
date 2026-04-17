import json
import os
import re
import unicodedata
import pandas as pd
import requests
import streamlit as st


# ==== CONFIGURAÇÕES INICIAIS ==== #

st.set_page_config(page_title="Lumi", page_icon="💡", layout="centered")

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "phi3:mini"

META_PATRIMONIAL = 500000.0
TAXA_MENSAL = 0.01


# ==== CONTEXTO ==== #

if "messages" not in st.session_state:
    st.session_state.messages = []

if "boas_vindas_exibida" not in st.session_state:
    st.session_state.boas_vindas_exibida = False


# ==== CARREGAMENTO DE DADOS ==== #

@st.cache_data
def carregar_dados():
    with open(os.path.join(DATA_DIR, "perfil_investidor.json"), encoding="utf-8") as f:
        perfil = json.load(f)

    with open(os.path.join(DATA_DIR, "produtos_financeiros.json"), encoding="utf-8") as f:
        produtos = json.load(f)

    with open(os.path.join(DATA_DIR, "conhecimento_mercado.json"), encoding="utf-8") as f:
        conhecimento = json.load(f)

    transacoes = pd.read_csv(os.path.join(DATA_DIR, "transacoes.csv"))
    historico = pd.read_csv(os.path.join(DATA_DIR, "historico_atendimento.csv"))

    return perfil, produtos, conhecimento, transacoes, historico


perfil, produtos, conhecimento_mercado, transacoes, historico = carregar_dados()


# ==== VERIFICANDO ARQUIVOS ==== #

colunas_transacoes = ["data", "descricao", "categoria", "valor", "tipo", "pagamento"]
for coluna in colunas_transacoes:
    if coluna not in transacoes.columns:
        st.error(f"Coluna obrigatória '{coluna}' não encontrada em transacoes.csv.")
        st.stop()

colunas_historico = ["data", "interacao", "resposta", "sentimento"]
for coluna in colunas_historico:
    if coluna not in historico.columns:
        st.error(f"Coluna obrigatória '{coluna}' não encontrada em historico_atendimento.csv.")
        st.stop()


# ==== FUNÇÕES AUXILIARES ==== #

def normalizar_texto(texto):
    texto = str(texto).strip().lower()
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("utf-8")
    texto = re.sub(r"[^\w\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def normalizar_transacoes(df):
    df = df.copy()
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df["tipo"] = df["tipo"].astype(str).str.lower().str.strip()
    df["categoria"] = df["categoria"].astype(str).str.lower().str.strip()
    df["descricao"] = df["descricao"].astype(str).str.strip()
    df["pagamento"] = df["pagamento"].astype(str).str.lower().str.strip()
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df = df.dropna(subset=["data", "valor"])
    return df


def obter_ultima_referencia(df):
    if df.empty:
        return None, None
    ultima_data = df["data"].max()
    return ultima_data.month, ultima_data.year


def filtrar_mes_atual(df):
    df = normalizar_transacoes(df)
    if df.empty:
        return df

    mes_atual, ano_atual = obter_ultima_referencia(df)
    return df[(df["data"].dt.month == mes_atual) & (df["data"].dt.year == ano_atual)]


def calcular_aporte_mes(df):
    df_mes = filtrar_mes_atual(df)
    if df_mes.empty:
        return 0.0

    valor = df_mes[
        (df_mes["tipo"] == "saida") & (df_mes["categoria"] == "investimento")
    ]["valor"].sum()

    return float(valor)


def calcular_receitas_mes(df):
    df_mes = filtrar_mes_atual(df)
    if df_mes.empty:
        return 0.0

    valor = df_mes[df_mes["tipo"] == "entrada"]["valor"].sum()
    return float(valor)


def calcular_gastos_mes(df):
    df_mes = filtrar_mes_atual(df)
    if df_mes.empty:
        return 0.0

    valor = df_mes[
        (df_mes["tipo"] == "saida") & (df_mes["categoria"] != "investimento")
    ]["valor"].sum()

    return float(valor)


def calcular_gasto_categoria(df, categoria):
    df_mes = filtrar_mes_atual(df)
    if df_mes.empty:
        return 0.0

    categoria = normalizar_texto(categoria)
    valor = df_mes[df_mes["categoria"] == categoria]["valor"].sum()
    return float(valor)


def calcular_tempo_meta(patrimonio_atual, aporte_mensal, taxa=TAXA_MENSAL, meta=META_PATRIMONIAL):
    total = float(patrimonio_atual)
    meses = 0

    if total >= meta:
        return 0

    if aporte_mensal <= 0 and taxa <= 0:
        return None

    while total < meta:
        total = total * (1 + taxa) + aporte_mensal
        meses += 1

        if meses > 1200:
            return None

    return meses


def formatar_tempo_meses(meses):
    if meses is None:
        return "não foi possível estimar"

    anos = meses // 12
    meses_restantes = meses % 12

    if anos == 0:
        return f"{meses_restantes} mês(es)"
    if meses_restantes == 0:
        return f"{anos} ano(s)"
    return f"{anos} ano(s) e {meses_restantes} mês(es)"


def resumir_historico(df, limite=3):
    if df.empty:
        return "Sem histórico disponível."

    amostra = df.tail(limite)
    linhas = []

    for _, row in amostra.iterrows():
        linhas.append(
            f"Data: {row['data']} | Interação: {row['interacao']} | Resposta: {row['resposta']} | Sentimento: {row['sentimento']}"
        )

    return "\n".join(linhas)


def resumir_produtos(produtos_dict, limite=5):
    itens = []
    for nome, dados in list(produtos_dict.items())[:limite]:
        itens.append(
            f"{nome}: risco {dados.get('risco')}, liquidez {dados.get('liquidez')}, indicado para {dados.get('indicado_para', 'não informado')}"
        )
    return "\n".join(itens)


def obter_nome_usuario(perfil_dict):
    return perfil_dict.get("nome", "Investidor")


def obter_meta_aporte(perfil_dict):
    return float(perfil_dict.get("meta_aporte_mensal", 500.0))


def buscar_conceito(pergunta, base_conhecimento):
    texto = normalizar_texto(pergunta)

    for chave, dados in base_conhecimento.items():
        chave_normalizada = normalizar_texto(chave)
        chave_com_espaco = chave_normalizada.replace("_", " ")

        if chave_normalizada in texto or chave_com_espaco in texto:
            return chave, dados

    sinonimos = {
        "tesouro selic": "tesouro_selic",
        "reserva de emergencia": "reserva_emergencia",
        "perfil moderado": "perfil_moderado",
    }

    for termo, chave in sinonimos.items():
        if termo in texto and chave in base_conhecimento:
            return chave, base_conhecimento[chave]

    return None, None


def buscar_produto(pergunta, produtos_dict):
    texto = normalizar_texto(pergunta)

    for nome, dados in produtos_dict.items():
        nome_normalizado = normalizar_texto(nome)
        if nome_normalizado in texto:
            return nome, dados

    aliases = {
        "cdb": "CDB Liquidez Diaria",
        "tesouro": "Tesouro Selic",
        "cripto": "Criptomoedas",
        "criptomoeda": "Criptomoedas",
        "acoes": "Acoes",
        "acao": "Acoes",
    }

    for termo, produto in aliases.items():
        if termo in texto and produto in produtos_dict:
            return produto, produtos_dict[produto]

    return None, None


def eh_saudacao(msg):
    texto = normalizar_texto(msg)

    saudacoes_exatas = {
        "oi",
        "ola",
        "bom dia",
        "boa tarde",
        "boa noite",
        "ei",
        "e ai",
        "iai",
        "olá",
    }

    return texto in saudacoes_exatas


def classificar_pergunta(msg, base_conhecimento, produtos_dict):
    texto = normalizar_texto(msg)

    if any(p in texto for p in ["bitcoin", "cripto", "criptomoeda", "alto risco"]):
        return "risco"

    if any(p in texto for p in ["chover", "clima", "temperatura", "previsao do tempo"]):
        return "fora_escopo"

    if any(p in texto for p in ["senha", "cpf", "documento", "conta bancaria", "dados bancarios", "cartao", "chave pix"]):
        return "seguranca"

    if any(p in texto for p in ["gastar", "gasto", "comprar", "compra", "ifood", "lazer"]):
        return "gasto"

    if any(p in texto for p in ["quanto falta", "minha meta", "meta patrimonial", "quanto tempo", "quando atinjo"]):
        return "meta"

    if any(p in texto for p in ["reserva de emergencia", "reserva", "emergencia"]):
        return "reserva"

    if eh_saudacao(texto):
        return "saudacao"

    conceito, _ = buscar_conceito(texto, base_conhecimento)
    if conceito:
        return "conceito"

    produto, _ = buscar_produto(texto, produtos_dict)
    if produto:
        return "produto"

    return "geral"


def perguntar_llm(
    pergunta,
    nome_usuario,
    perfil_dict,
    aporte_atual,
    faltante,
    patrimonio_atual,
    historico_texto,
    produtos_texto,
    conhecimento_texto,
):
    prompt = f"""
Você é Lumi, uma assistente financeira educativa, clara, responsável e objetiva.
Responda em português do Brasil.
Use apenas o contexto fornecido sobre o cliente.
Não invente dados.
Não recomende produtos incompatíveis com o perfil do investidor.
Se faltar informação, admita isso e responda com segurança.
Se a pergunta fugir do tema financeiro, informe com educação que seu foco é finanças pessoais.

CONTEXTO DO CLIENTE:
- Nome: {nome_usuario}
- Perfil: {perfil_dict.get('perfil_investidor', 'Não informado')}
- Renda mensal: R$ {perfil_dict.get('renda_mensal', 0):.2f}
- Patrimônio atual: R$ {patrimonio_atual:.2f}
- Meta de aporte mensal: R$ {perfil_dict.get('meta_aporte_mensal', 0):.2f}
- Aporte atual no mês: R$ {aporte_atual:.2f}
- Faltante para a meta: R$ {faltante:.2f}
- Objetivo principal: {perfil_dict.get('objetivo_principal', 'Não informado')}
- Preferências: {json.dumps(perfil_dict.get('preferencias', {}), ensure_ascii=False)}

HISTÓRICO DE ATENDIMENTO:
{historico_texto}

PRODUTOS DISPONÍVEIS:
{produtos_texto}

CONHECIMENTO FINANCEIRO:
{conhecimento_texto}

PERGUNTA DO USUÁRIO:
{pergunta}
"""

    try:
        resposta = requests.post(
            OLLAMA_URL,
            json={
                "model": MODELO,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "num_predict": 180,
                    "top_k": 40
                },
            },
            timeout=60,
        )
        resposta.raise_for_status()
        conteudo = resposta.json().get("response", "").strip()
        return conteudo if conteudo else None
    except requests.RequestException:
        return None


# ==== INFORMAÇÕES DO CLIENTE ==== #

nome_usuario = obter_nome_usuario(perfil)
meta_aporte = obter_meta_aporte(perfil)
patrimonio_atual = float(perfil.get("patrimonio_total", 0.0))

aporte_atual = calcular_aporte_mes(transacoes)
receitas_mes = calcular_receitas_mes(transacoes)
gastos_mes = calcular_gastos_mes(transacoes)
faltante = max(meta_aporte - aporte_atual, 0.0)
meses_meta = calcular_tempo_meta(patrimonio_atual, aporte_atual)

historico_resumido = resumir_historico(historico)
produtos_resumidos = resumir_produtos(produtos)
conhecimento_resumido = json.dumps(conhecimento_mercado, ensure_ascii=False)


# ==== INTERFACE COM O CLIENTE ==== #

st.title("💡 Lumi")
st.caption("Assistente virtual para controle de gastos e metas financeiras.")

with st.expander("Resumo financeiro do mês"):
    st.write(f"Receitas: R$ {receitas_mes:,.2f}")
    st.write(f"Gastos: R$ {gastos_mes:,.2f}")
    st.write(f"Meta de aporte: R$ {meta_aporte:,.2f}")
    st.write(f"Objetivo principal: {perfil.get('objetivo_principal', 'Não informado')}")
    st.write(f"Tempo estimado para atingir o objetivo: {formatar_tempo_meses(meses_meta)}")

if not st.session_state.boas_vindas_exibida:
    mensagem_inicial = (
        f"Olá, {nome_usuario}! Em que posso te ajudar hoje ?"
    )
    st.session_state.messages.append({"role": "assistant", "content": mensagem_inicial})
    st.session_state.boas_vindas_exibida = True


# ==== CHAT ==== #

if user_input := st.chat_input("Digite sua dúvida financeira..."):
    tipo = classificar_pergunta(user_input, conhecimento_mercado, produtos)

    if tipo == "saudacao":
        resposta = f"Olá, {nome_usuario}! Como posso te ajudar ?"

    elif tipo == "gasto":
        meses_sem_gasto = calcular_tempo_meta(patrimonio_atual, aporte_atual)
        meses_com_gasto = calcular_tempo_meta(patrimonio_atual, max(aporte_atual - 100, 0))

        impacto = 0
        if meses_sem_gasto is not None and meses_com_gasto is not None:
            impacto = meses_com_gasto - meses_sem_gasto

        if faltante > 0:
            resposta = (
                f"{nome_usuario}, se você gastar R$ 100 hoje, sua meta de aporte do mês continuará incompleta: "
                f"ainda faltarão R$ {faltante:.2f}. "
                f"Isso pode atrasar sua meta patrimonial em cerca de {impacto} mês(es). "
                "Minha recomendação é priorizar o investimento antes de aumentar gastos não essenciais."
            )
        else:
            resposta = (
                f"{nome_usuario}, sua meta mensal de aporte já foi cumprida. "
                "Você pode decidir esse gasto com mais tranquilidade, mantendo o controle do seu planejamento financeiro."
            )

    elif tipo == "meta":
        if meses_meta is None:
            resposta = (
                f"{nome_usuario}, com o aporte atual, não foi possível estimar com segurança o tempo até sua meta patrimonial. "
                "Se quiser, posso simular cenários com um aporte mensal maior."
            )
        elif meses_meta == 0:
            resposta = f"{nome_usuario}, parabéns: você já atingiu sua meta patrimonial."
        else:
            resposta = (
                f"{nome_usuario}, faltam R$ {faltante:.2f} para você concluir sua meta mensal de aporte. "
                f"Mantendo o ritmo atual, o tempo estimado para atingir seu objetivo é de {formatar_tempo_meses(meses_meta)}."
            )

    elif tipo == "reserva":
        resposta = (
            f"{nome_usuario}, para sua reserva de emergência, as opções mais indicadas são "
            "Tesouro Selic e CDB com liquidez diária, porque oferecem segurança e acesso rápido ao dinheiro."
        )

    elif tipo == "risco":
        resposta = (
            f"{nome_usuario}, como seu perfil é moderado, Bitcoin e outros ativos de alto risco "
            "não são as opções mais adequadas neste momento. "
            "O mais seguro é priorizar alternativas como Tesouro Selic e CDB com liquidez diária."
        )

    elif tipo == "conceito":
        conceito, dados = buscar_conceito(user_input, conhecimento_mercado)
        resposta = (
            f"{conceito.replace('_', ' ').title()}:\n\n"
            f"Definição: {dados.get('definicao', 'Não informado.')}\n\n"
            f"Exemplo: {dados.get('exemplo', 'Não informado.')}\n\n"
            f"Impacto para o investidor: {dados.get('impacto_investidor', 'Não informado.')}"
        )

    elif tipo == "produto":
        produto, dados = buscar_produto(user_input, produtos)
        resposta = (
            f"{produto}:\n\n"
            f"Categoria: {dados.get('categoria', 'Não informada')}\n"
            f"Risco: {dados.get('risco', 'Não informado')}\n"
            f"Rentabilidade: {dados.get('rentabilidade', 'Não informada')}\n"
            f"Liquidez: {dados.get('liquidez', 'Não informada')}\n"
            f"Restrição: {dados.get('restricao', 'Não informada')}\n"
            f"Indicado para: {dados.get('indicado_para', 'Não informado')}\n\n"
            f"Lumi explica: {dados.get('contexto_lumi', 'Não informado')}"
        )

    elif tipo == "fora_escopo":
        resposta = (
            "Não tenho essa informação. Posso te ajudar com seus gastos, metas de investimento e organização financeira."
        )

    elif tipo == "seguranca":
        resposta = (
            "Não tenho acesso a senhas, dados bancários sigilosos ou informações pessoais sensíveis. "
            "Posso te ajudar com organização financeira, metas e investimentos."
        )

    else:
        resposta = perguntar_llm(
            user_input,
            nome_usuario,
            perfil,
            aporte_atual,
            faltante,
            patrimonio_atual,
            historico_resumido,
            produtos_resumidos,
            conhecimento_resumido,
        )

        if not resposta:
            resposta = (
                "No momento estou com instabilidade técnica no modelo local, "
                "mas ainda posso te ajudar com metas, gastos, reserva de emergência, produtos financeiros e conceitos básicos."
            )

    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": resposta})
    st.session_state.messages = st.session_state.messages[-14:]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.text(msg["content"])
