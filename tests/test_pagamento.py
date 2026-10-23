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
