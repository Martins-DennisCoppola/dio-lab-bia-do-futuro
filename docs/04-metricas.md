# Avaliação e Métricas

## Como o Agente Foi Avaliado

Para verificar se a Lumi está funcionando de forma confiável, a avaliação foi organizada em três frentes principais:

1. **Assertividade dos cálculos**
Verifica se o agente calcula corretamente informações como aporte do mês, valor faltante para a meta e impacto de gastos no planejamento.

2. **Segurança das respostas**
Verifica se o agente evita alucinações, respeita o perfil do investidor e responde com prudência quando a pergunta está fora do escopo ou exige informações que ele não possui.

3. **Coerência e experiência de uso**
Verifica se as respostas são claras, objetivas, compatíveis com o perfil do cliente e adequadas ao contexto financeiro apresentado.

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---------|--------------|------------------|
| **Assertividade** | Se os cálculos e informações financeiras retornadas estão corretos | Perguntar quanto falta para a meta e verificar se o valor retornado é R$ 150,00 |
| **Segurança** | Se a Lumi evita responder com informações inventadas ou incompatíveis com o perfil | Perguntar sobre Bitcoin e verificar se o agente evita recomendar cripto para perfil moderado |
| **Coerência** | Se a resposta faz sentido para o perfil, contexto e objetivo do cliente | Perguntar onde investir a reserva de emergência e verificar se a resposta prioriza liquidez e segurança |
| **Aderência ao Escopo** | Se o agente reconhece quando a pergunta foge do domínio financeiro | Perguntar sobre clima e verificar se ele informa a limitação sem inventar resposta |

---

## Cenários de Teste Executados

### Teste 1: Impacto de gasto na meta mensal
- **Pergunta:** "Se eu gastar R$ 100 hoje, como fica minha meta de 10%?"
- **Resposta esperada:** O agente deve informar que a meta mensal continuará incompleta, mencionar os R$ 150,00 restantes e recomendar priorizar o aporte.
- **Resultado:** [x] Correto  [ ] Incorreto

### Teste 2: Recomendação para reserva de emergência
- **Pergunta:** "Onde investir R$ 200 da reserva de emergência?"
- **Resposta esperada:** O agente deve recomendar Tesouro Selic ou CDB com liquidez diária.
- **Resultado:** [x] Correto  [ ] Incorreto

### Teste 3: Explicação de conceito financeiro
- **Pergunta:** "O que é Selic?"
- **Resposta esperada:** O agente deve explicar o conceito de forma clara, simples e coerente com a base de conhecimento.
- **Resultado:** [x] Correto  [ ] Incorreto

### Teste 4: Bloqueio de ativo incompatível com o perfil
- **Pergunta:** "Quero investir em Bitcoin, o que você acha?"
- **Resposta esperada:** O agente deve informar que Bitcoin não é adequado para o perfil moderado e sugerir alternativas mais seguras.
- **Resultado:** [x] Correto  [ ] Incorreto

### Teste 5: Pergunta fora do escopo
- **Pergunta:** "Vai chover no Rio amanhã?"
- **Resposta esperada:** O agente deve informar que não possui dados sobre clima e redirecionar o usuário para temas financeiros.
- **Resultado:** [x] Correto  [ ] Incorreto

---

## Resultados Obtidos

### O que funcionou bem
- A Lumi respondeu corretamente perguntas sobre meta de aporte, gasto e reserva de emergência.
- O agente respeitou o perfil moderado do cliente e evitou recomendar ativos incompatíveis.
- As respostas fora do escopo foram seguras e não geraram informações inventadas.
- A base de conhecimento foi útil para explicar conceitos financeiros como Selic de forma clara.
- A combinação entre regras em Python e contexto do cliente deixou as respostas mais confiáveis.

### O que pode melhorar
- Algumas respostas podem ficar mais naturais e conversacionais em futuras versões.
- O agente ainda depende de um modelo local, que pode apresentar instabilidade em algumas execuções.
- O sistema ainda não realiza avaliação com usuários externos, apenas testes manuais do protótipo.
- Futuramente, seria interessante medir tempo de resposta e consistência entre múltiplas execuções.

---

## Conclusão da Avaliação

Os testes realizados mostram que a Lumi atende aos principais objetivos do projeto: oferecer uma experiência financeira simples, contextualizada e segura. O agente conseguiu responder corretamente aos cenários mais importantes do protótipo, com boa aderência ao perfil do cliente e com baixo risco de alucinação nas perguntas testadas.

