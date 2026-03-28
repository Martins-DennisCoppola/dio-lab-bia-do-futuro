# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `conhecimento_mercado.json` | JSON | Fornece a base técnica sobre Selic e Juros Compostos (Enriquecido via Hugging Face). |
| `historico_atendimento.csv` | CSV | Mantém a continuidade da jornada financeira e progresso das metas. |
| `perfil_investidor.json` | JSON | Define a meta de 10% de aporte mensal e o perfil moderado do Dennis. |
| `produtos_financeiros.json` | JSON | Catálogo de investimentos com curadoria para a estratégia de dobrar a renda. |
| `transacoes.csv` | CSV | "Registro de gastos reais (Energia, Gás, Alimentação) para cálculo de sobra de caixa." |

> [!TIP]
> Hugging Face Integration: Utilizamos o DNA de datasets como o Financial PhraseBank para garantir que as definições técnicas de "Juros Compostos" e "Selic" no arquivo conhecimento_mercado.json sigam padrões rigorosos do setor.
---

## Adaptações nos Dados

> Os dados originais foram expandidos para incluir a "Regra de Ouro dos 10%".

**Categorização Semântica:** Substituímos nomes de estabelecimentos por categorias puras (Energia, Gás, Alimentação) para facilitar a análise da IA.

**Camada de Contexto:** Adicionamos o campo contexto_lumi no JSON de produtos, permitindo que a IA explique o "porquê" de cada recomendação para o perfil do Dennis.

**Remoção de Ruído:** Optamos por não incluir gastos complexos como veículos próprios, focando na eficiência do transporte por aplicativo/público.

---

## Estratégia de Integração

### Como os dados são carregados?
> Os arquivos JSON e CSV localizados na pasta /data são processados via scripts Python (utilizando a biblioteca pandas para os CSVs e json para os perfis) e convertidos em blocos de texto estruturado no início de cada sessão.

### Como os dados são usados no prompt?
> Os arquivos JSON e CSV localizados na pasta /data são processados via scripts Python (utilizando a biblioteca pandas para os CSVs e json para os perfis) e convertidos em blocos de texto estruturado no início de cada sessão.
---

## Exemplo de Contexto Montado

> DADOS DO ESTRATEGISTA:
- Nome: Dennis (Analista de Dados)
- Meta Mensal: R$ 500,00 (10% do salário)
- Aporte Realizado: R$ 350,00

>ANÁLISE DE FLUXO (MARÇO/2026):
- Moradia (Aluguel/Energia/Gás): R$ 1.835,00
- Lazer Atual: R$ 235,90
- Status: Faltam R$ 150,00 para bater a meta de 10%.

>CONHECIMENTO DISPONÍVEL:
- Recomendação: Tesouro Selic (Baixo risco, ideal para completar o aporte).
