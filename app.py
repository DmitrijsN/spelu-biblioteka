from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# Datubāzes izveide
# Šī funkcija izveido tabulu, ja tā vēl neeksistē

def init_db():
    conn = sqlite3.connect("games.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nosaukums TEXT NOT NULL,
            zanrs TEXT NOT NULL,
            vertejums INTEGER NOT NULL,
            status TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


# Galvenā lapa
@app.route('/')
def index():
    conn = sqlite3.connect("games.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM games")
    games = cursor.fetchall()

    conn.close()

    return render_template("index.html", games=games)


# Pievienošanas lapa
@app.route('/pievienot', methods=['GET', 'POST'])
def pievienot():
    if request.method == 'POST':
        nosaukums = request.form['nosaukums']
        zanrs = request.form['zanrs']
        vertejums = request.form['vertejums']
        status = request.form['status']

        conn = sqlite3.connect("games.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO games (nosaukums, zanrs, vertejums, status) VALUES (?, ?, ?, ?)",
            (nosaukums, zanrs, vertejums, status)
        )

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template("pievienot.html")


# Dzēšanas funkcija
@app.route('/dzest/<int:id>')
def dzest(id):
    conn = sqlite3.connect("games.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM games WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect('/')


# Programmas palaišana
if __name__ == '__main__':
    init_db()
    app.run(debug=True)