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
                "INSERT INTO categories (name) values (?)",
                [name]
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
        except Exception:
            abort(422)


@app.route('/categories/<int:cat_id>', methods=['GET', 'POST', 'PUT'])
def update_category(cat_id):
    db = get_db()
    if request.method == "PUT":
        try:
            name = request.form['name']
            cursor = db.execute(
                "UPDATE categories SET name = ? WHERE id = ?",
                [name, cat_id]
            )
            modified_cat = db.commit()
            cursor = db.execute(
                "SELECT id, name FROM categories WHERE id = ?",
                [cat_id]
            )
            modified_cat = cursor.fetchone()
            if modified_cat is None:
                abort(404)
            return jsonify({
                'id': modified_cat[0],
                'name': modified_cat[1]
            })
        except IndexError:
            abort(404)


@app.route('/categories/<int:cat_id>', methods=['GET', 'DELETE'])
def delete_category(cat_id):
    db = get_db()
    if request.method == "DELETE":
        try:
            cursor = db.execute(
                "SELECT id, name FROM categories WHERE id = ?",
                [cat_id]
            )
            del_cat = []
            for cat in cursor:
                del_cat.append({
                    "id": cat[0],
                    "name": cat[1]
                    })
            cursor = db.execute(
                "DELETE FROM categories WHERE id = ?",
                [cat_id]
            )
            db.commit()
            if len(del_cat) <= 0:
                abort(404)
            return jsonify(del_cat)
        except IndexError:
            abort(404)


if __name__ == "__main__":
    app.run(debug=True)
