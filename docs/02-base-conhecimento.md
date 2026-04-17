# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Função no projeto |
|---------|---------|-------------------|
| `conhecimento_mercado.json` | JSON | Base conceitual para explicar termos como Selic, CDI, liquidez, juros compostos, reserva de emergência e risco. |
| `historico_atendimento.csv` | CSV | Registra interações anteriores do cliente, ajudando a manter continuidade e contexto no atendimento. |
| `perfil_investidor.json` | JSON | Define o perfil do cliente, meta de aporte mensal, objetivo principal, patrimônio atual e preferências de investimento. |
| `produtos_financeiros.json` | JSON | Catálogo de produtos financeiros com informações de risco, liquidez, categoria, restrição e contexto de recomendação. |
| `transacoes.csv` | CSV | Histórico de receitas, gastos e aportes do cliente, usado para cálculos financeiros e análise do mês atual. |

---

## Adaptações nos Dados

Os dados mockados foram adaptados para tornar a Lumi mais coerente com o caso de uso proposto no projeto.

### Principais ajustes realizados
- O arquivo `conhecimento_mercado.json` foi ampliado com conceitos mais úteis para a experiência do agente, como reserva de emergência, renda fixa, Tesouro Selic, CDB, perfil moderado, risco e rentabilidade.
- O arquivo `historico_atendimento.csv` passou a incluir o campo `sentimento`, permitindo registrar o tom das interações anteriores.
- O arquivo `perfil_investidor.json` foi enriquecido com informações como renda mensal, patrimônio total, objetivo principal, nível de tolerância ao risco e preferências de liquidez.
- O arquivo `produtos_financeiros.json` recebeu campos como `categoria`, `indicado_para` e `contexto_lumi`, para facilitar explicações mais personalizadas.
- O arquivo `transacoes.csv` foi organizado com categorias claras de receitas, gastos e investimentos, permitindo simulações simples e análise de comportamento financeiro.

---

## Estratégia de Integração

### Como os dados são carregados
Os arquivos JSON e CSV da pasta `data` são carregados no início da aplicação. Os arquivos CSV são tratados com `pandas`, enquanto os arquivos JSON são lidos com a biblioteca `json`.

Além do carregamento, o sistema realiza validações básicas para garantir que os arquivos possuem as colunas esperadas antes de iniciar o atendimento.

### Como os dados são usados
A base de conhecimento é usada de duas formas:

1. **Regras e cálculos em Python**
- cálculo do aporte realizado no mês
- cálculo de receitas e gastos do mês
- cálculo do valor faltante para a meta mensal
- projeção simples de tempo para atingir a meta patrimonial
- resposta direta para perguntas sobre gasto, meta, reserva, risco e fora de escopo

2. **Contexto para o LLM**
- perfil do investidor
- histórico resumido de atendimento
- resumo dos produtos financeiros
- conceitos do mercado financeiro

Dessa forma, a Lumi não depende exclusivamente do modelo de linguagem para responder perguntas importantes, reduzindo o risco de alucinação.

---

## Exemplo de Contexto Montado

### Perfil do Cliente
- Nome: Dennis
- Profissão: Analista de Dados
- Perfil do investidor: Moderado
- Renda mensal: R$ 5.000,00
- Patrimônio atual: R$ 15.000,00
- Meta de aporte mensal: R$ 500,00
- Objetivo principal: Aposentadoria com renda passiva

### Situação Financeira do Mês
- Aporte realizado: R$ 350,00
- Valor faltante para a meta: R$ 150,00
- Gastos com lazer: R$ 180,00
- Receitas no mês: calculadas a partir do `transacoes.csv`
- Gastos no mês: calculados a partir do `transacoes.csv`

### Conhecimento Disponível
- Conceitos financeiros como Selic, liquidez, CDI, juros compostos e reserva de emergência
- Produtos como Tesouro Selic, CDB com liquidez diária, Tesouro IPCA+ e outros
- Histórico de interações anteriores para dar continuidade ao atendimento

---

## Papel da Base de Conhecimento na Lumi

A base de conhecimento permite que a Lumi:
- personalize respostas com base no perfil do cliente
- explique conceitos financeiros com clareza
- recomende produtos compatíveis com o perfil moderado
- simule impactos de gastos e investimentos
- mantenha consistência e segurança nas respostas

Essa estrutura torna o agente mais confiável, contextualizado e aderente ao objetivo do projeto.
