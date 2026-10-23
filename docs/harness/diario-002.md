# Diário do agente — Feature 002 (Registrar pagamento)

## Um critério em que o vermelho revelou uma ambiguidade
No CA-03 e no CA-04, ao escrever o teste, o agente percebeu que "R$ 42,50" também aparecia em outra linha da página, então um teste que só procurasse esse texto passaria mesmo com o saldo errado. A spec dizia "o saldo devedor exibido" sem dizer qual valor da tela é o saldo. Os testes passaram a conferir o rótulo "Saldo devedor:" junto do valor, e o vermelho continuou falhando pelo motivo certo.
Outro caso: ao fazer o CA-02, o agente notou que a spec não tinha critério para a tela de pagamento; o teste só chamava a rota direto, e a Marli não teria como pagar pelo navegador. Criamos o CA-06 (formulário de pagamento), com vermelho e verde próprios.

## Uma vez em que o agente poderia ter "otimizado para o verde"
O teste do CA-02 (pagamento total zera o saldo) nasceu verde, porque a implementação do CA-01 já cobria a quitação. Em vez de estragar o código ou o teste para forçar uma falha, o agente parou e perguntou. Decidimos commitar o teste sozinho, declarando que ele nasceu verde e não conta como ciclo vermelho-verde (D-06). O mesmo aconteceu com o teste de -R$ 5,00, já coberto pelo CA-04. Nenhum teste foi apagado, pulado ou ajustado para passar.

## Uma refatoração feita com segurança
Depois dos critérios, a conversão e a validação de formato do valor estavam repetidas entre fiado e pagamento. Extraímos a função ler_valor(), usada pelas duas rotas (https://github.com/MariaEgoetz/FiaBar/commit/ffef801dcb5adebd8bd018d021708e69d068b5e5). A suíte inteira tinha 35 testes passando antes e continuou com 35 passando depois; nenhum ficou vermelho no caminho, então foi refatoração, não mudança de comportamento. A checagem de faixa ficou em cada rota, porque as regras são diferentes (fiado até R$ 5.000,00; pagamento até o saldo).

## O que mudou no harness
A skill implementar-spec passou a seguir o ciclo vermelho, verde e refatorar, com commits separados para o vermelho e o verde, a proibição de apagar ou alterar testes para passar e a instrução de perguntar quando a spec não define uma mensagem ou limite (https://github.com/MariaEgoetz/FiaBar/commit/144ba8364660ab160c2cb6b7877b7a6a02031de4).

## Pendências
Dois testes antigos da feature 001 têm a mesma fraqueza de procurar só o valor na página (test_rn02_mais_de_duas_casas_rejeitado e test_valor_nao_numerico_rejeitado). Ficaram para uma próxima tarefa, fora do escopo da 002.

## Resultado
Spec 002 com CA-01 a CA-06 cobertos por teste, suíte inteira com 35 testes passando, incluindo os da feature 001, sem regressão.
