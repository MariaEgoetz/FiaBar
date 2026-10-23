# Diário do agente — Feature 002

## Testes que não contam como ciclo vermelho-verde
- **CA-02** (pagamento total zera o saldo): o teste nasceu verde, porque a implementação do CA-01 já cobria a quitação total. Foi commitado sozinho (`test(002): CA-02 nasceu verde — já coberto pela implementação do CA-01`), sem commit de verde e sem forçar falha. Decisão registrada como D-06 na spec 002.
