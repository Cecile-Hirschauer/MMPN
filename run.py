from flask import Flask, request, jsonify, g, abort
import sqlite3

app = Flask(__name__)
DATABASE = 'app.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.route('/categories')
def index_categories():
    db = get_db()
    cursor = db.execute("SELECT id, name FROM categories")
    categories = []
    for cat in cursor:
        categories.append({
            "id": cat[0],
            "name": cat[1]
            })
    return jsonify(categories)


@app.route('/categories/<int:cat_id>')
def show_category(cat_id):
    db = get_db()
    cursor = db.execute(
        "SELECT id, name FROM categories WHERE id = ?", [cat_id]
    )
    category = cursor.fetchone()
    if category is None:
        abort(404)
    return jsonify({
        "id": category[0],
        "name": category[1]
    })


@app.route('/categories', methods=['GET', 'POST'])
def create_category():
    db = get_db()
    if request.method == "POST":
        try:
            name = request.form.get('name')
            cursor = db.execute(
                "INSERT INTO categories (name) values (?)", [name]
            )
            new_cat = db.commit()
            cursor = db.execute(
                "SELECT MAX(id), name FROM categories"
            )
            new_cat = cursor.fetchone()
            if new_cat is None:
                abort(404)
            return jsonify({
                "id": new_cat[0],
                "name": new_cat[1]
            })
        except UnprocessableEntity:
            abort(422)


if __name__ == "__main__":
    app.run(debug=True)
