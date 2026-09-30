# Diário do agente — Feature 001

## Nível do slider de autonomia
T1 a T3: nível 4 (tarefa multi-arquivo), uma tarefa por sessão, com revisão humana entre elas. T4 a T11: continuamos no nível 4, mas com oito tarefas em um só pedido e um commit por tarefa. Confiamos nos sensores para isso: a skill exige o teste falhando antes do código, o hook roda o ruff a cada edição, e o agente tinha ordem de parar se um teste só passasse mudando a spec. Não subimos ao nível 5 porque o plano foi escrito e revisado por nós antes de qualquer código.

## Uma vez em que o agente errou
No T8, o teste do RN-04 comparava horários sem fuso horário. O ruff (lint) rejeitou, e o agente corrigiu a forma de ler o relógio sem afrouxar o teste, que continua exigindo que o horário salvo esteja a até 60 segundos do atual. Mecanismo que pegou: lint, rodado pelo agente como prova da tarefa. O hook não disparou porque os arquivos foram alterados pelo terminal.

Um erro que nenhum mecanismo pegou: digitar "NaN" no campo de valor ainda derruba o servidor (erro 500). Nenhum teste cobre esse caso porque a spec não o previa. O agente apontou isso no resumo final, mas não corrigiu por estar fora do plano.

## Uma vez em que o agente perguntou antes de assumir
No T7, a spec e o plano não diziam qual mensagem exibir para descrição acima de 200 caracteres. O agente parou e perguntou, oferecendo opções. Escolhemos "A descrição deve ter no máximo 200 caracteres", registrada como D-10 na spec.

## O que mudaríamos no harness
- Hook: o PostToolUse só roda em Edit e Write, e arquivos criados pelo terminal escapam dele. Adicionaríamos um hook Stop que roda pytest e ruff ao fim de cada resposta.
- Permissões: o deny cobre só Read e Edit do .env. Adicionaríamos deny para leituras pelo terminal (cat, type, Get-Content).
- Skill: incluir um passo explícito "se a spec não define uma mensagem ou limite, pergunte antes de implementar". Funcionou pelo AGENTS.md, mas na skill fica garantido.

Já aplicamos o hook Stop e o deny pelo terminal: https://github.com/MariaEgoetz/FiaBar/commit/a9f71ceb9ff9ebd95a2f18704228203596aef358

## Critérios atendidos
CA-01 a CA-05 e RN-01 a RN-07 cobertos por 25 testes passando. A checagem de 360 px foi manual, na lista de clientes e na tela do cliente. O CA-01 foi implementado antes do plano, durante o teste do harness, e está registrado como T0. Nenhum teste foi apagado ou afrouxado.

Observação de uso: a tela do cliente não tem link de volta para a lista. A spec não pede, então não é falha, mas entra como candidata a uma próxima spec.
