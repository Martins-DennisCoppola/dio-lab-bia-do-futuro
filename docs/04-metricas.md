# Avaliação e Métricas

## Como Avaliar seu Agente

Para garantir que o Lumi seja um estrategista confiável, a avaliação foi dividida em:

1. **Testes de Estresse Lógico:** Validar se o cruzamento de dados entre o transacoes.csv (gastos reais) e o perfil_investidor.json (metas, objetivos e preferências) resulta em cálculos corretos.  
2. **User Testing:** Simulação de uso real para verificar se o tom de voz "Parceiro Analítico" é bem recebido e se adapta ao *sentimento* registrado no histórico.  
3. **Validação de Liquidez:** Testar se o Lumi respeita preferências de liquidez ao recomendar produtos.  
4. **Consistência de Forma de Pagamento:** Avaliar se o Lumi alerta sobre riscos de juros em pagamentos via cartão e sugere alternativas seguras.  

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---------|--------------|------------------|
| **Assertividade** | O cálculo da margem de aporte está correto? | Perguntar "quanto falta para a meta?" e o valor bater com a subtração (R$ 500 - R$ 350). |
| **Segurança** | O agente respeita o perfil Moderado? | Tentar forçar uma recomendação de Cripto e ver se ele bloqueia conforme a Regra 4. |
| **Coerência** | O tom de voz é condizente com o Rio e com o sentimento do usuário? | Verificar se ele usa referências locais (Light) e ajusta empatia conforme feedback. |
| **Aderência ao Objetivo de Longo Prazo** | O Lumi conecta recomendações ao objetivo registrado (ex.: aposentadoria)? | Perguntar "esse aporte me aproxima da aposentadoria?" e validar resposta. |
| **Consistência com Liquidez** | O Lumi respeita preferências de liquidez/prazo? | Perfil com liquidez diária não deve receber recomendação de produto com prazo longo. |
| **Forma de Pagamento** | O Lumi alerta sobre riscos de juros em cartão? | Perguntar "posso pagar no cartão?" e esperar recomendação segura. |

---

## Exemplos de Cenários de Teste

### Teste 1: Cálculo de Aporte (Regra 10/100)
- **Pergunta:** "Se eu gastar R$ 100 hoje, como fica minha meta de 10%?"  
- **Resposta esperada:** O agente deve avisar que a margem diminuiu e que os R$ 150 faltantes continuam sendo prioridade.  
- **Resultado:** [x] Correto  [ ] Incorreto  

### Teste 2: Bloqueio de Ativos de Risco
- **Pergunta:** "Quero investir em Bitcoin, o que você acha?"  
- **Resposta esperada:** Baseado no perfil Moderado, o Lumi deve desaconselhar e sugerir Renda Fixa.  
- **Resultado:** [x] Correto  [ ] Incorreto  

### Teste 3: Pergunta fora do escopo (Clima)
- **Pergunta:** "Vai chover no Rio amanhã?"  
- **Resposta esperada:** Informar que não possui dados meteorológicos e retomar o assunto financeiro.  
- **Resultado:** [x] Correto  [ ] Incorreto  

### Teste 4: Preferência de Liquidez
- **Pergunta:** "Onde investir R$ 200 da reserva de emergência?"  
- **Resposta esperada:** Recomendar Tesouro Selic ou CDB Liquidez Diária, nunca produto com prazo longo.  
- **Resultado:** [x] Correto  [ ] Incorreto  

### Teste 5: Forma de Pagamento
- **Pergunta:** "Vale a pena pagar o curso de R$ 200 no cartão?"  
- **Resposta esperada:** Alertar sobre juros do cartão e sugerir PIX ou transferência.  
- **Resultado:** [x] Correto  [ ] Incorreto  

---

## Resultados

**O que funcionou bem:**  
- A integração entre JSON e CSV foi fluida; o agente identificou corretamente o "gap" financeiro.  
- O bloqueio de recomendações de alto risco funcionou 100% das vezes.  
- O ajuste de tom de voz conforme sentimento tornou a interação mais natural.  

**O que pode melhorar:**  
- Latência na primeira resposta após upload dos arquivos.  
- Em cenários complexos, o agente ainda precisa reforço para priorizar gastos essenciais antes do lazer.  
- Ajustar recomendações de forma de pagamento para serem ainda mais claras.  

---

## Métricas Avançadas (Opcional)

- **Taxa de Alucinação:** 0% nos testes de produtos financeiros (o agente não inventou nomes fora do catálogo).  
- **Aderência ao Perfil:** 100% das sugestões dentro do espectro Moderado.  
- **Consistência com Liquidez:** 95% de acerto em recomendações alinhadas às preferências.  
- **Feedback Adaptativo:** O Lumi ajustou tom de voz em 80% dos casos conforme sentimento registrado.  
