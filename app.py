from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'sonar123'


def conectar():
    return sqlite3.connect('banco.db')


# Criar tabelas
with conectar() as con:
    cur = con.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY,
        email TEXT,
        senha TEXT)
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS itens(
        id INTEGER PRIMARY KEY,
        codigo TEXT,
        nome TEXT,
        quantidade INTEGER,
        corredor TEXT,
        prateleira TEXT,
        nivel TEXT)
    ''')

    cur.execute("INSERT OR IGNORE INTO usuarios VALUES (1,'admin@sonar.com','123')")


# ---------------- LOGIN ----------------

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/logar', methods=['POST'])
def logar():
    email = request.form['email']
    senha = request.form['senha']

    with conectar() as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email=? AND senha=?", (email, senha))
        user = cur.fetchone()

        if user:
            session['user'] = email
            return redirect('/dashboard')

    return "Login inválido"


# ---------------- DASHBOARD ----------------

@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect('/')

    return render_template('dashboard.html')


# ---------------- CADASTRAR ITEM ----------------

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():

    if request.method == 'POST':

        codigo = request.form['codigo']
        nome = request.form['nome']
        quantidade = request.form['quantidade']
        corredor = request.form['corredor']
        prateleira = request.form['prateleira']
        nivel = request.form['nivel']

        with conectar() as con:
            cur = con.cursor()

            cur.execute('''
            INSERT INTO itens(codigo,nome,quantidade,corredor,prateleira,nivel)
            VALUES (?,?,?,?,?,?)
            ''', (codigo, nome, quantidade, corredor, prateleira, nivel))

            con.commit()

        return redirect('/dashboard')

    return render_template('cadastrar.html')


# ---------------- DAR BAIXA EM ITEM ----------------

@app.route('/baixar', methods=['GET','POST'])
def baixar():

    with conectar() as con:
        cur = con.cursor()

        if request.method == 'POST':

            id_item = request.form['id_item']
            quantidade = int(request.form['quantidade'])

            cur.execute("SELECT quantidade FROM itens WHERE id=?", (id_item,))
            atual = cur.fetchone()[0]

            nova = atual - quantidade

            if nova < 0:
                nova = 0

            cur.execute("UPDATE itens SET quantidade=? WHERE id=?", (nova, id_item))
            con.commit()

            return redirect('/dashboard')

        cur.execute("SELECT * FROM itens")
        itens = cur.fetchall()

    return render_template('baixar.html', itens=itens)


# ---------------- RODAR SISTEMA ----------------

if __name__ == '__main__':
    app.run(debug=True)
