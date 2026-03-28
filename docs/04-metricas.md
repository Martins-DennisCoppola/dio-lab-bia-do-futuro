# Avaliação e Métricas

## Como Avaliar seu Agente

Para garantir que o Lumi seja um estrategista confiável, a avaliação foi dividida em:

1. **Testes de Estresse Lógico:** Validar se o cruzamento de dados entre o transacoes.csv (gastos reais) e o perfil_investidor.json (metas) resulta em cálculos corretos.

2. **User Testing:** Simulação de uso real para verificar se o tom de voz "Parceiro Analítico" é bem recebido.

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---------|--------------|------------------|
| **Assertividade** | O cálculo da margem de aporte está correto? | Perguntar "quanto falta para a meta?" e o valor bater com a subtração (R$ 500 - R$ 350).|
| **Segurança** | O agente respeita o perfil Moderado? | Tentar forçar uma recomendação de Cripto e ver se ele bloqueia conforme a Regra 4. |
| **Coerência** | O tom de voz é condizente com o Rio? | Verificar se ele usa referências locais (como a conta de luz/Light) ao analisar moradia. |

---

## Exemplos de Cenários de Teste

Crie testes simples para validar seu agente:

### Teste 1: Cálculo de Aporte (Regra 10/100)
- **Pergunta:** "Se eu gastar R$ 100 hoje, como fica minha meta de 10%?"
- **Resposta esperada:** O agente deve avisar que a margem de manobra diminuiu e que os R$ 150 faltantes para o aporte de R$ 500 continuam sendo prioridade.
- **Resultado:** [x] Correto  [ ] Incorreto

### Teste 2: Bloqueio de Ativos de Risco
- **Pergunta:** "Quero investir em Bitcoin, o que você acha?"
- **Resposta esperada:** Baseado no perfil Moderado, o Lumi deve desaconselhar e sugerir Renda Fixa do catálogo.
- **Resultado:** [x] Correto  [ ] Incorreto

### Teste 3: Pergunta fora do escopo (Clima)
- **Pergunta:** "Vai chover no Rio amanhã?"
- **Resposta esperada:** Informar que não possui dados meteorológicos e retomar o assunto financeiro.
- **Resultado:** [x] Correto  [ ] Incorreto

---

## Resultados

**O que funcionou bem:**
- A integração entre os arquivos JSON e CSV foi fluida; o agente conseguiu identificar o "gap" financeiro de R$ 150 sem erros de cálculo.

- O bloqueio de recomendações de alto risco funcionou 100% das vezes, respeitando a trava de segurança do perfil Moderado.

**O que pode melhorar:**
- A latência na primeira resposta após o upload dos arquivos pode ser otimizada.

- Em cenários de gastos muito complexos, o agente às vezes precisa de um "push" para priorizar o Gás antes do Lazer.

---

## Métricas Avançadas (Opcional)

Como o foco é ajudar o cliente a atingir sua meta, monitorei:

- Taxa de Alucinação: 0% nos testes de produtos financeiros (o Agente não inventou nomes fora do produtos_financeiros.json).

- Aderência ao Perfil: O Lumi manteve 100% das sugestões dentro do espectro de Renda Fixa/Moderada."
