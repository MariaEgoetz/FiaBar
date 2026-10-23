---
name: implementar-spec
description: Use quando pedirem para implementar, codar ou construir uma funcionalidade do FiaBar que tenha spec em docs/specs/. Implementa critério por critério, com teste antes do código.
---

# Implementar a partir da spec

1. Leia a spec em `docs/specs/` que corresponde ao pedido. Se não existir spec, pare e avise.
2. Liste os critérios de aceite (CA-xx) e as regras (RN-xx) que o pedido cobre.
3. Se a spec não define uma mensagem ou um limite de que a implementação precisa, pare e pergunte antes de implementar.
4. Siga o ciclo vermelho → verde → refatorar, **um CA por vez**:
   1. **Vermelho:** escreva um teste em `tests/` com o ID no nome (ex.: `test_ca01_saldo_aumenta`). Rode `.venv/Scripts/python -m pytest` e confirme que o teste novo falha. Commite só o teste: `test(NNN): CA-xx vermelho — <resumo>`.
   2. **Verde:** implemente o mínimo em `app/` para o teste passar. Rode `.venv/Scripts/python -m pytest` e confirme que a suíte inteira passa. Rode `.venv/Scripts/python -m ruff check .`. Commite: `feat(NNN): CA-xx verde — <resumo>`.
   3. **Refatorar:** se houver o que limpar, limpe sem mudar comportamento e rode a suíte de novo.
   4. Passe para o próximo CA.
5. Nunca apague, pule, desative ou altere um teste para fazê-lo passar. Se achar que o teste está errado, pare e pergunte.
6. Prova final: mostre a saída do pytest com os testes passando e a lista dos CA cobertos. Não declare a tarefa concluída sem essa saída.
