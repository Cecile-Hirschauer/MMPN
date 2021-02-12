from flask import Flask, request, jsonify, g, abort
import sqlite3
from hashlib import md5
from random import randrange

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


@app.route('/categories/<cat_name>/toys')
def show_toys_category(cat_name):
    db = get_db()
    if request.method == 'GET':
        try:
            cursor = db.execute(
                """SELECT toys.id, toys.name, description, price,
                    categories.name as category
                    FROM toys
                    LEFT JOIN categories
                    ON toys.category_id = categories.id
                    WHERE categories.name = ?""", [cat_name]
            )
            my_toys = cursor.fetchall()
            toys_category = []
            for toy in my_toys:
                toys_category.append({
                    "id": toy[0],
                    "name": toy[1],
                    "description": toy[2],
                    "price": toy[3],
                    'category': toy[4]
                })
            if toys_category == []:
                abort(404)
            return jsonify(toys_category)
        except UnboundLocalError:
            abort(404)


@app.route('/toys')
def index_toys():
    db = get_db()
    cursor = db.execute("""SELECT toys.id, toys.name, toys.description,
                        toys.price, categories.name as category
                        FROM toys
                        LEFT JOIN categories
                        ON toys.category_id = categories.id""")
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
        """SELECT toys.id, toys.name, toys.description,
        toys.price, categories.name as category
        FROM toys
        LEFT JOIN categories
        ON toys.category_id = categories.id
        WHERE toys.id = ?""", [toy_id]
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
            attributes = ['name', 'description', 'price', 'category']
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
                    category_id = cursor.fetchone()
                    cursor = db.execute(
                            "INSERT INTO toys (name, description, price, category_id) \
                            VALUES (?, ?, ?, ?)",
                            [name, description, price, category_id[0]]
                    )
                    db.commit()
                    cursor = db.execute(
                        """SELECT MAX(toys.id), toys.name, toys.description,
                        toys.price, categories.name as category
                        FROM toys
                        LEFT JOIN categories
                        ON toys.category_id = categories.id
                        WHERE categories.name = ?""",
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
                        "UPDATE toys SET name = ? WHERE id = ?",
                        [name, toy_id]
                    )
                if k == 'description':
                    description = request.form['description']
                    cursor = db.execute(
                        "UPDATE toys SET description = ? WHERE id = ?",
                        [description, toy_id]
                    )
                if k == 'price':
                    price = int(request.form['price'])
                    cursor = db.execute(
                        "UPDATE toys SET price = ? WHERE id = ?",
                        [price, toy_id]
                    )
                if k == 'category_id':
                    category_id = int(request.form['category_id'])
                    cursor = db.execute(
                        "UPDATE toys SET category_id = ? WHERE id = ?",
                        [category_id, toy_id]
                    )
                if k == 'category':
                    category = request.form['category']
                    cursor = db.execute(
                        "SELECT id FROM categories WHERE name = ?",
                        [category]
                    )
                    my_cat = cursor.fetchone()
            db.commit()
            cursor = db.execute(
                """SELECT toys.id, toys.name, toys.description,
                toys.price, categories.name as category
                FROM toys
                LEFT JOIN categories
                ON toys.category_id = categories.id
                WHERE toys.id = ?""",
                [toy_id]
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
                """SELECT toys.id, toys.name, description, price,
                categories.name as category
                FROM toys
                LEFT JOIN categories
                ON toys.category_id = categories.id
                WHERE toys.id = ?""",
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


@app.route('/elves')
def index_elves():
    db = get_db()
    cursor = db.execute("""
                        SELECT id, first_name, last_name, login, password
                        FROM elves
                        """)
    elves = []
    for elf in cursor:
        elves.append({
            'id': elf[0],
            'first_name': elf[1],
            'last_name': elf[2],
            'login': elf[3],
            'password': elf[4]
        })
    if elves is None:
        abort(404)
    return jsonify(elves)


@app.route('/elves/<int:elf_id>')
def show_elf(elf_id):
    db = get_db()
    cursor = db.execute("""SELECT id, first_name, last_name, login, password
                           FROM elves
                           WHERE id = ?
                        """, [elf_id])
    elf = cursor.fetchone()
    if elf is None:
        abort(404)
    return jsonify({
        'id': elf[0],
        'first_name': elf[1],
        'last_name': elf[2],
        'login': elf[3],
        'password': elf[4]
        })


@app.route('/elves', methods=['GET', 'POST'])
def create_elf():
    db = get_db()
    if request.method == 'POST':
        try:
            values = request.values
            values_keys = list(values.keys())
            attributes = ['first_name', 'last_name', 'login', 'password']
            for k in attributes:
                if k in values_keys and len(values_keys) == len(attributes):
                    first_name = request.form['first_name']
                    last_name = request.form['last_name']
                    login = request.form['login']
                    password = request.form['password']
                    hash_password = md5(password.encode()).hexdigest()
            cursor = db.execute(
                """ INSERT INTO elves (first_name, last_name, login, password)
                VALUES (?, ?, ?, ?)""",
                [first_name, last_name, login, hash_password]
                )
            db.commit()
            cursor = db.execute("""
                        SELECT MAX(id), first_name, last_name, login, password
                        FROM elves
                        """)
            elf = cursor.fetchone()
            if elf is None:
                abort(404)
            return jsonify({
                'id': elf[0],
                'first_name': elf[1],
                'last_name': elf[2],
                'login': elf[3],
                'password': elf[4]
                })
        except Exception:
            abort(422)


@app.route('/elves/<int:elf_id>', methods=['GET', 'POST', 'PUT'])
def update_elf(elf_id):
    db = get_db()
    if request.method == 'PUT':
        try:
            modified_elf = request.values.to_dict()
            for k in modified_elf.keys():
                if k == 'first_name':
                    first_name = request.form['first_name']
                    cursor = db.execute(
                        "UPDATE elves SET first_name = ? WHERE id = ?",
                        [first_name, elf_id]
                    )
                if k == 'last_name':
                    last_name = request.form['last_name']
                    cursor = db.execute(
                        "UPDATE elves SET last_name = ? WHERE id = ?",
                        [last_name, elf_id]
                    )
                if k == 'login':
                    login = request.form['login']
                    cursor = db.execute(
                        "UPDATE elves SET login = ? WHERE id = ?",
                        [login, elf_id]
                    )
                if k == 'password':
                    password = request.form['password']
                    hash_password = md5(password.encode()).hexdigest()
                    cursor = db.execute(
                        "UPDATE elves SET password = ? WHERE id = ?",
                        [hash_password, elf_id]
                    )
            db.commit()
            cursor = db.execute("""SELECT id, first_name,
                                last_name, login, password
                                FROM elves
                                WHERE id = ?""",
                                [elf_id])
            elf = cursor.fetchone()
            if elf is None:
                abort(404)
            return jsonify({
                'id': elf[0],
                'first_name': elf[1],
                'last_name': elf[2],
                'login': elf[3],
                'password': elf[4]
                })
        except IndexError:
            abort(404)


@app.route('/elves/<int:elf_id>', methods=['GET', 'DELETE'])
def delete_elf(elf_id):
    db = get_db()
    try:
        if request.method == 'DELETE':
            cursor = db.execute("""SELECT id, first_name,
                                last_name, login, password
                                FROM elves
                                WHERE id = ?""",
                                [elf_id])
            elf = cursor.fetchone()
            if elf is None:
                abort(404)
            else:
                cursor = db.execute(
                    "DELETE FROM elves WHERE id = ?", [elf_id]
                )
                db.commit()
                return jsonify({
                    'id': elf[0],
                    'first_name': elf[1],
                    'last_name': elf[2],
                    'login': elf[3],
                    'password': elf[4]
                })
        else:
            abort(404)
    except IndexError:
        abort(404)


@app.route('/wishes')
def index_wishes():
    db = get_db()
    cursor = db.execute(
        """SELECT wishes.id, child_name, toys.name as toy
        FROM wishes LEFT JOIN toys
        ON wishes.toy_id = toys.ID"""
    )
    wishes = []
    for wish in cursor:
        wishes.append({
            'id': wish[0],
            'child_name': wish[1],
            'toy': wish[2]
        })
    if wishes != []:
        return jsonify(wishes)
    return "No wish yet!"


@app.route('/wishes', methods=['GET', 'POST'])
def create_wish():
    db = get_db()
    if request.method == 'POST':
        wish = request.values
        wish_keys = list(wish.keys())
        attributes = ['child_name', 'toy']
        for k in attributes:
            if k in wish_keys and len(wish_keys) == len(attributes):
                child_name = request.form.get('child_name')
                toy = request.form.get('toy')
            
        cursor = db.execute("SELECT id FROM toys WHERE name = ?", [toy])
        toy_id = cursor.fetchone()
        if toy_id is None:
            abort(422)
        else:
            cursor = db.execute(
                    """INSERT INTO wishes (child_name, toy_id)
                    VALUES (?, ?)""", [child_name, toy_id[0]]
                )
            db.commit()
            cursor = db.execute(
            """SELECT max(wishes.id), child_name, toys.name as toy
            FROM wishes LEFT JOIN toys 
            ON wishes.toy_id = toys.id
            WHERE toys.name = ?""",
            [toy]
        )
            new_wish = cursor.fetchone()
            cursor = db.execute(
                "SELECT id FROM elves"
            )
            elves_id = []
            for elf in cursor:
                elves_id.append(elf[0])
            elf_random = randrange(len(elves_id))
            elf_id = elves_id[elf_random]
            cursor = db.execute(
                """INSERT INTO schedules (wish_id, elf_id)
                VALUES (?, ?)""", [new_wish[0], elf_id]
            )
            db.commit()
            return jsonify({
                'id': new_wish[0],
                'child_name': new_wish[1],
                'toy': new_wish[2]
            })
         

@app.route('/schedules')
def index_schedules():
    db = get_db()
    cursor = db. execute(
        "SELECT id, wish_id, elf_id, done, done_at FROM schedules"
    )
    schedules = []
    for sched in cursor:
        schedules.append({
            'id': sched[0],
            'wish_id': sched[1],
            'elf_id': sched[2],
            'done': sched[3],
            'done_at': sched[4]
        })
    return jsonify(schedules)


if __name__ == "__main__":
    app.run(debug=True)
