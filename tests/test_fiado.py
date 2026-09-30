import pytest

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


def cadastrar_cliente(client, nome, telefone=""):
    return client.post(
        "/clientes",
        data={"nome": nome, "telefone": telefone},
        follow_redirects=True,
    )


def contar_clientes(app):
    with app.app_context():
        return get_db().execute("SELECT COUNT(*) FROM cliente").fetchone()[0]


def test_cadastrar_cliente_aparece_na_lista(client):
    resposta = cadastrar_cliente(client, "Maria Silva", "64999999999")

    assert resposta.status_code == 200
    assert "Maria Silva" in client.get("/clientes").get_data(as_text=True)


@pytest.mark.parametrize("nome", ["A", "A" * 61])
def test_nome_fora_do_tamanho_rejeitado(app, client, nome):
    resposta = cadastrar_cliente(client, nome)

    assert "O nome deve ter entre 2 e 60 caracteres" in resposta.get_data(
        as_text=True
    )
    assert contar_clientes(app) == 0


@pytest.mark.parametrize("telefone", ["649999999", "649999999999"])
def test_telefone_invalido_rejeitado(app, client, telefone):
    resposta = cadastrar_cliente(client, "Maria Silva", telefone)

    assert "Informe um telefone com 10 ou 11 dígitos" in resposta.get_data(
        as_text=True
    )
    assert contar_clientes(app) == 0


def test_telefone_com_pontuacao_aceito(client):
    cadastrar_cliente(client, "Maria Silva", "(64) 99999-9999")

    assert "Maria Silva" in client.get("/clientes").get_data(as_text=True)


def test_telefone_vazio_aceito(client):
    cadastrar_cliente(client, "Maria Silva")

    assert "Maria Silva" in client.get("/clientes").get_data(as_text=True)


def test_ca04_nome_duplicado_rejeitado(client):
    cadastrar_cliente(client, "Maria Silva")

    resposta = cadastrar_cliente(client, " maria silva ")

    assert "Já existe um cliente com esse nome" in resposta.get_data(as_text=True)
    lista = client.get("/clientes").get_data(as_text=True)
    assert lista.lower().count("maria silva") == 1


def contar_lancamentos(app):
    with app.app_context():
        return get_db().execute("SELECT COUNT(*) FROM lancamento").fetchone()[0]


def registrar_fiado(client, cliente_id, valor, descricao="2 cervejas"):
    return client.post(
        f"/clientes/{cliente_id}/fiados",
        data={"descricao": descricao, "valor": valor},
        follow_redirects=True,
    )


def test_ca02_valor_zero_rejeitado(app, client):
    joao = criar_cliente_com_saldo(app, "João", 3000)

    resposta = registrar_fiado(client, joao, "0,00")

    pagina = resposta.get_data(as_text=True)
    assert "Informe um valor entre R$ 0,01 e R$ 5.000,00" in pagina
    assert "R$ 30,00" in pagina
    assert contar_lancamentos(app) == 1


@pytest.mark.parametrize(
    ("valor", "salva"),
    [
        ("0,01", True),
        ("5.000,00", True),
        ("5.000,01", False),
        ("0,00", False),
        ("-5,00", False),
    ],
)
def test_rn01_faixa_de_valor(app, client, valor, salva):
    joao = criar_cliente_com_saldo(app, "João", 3000)

    resposta = registrar_fiado(client, joao, valor)

    pagina = resposta.get_data(as_text=True)
    mensagem = "Informe um valor entre R$ 0,01 e R$ 5.000,00"
    assert (mensagem not in pagina) == salva
    assert contar_lancamentos(app) == (2 if salva else 1)
