from app.db import get_db


def criar_cliente_com_saldo(app, nome, centavos):
    with app.app_context():
        db = get_db()
        cliente_id = db.execute(
            "INSERT INTO cliente (nome) VALUES (?)", (nome,)
        ).lastrowid
        db.execute(
            "INSERT INTO lancamento (cliente_id, descricao, valor_centavos)"
            " VALUES (?, ?, ?)",
            (cliente_id, "saldo anterior", centavos),
        )
        db.commit()
    return cliente_id


def test_ca01_pagamento_parcial_abate_saldo(app, client):
    joao = criar_cliente_com_saldo(app, "João", 4250)
    assert "R$ 42,50" in client.get(f"/clientes/{joao}").get_data(as_text=True)

    resposta = client.post(
        f"/clientes/{joao}/pagamentos",
        data={"valor": "20,00"},
        follow_redirects=True,
    )

    assert resposta.status_code == 200
    assert "R$ 22,50" in resposta.get_data(as_text=True)


def test_ca02_pagamento_total_zera_saldo(app, client):
    joao = criar_cliente_com_saldo(app, "João", 4250)

    resposta = client.post(
        f"/clientes/{joao}/pagamentos",
        data={"valor": "42,50"},
        follow_redirects=True,
    )

    assert resposta.status_code == 200
    assert "R$ 0,00" in resposta.get_data(as_text=True)


def test_ca06_tela_exibe_formulario_de_pagamento(app, client):
    joao = criar_cliente_com_saldo(app, "João", 4250)

    html = client.get(f"/clientes/{joao}").get_data(as_text=True)

    assert f'action="/clientes/{joao}/pagamentos"' in html
    assert "Valor" in html
    assert "Registrar pagamento" in html


def test_ca04_pagamento_zero_rejeitado(app, client):
    joao = criar_cliente_com_saldo(app, "João", 4250)

    resposta = client.post(
        f"/clientes/{joao}/pagamentos",
        data={"valor": "0,00"},
        follow_redirects=True,
    )

    html = resposta.get_data(as_text=True)
    assert "Informe um valor maior que zero" in html
    assert "Saldo devedor: <strong>R$ 42,50</strong>" in html


def test_rn03_pagamento_com_mais_de_duas_casas_rejeitado(app, client):
    joao = criar_cliente_com_saldo(app, "João", 4250)

    resposta = client.post(
        f"/clientes/{joao}/pagamentos",
        data={"valor": "12,345"},
        follow_redirects=True,
    )

    html = resposta.get_data(as_text=True)
    assert "Use no máximo duas casas decimais" in html
    assert "Saldo devedor: <strong>R$ 42,50</strong>" in html


def test_rn03_pagamento_nao_numerico_rejeitado(app, client):
    joao = criar_cliente_com_saldo(app, "João", 4250)

    resposta = client.post(
        f"/clientes/{joao}/pagamentos",
        data={"valor": "abc"},
        follow_redirects=True,
    )

    html = resposta.get_data(as_text=True)
    assert "Informe um valor numérico, ex.: 12,50" in html
    assert "Saldo devedor: <strong>R$ 42,50</strong>" in html


def test_ca03_pagamento_maior_que_saldo_rejeitado(app, client):
    joao = criar_cliente_com_saldo(app, "João", 4250)

    resposta = client.post(
        f"/clientes/{joao}/pagamentos",
        data={"valor": "50,00"},
        follow_redirects=True,
    )

    html = resposta.get_data(as_text=True)
    assert "O pagamento não pode ser maior que o saldo devedor" in html
    assert "Saldo devedor: <strong>R$ 42,50</strong>" in html


def test_ca04_pagamento_negativo_rejeitado(app, client):
    joao = criar_cliente_com_saldo(app, "João", 4250)

    resposta = client.post(
        f"/clientes/{joao}/pagamentos",
        data={"valor": "-5,00"},
        follow_redirects=True,
    )

    html = resposta.get_data(as_text=True)
    assert "Informe um valor maior que zero" in html
    assert "Saldo devedor: <strong>R$ 42,50</strong>" in html


def test_ca05_historico_mostra_pagamento(app, client):
    joao = criar_cliente_com_saldo(app, "João", 4250)
    with app.app_context():
        db = get_db()
        db.execute(
            "INSERT INTO pagamento (cliente_id, valor_centavos, criado_em)"
            " VALUES (?, 2000, '2026-10-24 10:15:00')",
            (joao,),
        )
        db.commit()

    pagina = client.get(f"/clientes/{joao}").get_data(as_text=True)

    linhas = [linha for linha in pagina.splitlines() if "Pagamento" in linha]
    assert any(
        "24/10/2026" in linha and "10:15" in linha and "R$ 20,00" in linha
        for linha in linhas
    )
