# Spec 002 — Registrar pagamento

## 1. Objetivo
Permitir que Marli registre quando um cliente paga todo ou parte do fiado, abatendo do saldo devedor.

## 2. Escopo
**Entra:**
- Registro de pagamento, total ou parcial, para um cliente cadastrado.
- Saldo devedor passa a descontar os pagamentos.
- Pagamentos aparecem no histórico do cliente, junto com as compras.

**Não entra:**
- Edição, exclusão ou estorno de pagamento.
- Pagamento maior que o saldo (crédito ou troco).
- Forma de pagamento (Pix, dinheiro, cartão).
- Recibo, juros ou multa.

## 3. Atores
- **Marli (proprietária):** único usuário; registra pagamentos.
- **Cliente do bar:** não usa o sistema; aparece apenas como dado.

## 4. Dados
**Pagamento**
- Cliente: referência a um cliente cadastrado.
- Valor: em reais, com duas casas decimais.
- Data e hora: o sistema preenche no momento do registro.

## 5. Regras de negócio
- **RN-01:** O sistema aceita pagamento a partir de R$ 0,01.
- **RN-02:** O sistema rejeita pagamento maior que o saldo devedor atual do cliente.
- **RN-03:** O sistema rejeita valor com mais de duas casas decimais ou não numérico, com as mesmas mensagens da spec 001 (D-09).
- **RN-04:** O sistema grava data e hora do pagamento no momento em que Marli salva; Marli não altera esses campos.
- **RN-05:** O saldo devedor é a soma das compras menos a soma dos pagamentos do cliente.

## 6. Critérios de aceite
- **CA-01:** Dado que João tem saldo devedor de R$ 42,50, quando Marli registra um pagamento de R$ 20,00 para João, então o saldo devedor exibido passa a ser R$ 22,50.
- **CA-02:** Dado que João tem saldo devedor de R$ 42,50, quando Marli registra um pagamento de R$ 42,50, então o saldo devedor exibido passa a ser R$ 0,00.
- **CA-03:** Dado que João tem saldo devedor de R$ 42,50, quando Marli tenta registrar um pagamento de R$ 50,00, então o sistema exibe "O pagamento não pode ser maior que o saldo devedor" e o saldo continua R$ 42,50.
- **CA-04:** Dado que Marli preenche o valor R$ 0,00, quando tenta salvar o pagamento, então o sistema exibe "Informe um valor maior que zero" e o saldo continua o mesmo.
- **CA-05:** Dado que Marli registrou um pagamento de R$ 20,00 para João às 10h15 de 24/10/2026, quando abre o histórico de João, então aparece uma linha com "Pagamento", a data 24/10/2026, a hora 10:15 e o valor R$ 20,00.
- **CA-06:** Dado que João tem saldo devedor de R$ 42,50, quando Marli abre a tela de João, então a tela exibe um formulário de pagamento com campo Valor e botão 'Registrar pagamento'.

## 7. Restrições
- Interface em português do Brasil.
- Valores exibidos no formato R$ 0,00.
- A tela funciona em celular com largura a partir de 360 px.
- A feature 001 continua funcionando sem alteração de comportamento.

## 8. Tabela de exemplos — RN-02 (saldo devedor de R$ 42,50)

| Tipo  | Valor informado | Resultado esperado |
|-------|-----------------|--------------------|
| Feliz | R$ 20,00        | Sistema salva; saldo vai a R$ 22,50 |
| Borda | R$ 0,01         | Sistema salva; saldo vai a R$ 42,49 |
| Borda | R$ 42,50        | Sistema salva; saldo vai a R$ 0,00 |
| Borda | R$ 42,51        | Sistema rejeita (maior que o saldo) |
| Erro  | R$ 0,00         | Sistema rejeita (valor maior que zero) |
| Erro  | -R$ 5,00        | Sistema rejeita (valor maior que zero) |
| Erro  | R$ 12,345       | Sistema rejeita (RN-03) |
| Erro  | "abc"           | Sistema rejeita (RN-03) |

## 9. Decisões
- **D-01 — Sem crédito:** pagar mais que o saldo geraria saldo negativo e controle de troco, fora do escopo. O sistema rejeita (RN-02).
- **D-02 — Pagamento abate o total:** o pagamento não se liga a uma compra específica, porque Marli cobra o total devido, não item por item.
- **D-03 — Histórico único:** compras e pagamentos ficam na mesma lista, identificados pelo tipo, para servir de prova na cobrança.
- **D-04 — Mensagens de formato:** reaproveitam as da spec 001 (D-09) para o usuário ver sempre o mesmo texto.
- **D-05 — Saldo redefinido:** a RN-05 da spec 001 passa a valer como compras − pagamentos (registrado como D-12 na spec 001).
- **D-06 — CA-02 coberto pelo CA-01:** CA-02 é caso de borda do CA-01 (quitação total); a implementação do CA-01 já o cobria.

**Se o código fosse apagado agora, esta spec seria suficiente para reconstruí-lo?**
Sim para registro de pagamento, saldo e histórico. Não define o layout das telas, que fica a critério da equipe.
