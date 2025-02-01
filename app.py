from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import shutil

app = Flask(__name__)

# Diretório onde o script está rodando
DIRETORIO_BASE = os.path.dirname(os.path.abspath(__file__))

# Configuração das pastas
PASTA_IMAGENS = os.path.join(DIRETORIO_BASE, "fotinhas")
PASTA_APROVADAS = os.path.join(DIRETORIO_BASE, "3p")
PASTA_REJEITADAS = os.path.join(DIRETORIO_BASE, "apagar")

# Criar as pastas se não existirem
for pasta in [PASTA_IMAGENS, PASTA_APROVADAS, PASTA_REJEITADAS]:
    os.makedirs(pasta, exist_ok=True)

# Pegar a lista de imagens disponíveis
def listar_imagens():
    return [f for f in os.listdir(PASTA_IMAGENS) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

@app.route("/")
def index():
    imagens = listar_imagens()
    if imagens:
        return render_template("index.html", imagem=imagens[0])
    else:
        return "Todas as imagens foram revisadas!"

# Rota para servir imagens diretamente da pasta "fotinhas"
@app.route("/imagem/<nome_imagem>")
def servir_imagem(nome_imagem):
    return send_from_directory(PASTA_IMAGENS, nome_imagem)

@app.route("/acao", methods=["POST"])
def acao():
    nome_imagem = request.form["imagem"]
    destino = request.form["acao"]

    caminho_origem = os.path.join(PASTA_IMAGENS, nome_imagem)

    if destino == "aprovar":
        shutil.move(caminho_origem, os.path.join(PASTA_APROVADAS, nome_imagem))
    elif destino == "rejeitar":
        shutil.move(caminho_origem, os.path.join(PASTA_REJEITADAS, nome_imagem))

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
