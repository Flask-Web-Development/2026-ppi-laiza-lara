from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()

    lugares = db.execute(
        'SELECT l.id, nome, descricao, data_visita, author_id, username'
        ' FROM lugar l JOIN user u ON l.author_id = u.id'
        ' ORDER BY data_visita DESC'
    ).fetchall()

    return render_template('blog/index.html', lugares=lugares)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        data_visita = request.form['data_visita']
        error = None

        if not nome:
            error = 'nome is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()

            db.execute(
                'INSERT INTO lugar (nome, descricao, data_visita, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (nome, descricao, data_visita, g.user['id'])
            )

            db.commit()

            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_lugar(id, check_author=True):
    lugar = get_db().execute(
        'SELECT l.id, nome, descricao, data_visita, author_id, username'
        ' FROM lugar l JOIN user u ON l.author_id = u.id'
        ' WHERE l.id = ?',
        (id,)
    ).fetchone()

    if lugar is None:
        abort(404, f"Lugar id {id} doesn't exist.")

    if check_author and lugar['author_id'] != g.user['id']:
        abort(403)

    return lugar


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    lugar = get_lugar(id)

    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        data_visita = request.form['data_visita']
        error = None

        if not nome:
            error = 'nome is required.'

        if error is not None:
            flash(error)

        else:
            db = get_db()

            db.execute(
                'UPDATE lugar SET nome = ?, descricao = ?, data_visita = ?'
                ' WHERE id = ?',
                (nome, descricao, data_visita, id)
            )

            db.commit()

            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', lugar=lugar)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_lugar(id)

    db = get_db()

    db.execute(
        'DELETE FROM lugar WHERE id = ?',
        (id,)
    )

    db.commit()

    return redirect(url_for('blog.index'))