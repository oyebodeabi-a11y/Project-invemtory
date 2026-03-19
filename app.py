
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
DB = "database.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/enternew")
def enternew():
    return render_template("product.html")


@app.route("/addrec", methods=['POST'])
def addrec():
    try:
        nm = request.form['nm']
        price = request.form['price']
        quantity = request.form['quantity']
        batchno = request.form['batchno']

        with get_db() as con:
            con.execute(
                "INSERT INTO Product (name, price, quantity, batchno) VALUES (?, ?, ?, ?)",
                (nm, price, quantity, batchno)
            )

        msg = "Record successfully added!"

    except Exception as e:
        msg = f"Error: {e}"

    return render_template('result.html', msg=msg)


@app.route('/list')
def list():
    with get_db() as con:
        rows = con.execute("SELECT rowid, * FROM Product").fetchall()

    return render_template("list.html", rows=rows)


@app.route("/edit", methods=['POST'])
def edit():
    try:
        rowid = request.form['id']

        with get_db() as con:
            rows = con.execute(
                "SELECT rowid, * FROM Product WHERE rowid = ?",
                (rowid,)
            ).fetchall()

        return render_template("edit.html", rows=rows)

    except:
        return "Error loading edit page"


@app.route("/editrec", methods=['POST'])
def editrec():
    try:
        rowid = request.form['rowid']
        nm = request.form['nm']
        price = request.form['price']
        quantity = request.form['quantity']
        batchno = request.form['batchno']

        with get_db() as con:
            con.execute(
                """UPDATE Product 
                   SET name=?, price=?, quantity=?, batchno=? 
                   WHERE rowid=?""",
                (nm, price, quantity, batchno, rowid)
            )

        msg = "Record updated successfully!"

    except Exception as e:
        msg = f"Error: {e}"

    return render_template('result.html', msg=msg)


@app.route("/delete", methods=['POST'])
def delete():
    try:
        rowid = request.form['id']

        with get_db() as con:
            con.execute(
                "DELETE FROM Product WHERE rowid=?",
                (rowid,)
            )

        msg = "Record deleted successfully!"

    except Exception as e:
        msg = f"Error: {e}"

    return render_template('result.html', msg=msg)


if __name__ == '__main__':
    app.run(debug=True, port=5006)