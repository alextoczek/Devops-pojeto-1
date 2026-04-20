from flask import Flask, jsonify, render_template
import json
import os

app = Flask(__name__)
@app.route('/')
def home():
    return jsonify({"mensagem": "API funcionando"})

# carregar dados direto (sem funções separadas)
def carregar_estudantes():
    if not os.path.exists('estudantes.json'):
        return {}
    with open('estudantes.json', 'r', encoding='utf-8') as f:
        return json.load(f)


# página inicial
@app.route('/')
def inicio():
    return render_template('index.html')


# rota simples para listar estudantes
@app.route('/estudantes')
def listar_estudantes():
    dados = carregar_estudantes()
    return jsonify(dados)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)