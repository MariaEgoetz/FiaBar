# Plano — Spec 001 (Registrar compra fiado)

Spec: `docs/specs/001-registrar-fiado.md`. Cada tarefa é feita em uma sessão e fechada com um commit.
Prova de toda tarefa: `.venv/Scripts/python -m pytest` e `.venv/Scripts/python -m ruff check .` passando.
Tarefas de código seguem a skill `implementar-spec`: primeiro o teste falhando, depois o código mínimo.

## Decisões da revisão
- P1 (T3): nome fora de 2 a 60 caracteres exibe "O nome deve ter entre 2 e 60 caracteres".
- P2 (T3): o telefone ignora pontuação e espaços; "(64) 99999-9999" conta como 11 dígitos. Fora de 10 ou 11 dígitos exibe "Informe um telefone com 10 ou 11 dígitos".
- P3 (T6): mais de duas casas exibe "Use no máximo duas casas decimais"; valor não numérico exibe "Informe um valor numérico, ex.: 12,50".

## T0 — CA-01 já implementado (registro)
- **Atende:** CA-01, RN-05 (parcial: saldo é a soma dos lançamentos).
- **Situação:** implementado antes deste plano, durante o teste do harness, no commit `8439979` (feat(001): implementa CA-01 via skill implementar-spec).
- **Arquivos:** `app/__init__.py`, `app/db.py`, `app/fiado.py`, `app/templates/cliente.html`, `tests/conftest.py`, `tests/test_fiado.py`.
- **Teste que prova:** `test_ca01_saldo_aumenta_apos_registrar_fiado`.
- **Commit:** nenhum novo. Esta tarefa só registra o que já existe.

## T1 — Fixar versões no requirements.txt
- **Atende:** reprodutibilidade do ambiente (nenhum CA/RN).
- **Arquivos:** `requirements.txt` (`flask==3.1.3`, `pytest==9.1.1`, `ruff==0.16.9`, as versões hoje instaladas na venv).
- **Prova:** `.venv/Scripts/python -m pip install -r requirements.txt` não muda nada e `.venv/Scripts/python -m pytest` segue verde.
- **Commit:** `chore: fixa versões no requirements.txt`.

## T2 — Comando de rodar sem ativar a venv
- **Atende:** achado 3 do relatório 1 do harness (nenhum CA/RN).
- **Arquivos:** `AGENTS.md`, na linha "Rodar", que passa a ser `.venv/Scripts/python -m flask --app app run`, no mesmo padrão de Testar e Lint.
- **Prova:** em um shell sem a venv ativada, o comando sobe o servidor e `GET /clientes/1` responde 404 (banco vazio, então o servidor está de pé).
- **Commit:** `docs: comando de rodar do AGENTS.md usa o python da venv`.

## T3 — Cadastro e lista de clientes
- **Atende:** escopo "Cadastro de cliente" e seção 4, Dados do Cliente (nome com 2 a 60 caracteres; telefone opcional com 10 ou 11 dígitos). Mensagens conforme P1 e P2.
- **Arquivos:** `app/fiado.py` (rotas de listar e cadastrar clientes), `app/templates/clientes.html` (novo), `tests/test_fiado.py`.
- **Testes que provam:** `test_cadastrar_cliente_aparece_na_lista`, `test_nome_fora_do_tamanho_rejeitado` (1 e 61 caracteres; mensagem de P1), `test_telefone_invalido_rejeitado` (9 e 12 dígitos; mensagem de P2), `test_telefone_com_pontuacao_aceito` ("(64) 99999-9999"), `test_telefone_vazio_aceito`.
- **Commit:** `feat(001): cadastro e lista de clientes`.

## T4 — Nome de cliente único
- **Atende:** CA-04, RN-07. Depende de T3.
- **Arquivos:** `app/fiado.py` (compara nomes sem diferença de maiúsculas/minúsculas e sem espaços nas pontas), `app/templates/clientes.html` (exibe a mensagem), `tests/test_fiado.py`.
- **Teste que prova:** `test_ca04_nome_duplicado_rejeitado`: com "Maria Silva" cadastrada, cadastrar " maria silva " exibe "Já existe um cliente com esse nome" e a lista mostra um único "Maria Silva".
- **Commit:** `feat(001): CA-04 rejeita cliente com nome repetido`.

## T5 — Faixa de valor do lançamento
- **Atende:** CA-02, RN-01 e as linhas Feliz/Borda/Erro de faixa da tabela da seção 8.
- **Arquivos:** `app/fiado.py` (valida a faixa e, no erro, re-renderiza a tela do cliente com a mensagem), `app/templates/cliente.html` (exibe a mensagem), `tests/test_fiado.py`.
- **Testes que provam:** `test_ca02_valor_zero_rejeitado` (mensagem "Informe um valor entre R$ 0,01 e R$ 5.000,00" e saldo inalterado); `test_rn01_faixa_de_valor` parametrizado: 0,01 e 5.000,00 salvam; 5.000,01, 0,00 e -5,00 são rejeitados.
- **Commit:** `feat(001): CA-02 valida faixa de valor`.

## T6 — Formato do valor
- **Atende:** RN-02 e as linhas "12,345" e "abc" da tabela da seção 8. Mensagens conforme P3.
- **Arquivos:** `app/fiado.py` (rejeita mais de duas casas e valor não numérico; o "abc" hoje gera erro 500), `tests/test_fiado.py`.
- **Testes que provam:** `test_rn02_mais_de_duas_casas_rejeitado` ("Use no máximo duas casas decimais"), `test_valor_nao_numerico_rejeitado` ("Informe um valor numérico, ex.: 12,50"). Os dois checam também o saldo inalterado.
- **Commit:** `feat(001): RN-02 valida formato do valor`.

## T7 — Descrição obrigatória
- **Atende:** CA-03, RN-06.
- **Arquivos:** `app/fiado.py`, `tests/test_fiado.py`.
- **Testes que provam:** `test_ca03_descricao_em_branco_rejeitada` (mensagem "Informe o que o cliente levou" e saldo inalterado); `test_rn06_descricao_acima_de_200_rejeitada` (201 caracteres são rejeitados e 200 são aceitos).
- **Commit:** `feat(001): CA-03 valida descrição`.

## T8 — Histórico de lançamentos
- **Atende:** CA-05, RN-04, escopo "histórico de compras".
- **Arquivos:** `app/fiado.py` (busca os lançamentos do cliente e formata data dd/mm/aaaa e hora hh:mm), `app/templates/cliente.html` (lista do histórico), `tests/test_fiado.py`.
- **Testes que provam:** `test_ca05_historico_mostra_data_hora_descricao_valor`: lançamento gravado com `criado_em = 2026-10-02 19:40:00`; a tela mostra "02/10/2026", "19:40", "1 refrigerante" e "R$ 8,00". `test_rn04_data_hora_preenchida_pelo_sistema`: um POST com campo `criado_em` no formulário é ignorado e o lançamento sai com a data e hora atuais.
- **Commit:** `feat(001): CA-05 exibe histórico do cliente`.

## T9 — Lançamento só para cliente cadastrado
- **Atende:** RN-03. `buscar_cliente` já devolve 404; falta o teste.
- **Arquivos:** `tests/test_fiado.py`.
- **Teste que prova:** `test_rn03_fiado_para_cliente_inexistente_retorna_404`, que também confere que nenhum lançamento foi gravado.
- **Commit:** `test(001): RN-03 cobre cliente inexistente`.

## T10 — Restrições da seção 7
- **Atende:** a restrição de persistência, o formato R$ 0,00 e a tela a partir de 360 px.
- **Arquivos:** `tests/test_fiado.py`. Templates só se a checagem manual achar problema.
- **Provas:** `test_dados_persistem_apos_reabrir` (dois `create_app` com o mesmo arquivo de banco); `test_formatar_reais` (0,01 → "R$ 0,01"; 5000 → "R$ 5.000,00"); checagem manual no DevTools a 360 px de largura, registrada no commit.
- **Commit:** `test(001): cobre restrições da seção 7`.
- **Checagem manual de 360 px:** feita por Maria Eduarda em 30/09/2026, no DevTools a 360 px de largura, na lista de clientes (`/clientes`) e na tela do cliente (`/clientes/<id>`). Tudo cabe sem cortar e sem rolagem lateral; nenhum template precisou mudar.

## T11 — Atualizar a spec 001
- **Atende:** P1, P2 e P3 (Decisões da revisão). Mexe no texto da RN-02, na seção 4 (Dados do Cliente) e na tabela da seção 8.
- **Arquivos:** `docs/specs/001-registrar-fiado.md`: novas decisões D-07 (mensagem do nome, P1), D-08 (telefone ignora pontuação e espaços, e sua mensagem, P2) e D-09 (mensagens de casas decimais e de valor não numérico, P3); a seção 4 e a RN-02 passam a citar as mensagens; a tabela da seção 8 troca "Sistema rejeita (RN-02)" e "pede um número" pelas mensagens exatas.
- **Prova:** revisão do diff. As mensagens da spec são iguais às das Decisões da revisão e às verificadas nos testes de T3 e T6. `.venv/Scripts/python -m pytest` segue verde.
- **Commit:** `spec(001): registra mensagens de validação decididas no plano`.

## Cobertura final
| CA/RN | Tarefa |
|-------|--------|
| CA-01, RN-05 | T0 |
| CA-02, RN-01 | T5 |
| RN-02 | T6 |
| CA-03, RN-06 | T7 |
| CA-04, RN-07 | T4 |
| CA-05, RN-04 | T8 |
| RN-03 | T9 |

## Revisão da equipe
Revisado por Maria Eduarda Goetz Maia em 30/09/2026, antes de qualquer código novo. As pendências P1 a P3 foram fechadas nesta revisão (ver "Decisões da revisão").
