from decimal import Decimal

from flask import Blueprint, abort, redirect, render_template, request, url_for

from app.db import get_db

bp = Blueprint("fiado", __name__)


def formatar_reais(centavos):
    reais = f"{centavos / 100:,.2f}"
    return "R$ " + reais.replace(",", "_").replace(".", ",").replace("_", ".")


def buscar_cliente(cliente_id):
    cliente = get_db().execute(
        "SELECT id, nome FROM cliente WHERE id = ?", (cliente_id,)
    ).fetchone()
    if cliente is None:
        abort(404)
    return cliente


def listar_clientes(erro=None):
    clientes = get_db().execute(
        "SELECT id, nome, telefone FROM cliente ORDER BY nome"
    ).fetchall()
    return render_template("clientes.html", clientes=clientes, erro=erro)


@bp.get("/clientes")
def ver_clientes():
    return listar_clientes()


@bp.post("/clientes")
def cadastrar_cliente():
    nome = request.form["nome"].strip()
    telefone = "".join(c for c in request.form["telefone"] if c.isdigit())
    if not 2 <= len(nome) <= 60:
        return listar_clientes("O nome deve ter entre 2 e 60 caracteres")
    if telefone and len(telefone) not in (10, 11):
        return listar_clientes("Informe um telefone com 10 ou 11 dígitos")
    db = get_db()
    existentes = db.execute("SELECT nome FROM cliente").fetchall()
    if any(c["nome"].strip().lower() == nome.lower() for c in existentes):
        return listar_clientes("Já existe um cliente com esse nome")
    db.execute(
        "INSERT INTO cliente (nome, telefone) VALUES (?, ?)",
        (nome, telefone or None),
    )
    db.commit()
    return redirect(url_for("fiado.ver_clientes"))


@bp.get("/clientes/<int:cliente_id>")
def ver_cliente(cliente_id):
    cliente = buscar_cliente(cliente_id)
    saldo = get_db().execute(
        "SELECT COALESCE(SUM(valor_centavos), 0) FROM lancamento"
        " WHERE cliente_id = ?",
        (cliente_id,),
    ).fetchone()[0]
    return render_template(
        "cliente.html", cliente=cliente, saldo=formatar_reais(saldo)
    )


@bp.post("/clientes/<int:cliente_id>/fiados")
def registrar_fiado(cliente_id):
    buscar_cliente(cliente_id)
    valor = Decimal(request.form["valor"].replace(".", "").replace(",", "."))
    db = get_db()
    db.execute(
        "INSERT INTO lancamento (cliente_id, descricao, valor_centavos)"
        " VALUES (?, ?, ?)",
        (cliente_id, request.form["descricao"], int(valor * 100)),
    )
    db.commit()
    return redirect(url_for("fiado.ver_cliente", cliente_id=cliente_id))
