from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)


def caminho_arquivo(categoria):
    arquivos = {
        'estudantes': 'estudantes.json',
        'professores': 'professores.json',
        'disciplinas': 'disciplinas.json',
        'turmas': 'turmas.json',
        'matriculas': 'matriculas.json'
    }
    return arquivos.get(categoria)


def carregar_dados(categoria):
    arquivo = caminho_arquivo(categoria)
    if not arquivo:
        return {}
    if not os.path.exists(arquivo):
        return {}
    with open(arquivo, 'r', encoding='utf-8') as f:
        return json.load(f)


def salvar_dados(categoria, dados):
    arquivo = caminho_arquivo(categoria)
    if not arquivo:
        return
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


@app.route('/')
def pagina_inicial():
    return render_template('index.html')


@app.route('/api')
def inicio_api():
    return jsonify({
        "mensagem": "API do sistema acadêmico funcionando"
    })


@app.route('/<categoria>', methods=['GET'])
def listar(categoria):
    if caminho_arquivo(categoria) is None:
        return jsonify({"erro": "Categoria inválida"}), 404
    dados = carregar_dados(categoria)
    return jsonify(dados)


@app.route('/<categoria>/<codigo>', methods=['GET'])
def buscar_por_codigo(categoria, codigo):
    if caminho_arquivo(categoria) is None:
        return jsonify({"erro": "Categoria inválida"}), 404
    dados = carregar_dados(categoria)
    if codigo not in dados:
        return jsonify({"erro": "Registro não encontrado"}), 404
    return jsonify(dados[codigo])


@app.route('/<categoria>', methods=['POST'])
def incluir(categoria):
    if caminho_arquivo(categoria) is None:
        return jsonify({"erro": "Categoria inválida"}), 404

    dados = carregar_dados(categoria)
    novo = request.json

    if not novo or 'codigo' not in novo:
        return jsonify({"erro": "Campo 'codigo' é obrigatório"}), 400

    codigo = str(novo['codigo'])

    if codigo in dados:
        return jsonify({"erro": "Código já existe"}), 400

    registro = dict(novo)
    del registro['codigo']

    dados[codigo] = registro
    salvar_dados(categoria, dados)

    return jsonify({
        "mensagem": "Registro criado com sucesso",
        "codigo": codigo,
        "dados": registro
    }), 201


@app.route('/<categoria>/<codigo>', methods=['PUT'])
def atualizar(categoria, codigo):
    if caminho_arquivo(categoria) is None:
        return jsonify({"erro": "Categoria inválida"}), 404

    dados = carregar_dados(categoria)

    if codigo not in dados:
        return jsonify({"erro": "Registro não encontrado"}), 404

    atualizacao = request.json
    if not atualizacao:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    dados[codigo].update(atualizacao)
    salvar_dados(categoria, dados)

    return jsonify({
        "mensagem": "Registro atualizado com sucesso",
        "codigo": codigo,
        "dados": dados[codigo]
    })


@app.route('/<categoria>/<codigo>', methods=['DELETE'])
def excluir(categoria, codigo):
    if caminho_arquivo(categoria) is None:
        return jsonify({"erro": "Categoria inválida"}), 404

    dados = carregar_dados(categoria)

    if codigo not in dados:
        return jsonify({"erro": "Registro não encontrado"}), 404

    removido = dados.pop(codigo)
    salvar_dados(categoria, dados)

    return jsonify({
        "mensagem": "Registro removido com sucesso",
        "codigo": codigo,
        "dados": removido
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)