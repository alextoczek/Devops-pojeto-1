
## Alex Silva toczek
from datetime import date
import json
import os
# listas

menu_principal= ()
estudantes = {}
professores = {}
disciplinas = {}
turmas = {}
matriculas = {}


nomes_singulares = {
    'Estudantes': 'Estudante',
    'Professores': 'Professor(a)',
    'Disciplinas': 'Disciplina',
    'Turmas': 'Turma',
    'Matriculas': 'Matrícula'
}

nomes_menu_Principal = {
    1: 'Estudantes',
    2: 'Professores',
    3: 'Disciplinas',
    4: 'Turmas',
    5: 'Matriculas'
}

nomes_menu_secundario = {
    1: 'Incluir',
    2: 'Excluir',
    3: 'Listar',
    4: 'Atualizar',
    0: 'Voltar'
}
def caminho_arquivo(categoria):
    # Retorna o nome do arquivo JSON para cada categoria
    arquivos = {
        'Estudantes': 'estudantes.json',
        'Professores': 'professores.json',
        'Disciplinas': 'disciplinas.json',
        'Turmas': 'turmas.json',
        'Matriculas': 'matriculas.json'
    }
    return arquivos.get(categoria, None)

def salvar_dados(categoria, dados):
    arquivo = caminho_arquivo(categoria)
    if arquivo is None:
        print(f"Erro: Categoria '{categoria}' inexistente para salvar.")
        return
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar_dados(categoria):
    arquivo = caminho_arquivo(categoria)
    if arquivo is None:
        print(f"Erro: Categoria '{categoria}' inexistente para carregar.")
        return {}
    if not os.path.exists(arquivo):
        return {}
    with open(arquivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def menu_prinpal():

    try:
        data_hoje = date.today()
        print("Data de hoje:", data_hoje.strftime("%d/%m/%Y"))
        print("------MENU PUC-PR------")
        # OPÇÕES DO MENU
        print('1 - Estudantes')
        print('2 - Professores')
        print('3 - Disciplinas')
        print('4 - turma')
        print('5 - Matricula')
        print('0 - Sair')

        opcao = int(input("Selecione a opção desejada: "))
        if opcao in [0,1,2,3,4,5]:
            return opcao
        else:
            print("Opção inválida! Digite apenas números de 0 a 5.")
        return None
    except ValueError:
        print("Opção inválida! Digite apenas números de 0 a 5.")
        return None

def menu_secundario(categoria):
    try:
        print(f'Menu de operações de {nomes_singulares[categoria]}')
        print('1 - Incluir')
        print('2 - Excluir')
        print('3 - listar')
        print('4 - Atualizar')
        print('0 - Voltar')

        opcao1 = int(input("Selecione a opção desejada: "))
        if opcao1 in [0,1, 2, 3, 4,]:
            return opcao1
        else:
            print("Opção inválida! Digite apenas números de 0 a 4.")
        return None
    except ValueError:
        print("Opção inválida! Digite apenas números de 0 a 4.")

        return None
def operacao_incluir(categoria):
    try:
        print(f'Você escolheu Incluir a categoria de {nomes_singulares[categoria]}')
        dados = carregar_dados(categoria)
        codigo = input('Digite o código de cadastro (somente números): ').strip()

        if not codigo.isdigit():
            print("Código inválido! Deve conter apenas números.")
            return

        if codigo in dados:
            print(f"Já existe um(a) {nomes_singulares[categoria]} com esse código!")
            return

        if categoria in ["Estudantes", "Professores"]:
            print(f'Você escolheu Incluir a categoria de {nomes_singulares[categoria]}')
            nome = input('Digite o nome completo: ')
            cpf = input('Digite o CPF completo, incluindo pontos e traço (ex: 123.456.789-00): ')
            dados[codigo] = {'nome': nome, 'cpf': cpf}
            print(f'----{nomes_singulares[categoria]}----\nCódigo: {codigo}\nNome: {nome}\nCPF: {cpf}\nAdicionado com sucesso!')


        elif categoria == 'Disciplinas':
            print(f'Você escolheu Incluir a categoria de {nomes_singulares[categoria]}')
            nome_disciplina = input('Digite o nome da disciplina: ')
            dados[codigo] = {'nome': nome_disciplina,}
            print(f'----{nomes_singulares[categoria]}----\nCódigo: {codigo}\nNome: {nome_disciplina}\nAdicionado com sucesso!')

        elif categoria == 'Turmas':

            professores = carregar_dados('Professores')
            disciplinas = carregar_dados('Disciplinas')
            cod_professor = input('Digite o código do professor responsável: ')
            cod_disciplina = input('Digite o código da disciplina: ')

            if cod_professor not in professores:
                print("Professor não encontrado!")
                return
            if cod_disciplina not in disciplinas:
                print("Disciplina não encontrada!")
                return
            dados[codigo] = {'professor': cod_professor, 'disciplina': cod_disciplina}
        elif categoria == 'Matriculas':
            estudantes = carregar_dados('Estudantes')
            turmas = carregar_dados('Turmas')
            cod_turma = input('Digite o código da turma: ').strip()
            cod_estudante = input('Digite o código do estudante: ').strip()

            if cod_turma not in turmas:
                print("Turma não encontrada!")
                return
            if cod_estudante not in estudantes:
                print("Estudante não encontrado!")
                return

            dados[codigo] = {'turma': cod_turma, 'estudante': cod_estudante}


        salvar_dados(categoria, dados)
        print(f'{nomes_singulares[categoria]} incluído(a) com sucesso!')
        input("\nPressione ENTER para voltar...")

    except Exception as e:
        print("Erro ao incluir:", e)


def operacao_excluir(categoria):
    try:
        dados = carregar_dados(categoria)
        codigo_excluir = input(f'Digite o código do(a) {nomes_singulares[categoria]} que deseja excluir: ').strip()
        if codigo_excluir not in dados:
            print(f'\nCódigo {codigo_excluir} não encontrado em {categoria}.')
            return

        print(f'\n----{nomes_singulares[categoria]} Encontrado----')

        if categoria in ['Estudantes', 'Professores']:
            print(f'Nome: {dados[codigo_excluir]["nome"]}\nCPF: {dados[codigo_excluir]["cpf"]}')
        elif categoria == 'Disciplinas':
            print(f'Nome da disciplina: {dados[codigo_excluir]["nome"]}')
        elif categoria == 'Turmas':
            professores = carregar_dados('Professores')
            disciplinas = carregar_dados('Disciplinas')
            prof_nome = professores.get(str(dados[codigo_excluir]["professor"]), {}).get("nome", "Desconhecido")
            disc_nome = disciplinas.get(str(dados[codigo_excluir]["disciplina"]), {}).get("nome", "Desconhecida")
            print(f'Professor: {prof_nome}\nDisciplina: {disc_nome}')
        elif categoria == 'Matriculas':
            estudantes = carregar_dados('Estudantes')
            est_nome = estudantes.get(str(dados[codigo_excluir]["estudante"]), {}).get("nome", "Desconhecido")
            print(f'Estudante: {est_nome}\nTurma: {dados[codigo_excluir]["turma"]}')

        confirmar = input("Tem certeza que deseja excluir (s/n): ").lower()
        if confirmar == 's':
            del dados[codigo_excluir]
            salvar_dados(categoria, dados)
            print(f'\n{nomes_singulares[categoria]} excluído(a) com sucesso!')
        else:
            print('---Operação Cancelada---')

    except Exception as e:
        print("Erro ao excluir:", e)


def operacao_atualizar(categoria):
    try:
        dados = carregar_dados(categoria)
        if not dados:
            print(f'Nenhum(a) {nomes_singulares[categoria]} cadastrado(a).')
            return

        codigo = input(f'Digite o código do(a) {nomes_singulares[categoria]} que deseja atualizar: ').strip()
        if codigo not in dados:
            print(f'Código {codigo} não encontrado!')
            return

        if categoria in ['Estudantes', 'Professores']:
            novo_nome = input("Digite o novo nome (ou pressione ENTER para manter): ").strip()
            novo_cpf = input("Digite o novo CPF (ou pressione ENTER para manter): ").strip()
            if novo_nome:
                dados[codigo]['nome'] = novo_nome
            if novo_cpf:
                dados[codigo]['CPF'] = novo_cpf
        elif categoria == 'Disciplinas':
            novo_nome = input("Digite o novo nome da disciplina (ou ENTER para manter): ").strip()
            if novo_nome:
                dados[codigo]['nome'] = novo_nome
        elif categoria == 'Turmas':
            novo_prof = input("Digite o novo código do professor (ou ENTER para manter): ").strip()
            novo_disc = input("Digite o novo código da disciplina (ou ENTER para manter): ").strip()
            if novo_prof:
                dados[codigo]['professor'] = int(novo_prof)
            if novo_disc:
                dados[codigo]['disciplina'] = int(novo_disc)
        elif categoria == 'Matriculas':
            novo_est = input("Digite o novo código do estudante (ou ENTER para manter): ").strip()
            novo_turma = input("Digite o novo código da turma (ou ENTER para manter): ").strip()
            if novo_est:
                dados[codigo]['estudante'] = int(novo_est)
            if novo_turma:
                dados[codigo]['turma'] = int(novo_turma)

        salvar_dados(categoria, dados)
        print(f"{nomes_singulares[categoria]} atualizado(a) com sucesso!")

    except Exception as e:
        print("Erro, tente novamente.:", e)


def operacao_listar(categoria):
    dados = carregar_dados(categoria)

    if not dados:
        print(f"Nenhum(a) {nomes_singulares[categoria]} cadastrado(a).")
        input("\nPressione ENTER para voltar...")
        return

    print(f"\nLista de {categoria}:")

    if categoria in ['Estudantes', 'Professores']:
        for codigo, info in dados.items():
            print(f"\nCódigo: {codigo}\nNome: {info['nome']}\nCPF: {info['cpf']}")
    elif categoria == 'Disciplinas':
        for codigo, info in dados.items():
            print(f"\nCódigo: {codigo}\nNome da disciplina: {info['nome']}")
    elif categoria == 'Turmas':
        professores = carregar_dados('Professores')
        disciplinas = carregar_dados('Disciplinas')
        for codigo, info in dados.items():
            prof = professores.get(str(info['professor']), {}).get('nome', 'Desconhecido')
            disc = disciplinas.get(str(info['disciplina']), {}).get('nome', 'Desconhecida')
            print(
                f"\nCódigo da Turma: {codigo}\nProfessor: {prof} (código {info['professor']})\nDisciplina: {disc} (código {info['disciplina']})")
    elif categoria == 'Matriculas':
        estudantes = carregar_dados('Estudantes')
        turmas = carregar_dados('Turmas')
        for codigo, info in dados.items():
            est = estudantes.get(str(info['estudante']), {}).get('nome', 'Desconhecido')
            print(
                f"\nCódigo da Matrícula: {codigo}\nEstudante: {est} (código {info['estudante']})\nTurma: {info['turma']}")

    input("\nPressione ENTER para voltar...")


while True:
    escolha_menu_principal = menu_prinpal()

    if escolha_menu_principal == 0:
        print("Encerrando o sistema. Até logo!")
        break
    elif escolha_menu_principal in nomes_menu_Principal:
        categoria = nomes_menu_Principal[escolha_menu_principal]
        nome_singular = nomes_singulares[categoria]
        while True:
            escolha_menu_secundario = menu_secundario(categoria)

            if escolha_menu_secundario == 0:
                print(f"Voltando ao menu principal...\n")
                break
            elif escolha_menu_secundario == 1:
                operacao_incluir(categoria)
            elif escolha_menu_secundario == 2:
                operacao_excluir(categoria)
            elif escolha_menu_secundario == 3:
                operacao_listar(categoria)
            elif escolha_menu_secundario == 4:
                operacao_atualizar(categoria)
            else:
                print("Escolha inválida! Tente novamente.")

























