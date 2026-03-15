from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = "sonar123"
app.config["SESSION_COOKIE_SECURE"] = False
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


def conectar():
    return sqlite3.connect('banco.db')


# ---------------- CRIAR BANCO ----------------

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

    cur.execute("SELECT COUNT(*) FROM itens")
    total = cur.fetchone()[0]

    if total == 0:

        itens_iniciais = [

        ('1001','Monitor',10,'Rua 1','C','1'),
        ('1002','Notebook',10,'Rua 1','D','1'),
        ('1003','Tablet',10,'Rua 1','E','1'),

        ('1004','Smartphone',10,'Rua 2','A','1'),
        ('1005','Smartwatch',10,'Rua 2','B','1'),
        ('1006','Fone de ouvido',10,'Rua 2','C','1'),
        ('1007','Headset',10,'Rua 2','D','1'),
        ('1008','Caixa de som',10,'Rua 2','E','1'),
        ('1009','Microfone',10,'Rua 2','F','1'),

        ('1010','Webcam',10,'Rua 3','A','1'),
        ('1011','Impressora',10,'Rua 3','B','1'),
        ('1012','Scanner',10,'Rua 3','C','1'),
        ('1013','HD externo',10,'Rua 3','D','1'),
        ('1014','SSD externo',10,'Rua 3','E','1'),
        ('1015','Pendrive',10,'Rua 3','F','1')

        ]

        cur.executemany(
            "INSERT INTO itens(codigo,nome,quantidade,corredor,prateleira,nivel) VALUES (?,?,?,?,?,?)",
            itens_iniciais
        )

        con.commit()


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

    with conectar() as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM itens")
        itens = cur.fetchall()

    return render_template('dashboard.html', itens=itens)


# ---------------- CADASTRAR ITEM ----------------

@app.route('/cadastrar', methods=['GET','POST'])
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
            ''',(codigo,nome,quantidade,corredor,prateleira,nivel))

            con.commit()

        return redirect('/dashboard')

    return render_template('cadastrar.html')


# ---------------- DAR BAIXA ----------------

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

            cur.execute("UPDATE itens SET quantidade=? WHERE id=?", (nova,id_item))
            con.commit()

            return redirect('/dashboard')

        cur.execute("SELECT * FROM itens")
        itens = cur.fetchall()

    return render_template('baixar.html', itens=itens)


# ---------------- RODAR SERVIDOR ----------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
