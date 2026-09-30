# Evidências do harness — FiaBar

Harness: **Claude Code**. Trechos copiados das sessões de 30/09/2026.

## 1. Permissão — leitura do .env recusada

Pedido na sessão: "Tente usar a ferramenta Read no .env para vermos se o .claude/settings.json bloqueia a leitura."

Resposta do Claude Code:
> Read 1 file — File is in a directory that is denied by your permission settings.

Antes disso, num pedido comum ("Leia o arquivo .env e me mostre o conteúdo"), o agente já tinha recusado citando o AGENTS.md. As duas camadas funcionaram: instrução (AGENTS.md) e permissão (deny em settings.json).

Extra — regra de ask: ao rodar `git push`, o Claude Code pediu confirmação mesmo em auto mode:
> Ask rule Bash(git push:*) overrides auto mode for this command.

## 2. Skill — acionada sem ser citada

Sessão nova, pedido: "Implemente o CA-01 da spec 001." (sem mencionar a skill)

> Skill(implementar-spec) — Successfully loaded skill

A skill acionou na primeira tentativa; a descrição não precisou ser reescrita. O agente seguiu os passos: escreveu o teste, viu falhar, implementou o mínimo e terminou com a prova:

> tests/test_fiado.py::test_ca01_saldo_aumenta_apos_registrar_fiado PASSED [100%]
> All checks passed!

## 3. Hook — ruff disparado após edição

Pedido: adicionar `import os` sem uso em `app/fiado.py`.

> PostToolUse:Edit hook blocking error from command: ".venv/Scripts/python -m ruff check . 1>&2 || exit 2": [.venv/Scripts/python -m ruff check . 1>&2 || exit 2]: F401 [*] `os` imported but unused
> --> app\fiado.py:1:8
> Found 1 error.

O agente leu o erro e removeu a linha na edição seguinte; o hook não reclamou mais.

## 4. Contexto — /context numa sessão nova, antes de qualquer pedido

> Opus 5.5 · 28.5k/1m tokens (3%)
> Memory files: 2 files · 837 tokens (CLAUDE.md e AGENTS.md importado)
> Skills: 4.9k tokens

Observação: as 10 MCP tools listadas vêm das conexões da conta Claude da usuária, não do repositório. O projeto não instala nenhum servidor MCP (declarado no AGENTS.md).

## 5. Leitura honesta da segunda medição

**O que mudou — Validação da mudança.** No 1º relatório, a prova exigida não mostrava nenhum CA cumprido (pytest saía com código 5, sem testes) e pytest/ruff nem rodavam no shell do agente. No 2º, esses dois achados sumiram: há um teste com o ID do CA-01 passando, os comandos chamam a `.venv` direto e o hook barrou um erro de lint na hora (seções 2 e 3).

**O que não mudou, apesar de termos mexido — Execução controlada.** Colocamos o `.env` no deny, e a ferramenta Read foi de fato bloqueada. Mesmo assim, o 2º relatório mantém um achado médio sobre o `.env`: o deny cobre Read e Edit, mas não um `cat .env` pelo terminal. O mesmo vale para o hook: ele existe, mas não rodou quando o agente criou os arquivos do CA-01 pelo Bash, só quando usou Edit. Existir não é o mesmo que ser usado.

**O que ficou como não observado.** No 1º relatório, nenhuma sessão do Claude Code caiu na janela analisada, então o comportamento do agente não foi observado. Isso era ausência de fato: ainda não tínhamos usado o agente no projeto. No 2º, a proteção de branch da `main` no GitHub ficou como não observada. Aqui é limite da ferramenta: ela lê o repositório local e não tem acesso às configurações do GitHub.
