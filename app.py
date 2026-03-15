from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'sonar123'


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

    # Verifica se já existem itens
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
            ('1015','Pendrive',10,'Rua 3','F','1'),

            ('1016','Hub USB',10,'','','1'),
            ('1017','Dock station',10,'','','1'),
            ('1018','Carregador portátil (power bank)',10,'','','1'),
            ('1019','Carregador de celular',10,'','','1'),
            ('1020','Cabo USB',10,'','','1'),
            ('1021','Cabo HDMI',10,'','','1'),
            ('1022','Cabo Ethernet',10,'','','1'),
            ('1023','Adaptador USB-C',10,'','','1'),
            ('1024','Adaptador HDMI',10,'','','1'),
            ('1025','Roteador Wi-Fi',10,'','','1'),
            ('1026','Repetidor de sinal Wi-Fi',10,'','','1'),
            ('1027','Modem',10,'','','1'),
            ('1028','Placa de captura',10,'','','1'),
            ('1029','Controle de videogame',10,'','','1'),
            ('1030','Console de videogame',10,'','','1'),
            ('1031','Óculos de realidade virtual',10,'','','1'),
            ('1032','Projetor',10,'','','1'),
            ('1033','Ring light',10,'','','1'),
            ('1034','Câmera digital',10,'','','1'),
            ('1035','Câmera de segurança',10,'','','1'),
            ('1036','Leitor de cartão de memória',10,'','','1'),
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


# ---------------- RODAR SISTEMA ----------------

if __name__ == '__main__':
    app.run(debug=True)
