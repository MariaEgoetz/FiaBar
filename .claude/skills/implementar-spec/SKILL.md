---
name: implementar-spec
description: Use quando pedirem para implementar, codar ou construir uma funcionalidade do FiaBar que tenha spec em docs/specs/. Implementa critério por critério, com teste antes do código.
---

# Implementar a partir da spec

1. Leia a spec em `docs/specs/` que corresponde ao pedido. Se não existir spec, pare e avise.
2. Liste os critérios de aceite (CA-xx) e as regras (RN-xx) que o pedido cobre.
3. Para cada CA, escreva um teste em `tests/` com o ID no nome (ex.: `test_ca01_saldo_aumenta`).
4. Rode `.venv\Scripts\python -m pytest` e confirme que os testes novos falham.
5. Implemente o mínimo em `app/` para os testes passarem.
6. Rode `.venv\Scripts\python -m pytest` e `.venv\Scripts\python -m ruff check .`.
7. Prova final: mostre a saída do pytest com os testes passando e a lista dos CA cobertos. Não declare a tarefa concluída sem essa saída.
