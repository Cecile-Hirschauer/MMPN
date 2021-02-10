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
            db.commit()
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
            delete_category = cursor.fetchone()
            if delete_category is None:
                abort(404)
            else:
                cursor = db.execute(
                    "DELETE FROM categories WHERE id = ?",
                    [cat_id]
                )
                db.commit()
                return jsonify({
                    'id': delete_category[0],
                    'name': delete_category[1]
                })
        except IndexError:
            abort(404)


@app.route('/toys')
def index_toys():
    db = get_db()
    cursor = db.execute("SELECT toys.id, toys.name, toys.description, \
                        toys.price, categories.name as category \
                        FROM toys \
                        LEFT JOIN categories \
                        ON toys.category_id = categories.id")
    toys = []
    for toy in cursor:
        toys.append({
            "id": toy[0],
            "name": toy[1],
            "description": toy[2],
            "price": toy[3],
            "category": toy[4]
        })
    return jsonify(toys)


@app.route('/toys/<int:toy_id>')
def show_toy(toy_id):
    db = get_db()
    cursor = db.execute(
        "SELECT toys.id, toys.name, toys.description, \
        toys.price, categories.name as category \
        FROM toys \
        LEFT JOIN categories \
        ON toys.category_id = categories.id \
        WHERE toys.id = ?", [toy_id]
    )
    toy = cursor.fetchone()
    if toy is None:
        abort(404)
    return jsonify({
        "id": toy[0],
        "name": toy[1],
        "description": toy[2],
        "price": toy[3],
        "category": toy[4]
    })


@app.route('/toys', methods=['GET', 'POST'])
def create_toy():
    db = get_db()
    if request.method == "POST":
        try:
            new_toy = request.values
            new_toy_keys = list(new_toy.keys())
            attributes = ['name', 'description', 'price', 'category_id']
            for k in new_toy_keys:
                if k in attributes and len(new_toy_keys) == len(attributes):
                    name = request.form.get('name')
                    description = request.form.get('description')
                    price = int(request.form.get('price'))
                    category = request.form.get('category')
                    cursor = db.execute(
                        "SELECT id FROM categories WHERE name = ?",
                        [category]
                    )
                    my_category = cursor.fetchone()
                    cursor = db.execute(
                    "INSERT INTO toys (name, description, price, category_id) \
                     VALUES (?, ?, ?, ?)",
                        [name, description, price, my_category[0]]
                    )
                    db.commit()
                    cursor = db.execute(
                        "SELECT MAX(toys.id), toys.name, toys.description, \
                        toys.price, categories.name as category \
                        FROM toys \
                        LEFT JOIN categories \
                        ON toys.category_id = categories.id \
                        WHERE categories.name = ?",
                        [category]
                    )
                    new_toy = cursor.fetchone()
                    if cursor is None:
                        abort(404)
                    else:
                        return jsonify({
                            "id": new_toy[0],
                            "name": new_toy[1],
                            "description": new_toy[2],
                            "price": new_toy[3],
                            "category": new_toy[4]
                        })          
        except Exception:
            abort(422)


@app.route('/toys/<int:toy_id>', methods=['GET', 'POST', 'PUT'])
def update_toy(toy_id):
    db = get_db()
    if request.method == 'PUT':
        try:
            modified_toy = request.values
            for k in modified_toy.keys():
                if k == 'name':
                    name = request.form['name']
                    cursor = db.execute(
                        "UPDATE toys \
                        SET name = ? \
                        WHERE id = ?",
                        [name, toy_id]
                    )
                if k == 'description':
                    description = request.form['description']
                    cursor = db.execute(
                        "UPDATE toys \
                        SET description = ? \
                        WHERE id = ?",
                        [description, toy_id]
                    )
                if k == 'price':
                    price = int(request.form['price'])
                    cursor=db.execute(
                        "UPDATE toys \
                        SET price = ? \
                        WHERE id = ?",
                        [price, toy_id]
                    )
                if k == 'category_id':
                    category_id = int(request.form['category_id'])
                    cursor = db.execute(
                        "UPDATE toys \
                        SET category_id = ? \
                        WHERE id = ?",
                        [category_id, toy_id]
                    ) 
                if k == 'category':
                    category = request.form['category']
                    cursor = db.execute(
                        "SELECT id FROM categories WHERE name = ?",
                        [category]
                    )
                    my_cat = cursor.fetchone()
                    cursor = db.execute(
                        "UPDATE toys \
                        SET category_id = ? \
                        WHERE id = ?",
                        [my_cat[0], toy_id]
                    )
            db.commit()
            cursor = db.execute(
                "SELECT toys.id, toys.name, toys.description, \
            toys.price, categories.name as category \
            FROM toys \
            LEFT JOIN categories \
            ON toys.category_id = categories.id \
            WHERE toys.id = ?", [toy_id]
            )
            toy = cursor.fetchone()
            if toy is None:
                abort(404)
            return jsonify({
                "id": toy[0],
                "name": toy[1],
                "description": toy[2],
                "price": toy[3],
                "category": toy[4]
            })
        except IndexError:
            abort(404)


@app.route('/toys/<int:toy_id>', methods=['GET', 'DELETE'])
def delete_toy(toy_id):
    db = get_db()
    try:
        if request.method == 'DELETE':
            cursor = db.execute(
                "SELECT toys.id, toys.name, description, price, \
                categories.name as category \
                FROM toys \
                LEFT JOIN categories \
                ON toys.category_id = categories.id \
                WHERE toys.id = ?",
                [toy_id]
            )
            toy = cursor.fetchone()
            if toy is None:
                abort(404)
            else:
                cursor = db.execute(
                    "DELETE FROM toys WHERE id = ?", [toy_id]
                )
                db.commit()
                return jsonify({
                    "id": toy[0],
                    "name": toy[1],
                    "description": toy[2],
                    "price": toy[3],
                    "category": toy[4]
                })
        else:
            abort(404)
    except IndexError:
        abort(404)


if __name__ == "__main__":
    app.run(debug=True)
