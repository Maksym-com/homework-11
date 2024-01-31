from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from sqlalchemy import select

from app.database import Session
from app.models import Good

bp = Blueprint("good", __name__)

@bp.route("/")
def get_goods():
    with Session() as session:
        query = select(Good)
        goods = session.scalars(query).all()
    return render_template("all_goods.html", goods=goods)

@bp.route("/<int:good_id>")
def get_good(good_id):
    with Session() as session:
        query = select(Good).where(Good.id == good_id)
        good = session.scalars(query).one()
        if not good:
            abort(404)
    return render_template('good.html', good=good)

@bp.route('/create', methods=["GET", "POST"])
def create_good():
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        if not name:
            flash("Name is required")
        else:
            with Session() as session:
                new_good = Good(name=name, description=description)
                session.add(new_good)
                session.commit()
            return redirect(url_for('default.index'))
    return render_template('create_good.html')

@bp.route("/<int:good_id>/edit", methods=["GET", "POST"])
def edit_good(good_id):
    with Session() as session:
        good = session.scalars(select(Good).where(Good.id == good_id)).one()

    if not good:
        abort(404)

    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        if not name:
            flash("Name is required")
        else:
            with Session() as session:
                good.update(
                    {"name": name,
                     "description": description}
                )
                session.commit()
            return redirect(url_for('default.index'))
    return render_template('edit_good.html', good=good)


@bp.route("/<int:good_id>/delete", methods=["GET", "POST"])
def delete_good(good_id):
    with Session() as session:
        good = session.scalars(select(Good).where(Good.id == good_id)).one()

    if not good:
        abort(404)

    name = good.name
    with Session() as session:
        session.delete(good)
        session.commit()
    flash(f"{name} was successfully deleted")
    return redirect(url_for('default.index'))