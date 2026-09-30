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
