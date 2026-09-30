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


def test_ca01_saldo_aumenta_apos_registrar_fiado(app, client):
    joao = criar_cliente_com_saldo(app, "João", 3000)
    assert "R$ 30,00" in client.get(f"/clientes/{joao}").get_data(as_text=True)

    resposta = client.post(
        f"/clientes/{joao}/fiados",
        data={"descricao": "2 cervejas", "valor": "12,50"},
        follow_redirects=True,
    )

    assert resposta.status_code == 200
    assert "R$ 42,50" in resposta.get_data(as_text=True)
