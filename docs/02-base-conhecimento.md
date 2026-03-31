# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Para que serve no Lumi |
|---------|---------|----------------------|
| `conhecimento_mercado.json` | JSON | Fornece a base técnica sobre Selic, Juros Compostos, CDI, liquidez e diversificação (enriquecido via Hugging Face). |
| `historico_atendimento.csv` | CSV | Mantém a continuidade da jornada financeira, progresso das metas e agora inclui o campo **sentimento** para ajustar o tom de voz. |
| `perfil_investidor.json` | JSON | Define a meta de 10% de aporte mensal, perfil moderado do Dennis, além de **objetivo_longo_prazo** e **preferencias** (liquidez, prazo, restrições). |
| `produtos_financeiros.json` | JSON | Catálogo de investimentos com curadoria para a estratégia de dobrar a renda, incluindo campos de **liquidez** e **restricao** por perfil. |
| `transacoes.csv` | CSV | Registro de gastos reais (Energia, Gás, Alimentação, Educação, Seguros) e receitas extras, com campo adicional de **forma de pagamento**. |

---

## Adaptações nos Dados

> Os dados originais foram expandidos para incluir a "Regra de Ouro dos 10%" e novos campos de contexto.

**Categorização Semântica:** Substituímos nomes de estabelecimentos por categorias puras (Energia, Gás, Alimentação, Educação, Seguros) para facilitar a análise da IA.  

**Camada de Contexto:** Adicionamos o campo **contexto_lumi** no JSON de produtos, permitindo que a IA explique o "porquê" de cada recomendação para o perfil do Dennis.  

**Feedback e Sentimento:** O histórico de atendimento agora registra o sentimento (positivo, neutro, negativo), permitindo que o Lumi ajuste o tom de voz.  

**Objetivos e Preferências:** O perfil do investidor inclui objetivos de longo prazo (ex.: aposentadoria) e preferências de liquidez/prazo, garantindo recomendações personalizadas.  

**Remoção de Ruído:** Optamos por não incluir gastos complexos como veículos próprios, focando na eficiência do transporte por aplicativo/público.  

---

## Estratégia de Integração

### Como os dados são carregados?
> Os arquivos JSON e CSV localizados na pasta /data são processados via scripts Python (utilizando a biblioteca pandas para os CSVs e json para os perfis) e convertidos em blocos de texto estruturado no início de cada sessão.  
> Agora, os scripts também validam consistência dos novos campos (ex.: liquidez, forma de pagamento, sentimento).

### Como os dados são usados no prompt?
> Os arquivos são transformados em contexto textual para o LLM, permitindo que o Lumi:  
- Calcule sobras de caixa e aporte necessário.  
- Ajuste recomendações conforme liquidez e perfil.  
- Adapte comunicação conforme sentimento registrado.  
- Conecte decisões financeiras aos objetivos de longo prazo.  

---

## Exemplo de Contexto Montado

> DADOS DO ESTRATEGISTA:  
- Nome: Dennis (Analista de Dados)  
- Meta Mensal: R$ 500,00 (10% do salário)  
- Aporte Realizado: R$ 350,00  
- Objetivo de Longo Prazo: Aposentadoria com renda passiva  
- Preferência: Liquidez diária, evita ativos de alto risco  

> ANÁLISE DE FLUXO (MARÇO/2026):  
- Moradia (Aluguel/Energia/Gás): R$ 1.835,00  
- Lazer Atual: R$ 235,90  
- Educação: R$ 200,00  
- Seguros: R$ 300,00  
- Status: Faltam R$ 150,00 para bater a meta de 10%.  

> CONHECIMENTO DISPONÍVEL:  
- Recomendação: Tesouro Selic (Baixo risco, liquidez diária, ideal para completar o aporte).  
- Observação: Última interação registrada como **positiva**, ajustar comunicação para tom encorajador.  
