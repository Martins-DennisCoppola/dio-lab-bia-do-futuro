# Avaliação e Métricas

## Como Avaliar seu Agente

Para garantir que o Lumi seja um estrategista confiável, a avaliação foi dividida em:

1. **Testes de Estresse Lógico:** Validar se o cruzamento de dados entre o transacoes.csv (gastos reais) e o perfil_investidor.json (metas, objetivos e preferências) resulta em cálculos corretos.  
2. **User Testing:** Simulação de uso real para verificar se o tom de voz "Parceiro Analítico" é bem recebido e se adapta ao *sentimento* registrado no histórico.  
3. **Validação de Liquidez:** Testar se o Lumi respeita preferências de liquidez ao recomendar produtos.  

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---------|--------------|------------------|
| **Assertividade** | O cálculo da margem de aporte está correto? | Perguntar "quanto falta para a meta?" e o valor bater com a subtração (R$ 500 - R$ 350). |
| **Segurança** | O agente respeita o perfil Moderado? | Tentar forçar uma recomendação de Cripto e ver se ele bloqueia conforme a Regra 4. |
| **Coerência** | O tom de voz é condizente com o Rio e com o sentimento do usuário? | Verificar se ele usa referências locais (Light) e ajusta empatia conforme feedback. |
| **Aderência ao Objetivo de Longo Prazo** | O Lumi conecta recomendações ao objetivo registrado (ex.: aposentadoria)? | Perguntar "esse aporte me aproxima da aposentadoria?" e validar resposta. |

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

---

## Resultados

**O que funcionou bem:**  
- 
- 
- 

**O que pode melhorar:**  
- 
-  
- 

---
