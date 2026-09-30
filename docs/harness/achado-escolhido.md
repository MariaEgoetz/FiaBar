# Achado escolhido — Relatório 1 do Better Harness

Relatório: `docs/harness/relatorio-1.html` (Better Harness 0.7.0-alpha2, Claude Code, janela 2026-08-31 a 2026-09-30).

## Achados do relatório

1. **Médio — O agente ainda consegue ler o `.env` apesar da regra do AGENTS.md.** A proibição existia só como texto na seção Segurança do `AGENTS.md`; o `.gitignore` impede apenas o commit do arquivo, não a leitura pelo agente.
2. **Baixo — A prova exigida pelo AGENTS.md não mostra se algum CA da spec foi cumprido.** `pytest` sai com código 5 (sem testes) e `ruff check .` passa sem arquivos Python; nada liga cada CA-xx a um teste nomeado.
3. **Baixo — `pytest` e `ruff` não rodam como escritos no shell do agente.** Eles só existem em `.venv/Scripts` e a ativação da venv não persiste entre chamadas do Claude Code.

## Achado escolhido

Escolhemos o **achado 1** (o agente consegue ler o `.env`) por ser o de maior impacto e o único cobrado na correção. Os achados 2 e 3 ficam registrados e não foram corrigidos.

## Reparo aplicado

Criado `.claude/settings.json` versionado, contendo apenas `permissions.deny` com:

- `Read(./.env)` — nega a leitura do `.env` pelas ferramentas de arquivo do Claude Code;
- `Edit(./.env)` — nega a edição do `.env`.

A regra em texto da seção Segurança do `AGENTS.md` foi mantida.
