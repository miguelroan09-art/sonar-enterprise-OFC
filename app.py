from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "sonar_secret_key"

# Usuário fixo
USUARIO_CORRETO = "admin"
SENHA_CORRETA = "1234"

# Produtos simulados
produtos = [
    {"nome": "Teclado", "quantidade": 10, "localizacao": "Prateleira A"},
    {"nome": "Mouse", "quantidade": 20, "localizacao": "Prateleira B"},
]

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/logar", methods=["POST"])
def logar():
    usuario = request.form["usuario"]
    senha = request.form["senha"]

    if usuario == USUARIO_CORRETO and senha == SENHA_CORRETA:
        session["usuario"] = usuario
        return redirect(url_for("dashboard"))
    else:
        return render_template("login.html", erro="Usuário ou senha incorretos")

@app.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", produtos=produtos)

# ---------------------------
# NOVA ROTA DE CADASTRO
# ---------------------------

@app.route("/cadastro")
def cadastro():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("cadastro.html")

@app.route("/adicionar", methods=["POST"])
def adicionar():
    if "usuario" not in session:
        return redirect(url_for("login"))

    nome = request.form["nome"]
    quantidade = request.form["quantidade"]
    localizacao = request.form["localizacao"]

    novo_produto = {
        "nome": nome,
        "quantidade": quantidade,
        "localizacao": localizacao
    }

    produtos.append(novo_produto)

    return redirect(url_for("dashboard"))

# ---------------------------

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "sonar_secret_key"

# Usuário fixo
USUARIO_CORRETO = "admin"
SENHA_CORRETA = "1234"

# Produtos simulados
produtos = [
    {"nome": "Teclado", "quantidade": 10, "localizacao": "Rua 1, Prateleira A"},
    {"nome": "Mouse", "quantidade": 20, "localizacao": "Rua 1, Prateleira B"},
]

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/logar", methods=["POST"])
def logar():
    usuario = request.form["usuario"]
    senha = request.form["senha"]

    if usuario == USUARIO_CORRETO and senha == SENHA_CORRETA:
        session["usuario"] = usuario
        return redirect(url_for("dashboard"))
    else:
        return render_template("login.html", erro="Usuário ou senha incorretos")

@app.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", produtos=produtos)

# ---------------------------
# NOVA ROTA DE CADASTRO
# ---------------------------

@app.route("/cadastro")
def cadastro():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("cadastro.html")

@app.route("/adicionar", methods=["POST"])
def adicionar():
    if "usuario" not in session:
        return redirect(url_for("login"))

    nome = request.form["nome"]
    quantidade = request.form["quantidade"]
    localizacao = request.form["localizacao"]

    novo_produto = {
        "nome": nome,
        "quantidade": quantidade,
        "localizacao": localizacao
    }

    produtos.append(novo_produto)

    return redirect(url_for("dashboard"))

# ---------------------------

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
