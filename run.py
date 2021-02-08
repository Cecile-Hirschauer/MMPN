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


if __name__ == "__main__":
    app.run(debug=True)