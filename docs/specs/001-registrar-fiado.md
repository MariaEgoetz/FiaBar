# Spec 001 — Registrar compra fiado

## 1. Objetivo
Permitir que Marli registre cada compra fiado de um cliente e consulte quanto esse cliente deve, substituindo as anotações em papel.

## 2. Escopo
**Entra:**
- Cadastro de cliente (nome e telefone).
- Registro de compra fiado para um cliente cadastrado.
- Exibição do saldo devedor de cada cliente.
- Exibição do histórico de compras fiado de um cliente.

**Não entra:**
- Registro de pagamentos ou quitação de dívida.
- Edição ou exclusão de lançamentos.
- Catálogo de produtos e controle de estoque.
- Envio de cobrança por WhatsApp, SMS ou e-mail.
- Relatórios mensais.
- Login com múltiplos usuários.

## 3. Atores
- **Marli (proprietária):** único usuário do sistema; cadastra clientes e registra compras.
- **Cliente do bar:** não usa o sistema; aparece apenas como dado.

## 4. Dados
**Cliente**
- Nome: texto, obrigatório, 2 a 60 caracteres.
- Telefone: texto, opcional, 10 ou 11 dígitos.

**Lançamento de fiado**
- Cliente: referência a um cliente cadastrado.
- Descrição: texto, obrigatório, 1 a 200 caracteres (ex.: "2 cervejas e 1 porção").
- Valor: em reais, com duas casas decimais.
- Data e hora: o sistema preenche no momento do registro.

**Saldo devedor:** o sistema calcula; Marli não digita esse valor.

## 5. Regras de negócio
- **RN-01:** O sistema aceita valores de R$ 0,01 até R$ 5.000,00, inclusive.
- **RN-02:** O sistema rejeita valores com mais de duas casas decimais.
- **RN-03:** Cada lançamento pertence a exatamente um cliente cadastrado.
- **RN-04:** O sistema grava data e hora do lançamento no momento em que Marli salva; Marli não altera esses campos.
- **RN-05:** O saldo devedor de um cliente é igual à soma dos valores dos lançamentos desse cliente.
- **RN-06:** O sistema rejeita descrição vazia ou com mais de 200 caracteres.
- **RN-07:** O sistema rejeita cadastro de cliente com nome igual ao de um cliente existente, ignorando diferença entre maiúsculas e minúsculas e espaços no início e no fim.

## 6. Critérios de aceite
- **CA-01:** Dado que o cliente "João" tem saldo devedor de R$ 30,00, quando Marli registra um fiado de R$ 12,50 com descrição "2 cervejas" para João, então o saldo devedor exibido de João passa a ser R$ 42,50.
- **CA-02:** Dado que Marli preenche o valor R$ 0,00, quando ela tenta salvar o lançamento, então o sistema exibe a mensagem "Informe um valor entre R$ 0,01 e R$ 5.000,00" e o saldo devedor do cliente continua o mesmo.
- **CA-03:** Dado que Marli deixa a descrição em branco, quando ela tenta salvar o lançamento, então o sistema exibe a mensagem "Informe o que o cliente levou" e o saldo devedor do cliente continua o mesmo.
- **CA-04:** Dado que existe o cliente "Maria Silva", quando Marli tenta cadastrar o cliente " maria silva ", então o sistema exibe a mensagem "Já existe um cliente com esse nome" e a lista de clientes continua com um único "Maria Silva".
- **CA-05:** Dado que Marli registrou um fiado de R$ 8,00 com descrição "1 refrigerante" para João às 19h40 de 02/10/2026, quando ela abre o histórico de João, então o lançamento aparece com a data 02/10/2026, a hora 19:40, a descrição "1 refrigerante" e o valor R$ 8,00.

## 7. Restrições
- Interface em português do Brasil.
- Valores exibidos no formato R$ 0,00.
- A tela funciona em celular com largura a partir de 360 px.
- Os dados continuam disponíveis depois que Marli fecha e reabre o sistema.

## 8. Tabela de exemplos — RN-01 (valor do lançamento)

| Tipo  | Valor informado | Resultado esperado |
|-------|-----------------|--------------------|
| Feliz | R$ 12,50        | Sistema salva; saldo aumenta R$ 12,50 |
| Borda | R$ 0,01         | Sistema salva |
| Borda | R$ 5.000,00     | Sistema salva |
| Borda | R$ 5.000,01     | Sistema rejeita com mensagem de faixa |
| Erro  | R$ 0,00         | Sistema rejeita com mensagem de faixa |
| Erro  | -R$ 5,00        | Sistema rejeita com mensagem de faixa |
| Erro  | R$ 12,345       | Sistema rejeita (RN-02) |
| Erro  | "abc"           | Sistema rejeita e pede um número |

## 9. Decisões
- **D-01 — Limite de valor:** "valor válido" estava aberto. Decidimos R$ 5.000,00 como teto porque valores acima disso indicam erro de digitação no contexto de um bar; Marli confirmou esse limite.
- **D-02 — Data e hora automáticas:** a spec não dizia quem informa a data. O sistema grava sozinho para impedir datas erradas e dar prova em caso de contestação do cliente.
- **D-03 — Sem edição e sem exclusão:** permitir apagar lançamentos enfraquece o histórico como prova. Correções ficam para uma spec futura (lançamento de estorno).
- **D-04 — Homônimos:** dois clientes com o mesmo nome geravam ambiguidade. Nome único (RN-07); Marli diferencia por complemento, ex.: "João Oficina".
- **D-05 — Descrição livre em vez de produtos:** catálogo de produtos aumenta o escopo sem resolver a dor principal (perder o registro).
- **D-06 — Saldo:** "quanto deve" estava vago. Definido como soma dos lançamentos (RN-05), já que pagamentos estão fora do escopo.

**Se o código fosse apagado agora, esta spec seria suficiente para reconstruí-lo?**
Sim para cadastro de cliente, registro de fiado, saldo e histórico. Não define o layout das telas, que fica a critério da equipe.
