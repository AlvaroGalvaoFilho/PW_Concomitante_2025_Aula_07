from pydantic import ValidationError  # Para capturar erros de validação do Freelancer
from tabulate import tabulate         # Para exibir a lista de freelancers formatada
from freelancers.freelancer_repo import FreelancerRepo  # Importa o repositório
from freelancers.freelancer import Freelancer          # Importa a classe de domínio

def exibir_menu():
    """Exibe o menu principal de opções no console."""
    print("\n--- Menu de Gerenciamento de Freelancers ---")
    print("a) Cadastrar Freelancer")
    print("b) Listar Freelancers")
    print("c) Alterar Freelancer")
    print("d) Excluir Freelancer")
    print("e) Sair")
    print("-----------------------------------------")

def obter_entrada_usuario(mensagem, tipo=str):
    """Solicita uma entrada do usuário, com validação de tipo."""
    while True:
        entrada = input(mensagem)
        try:
            if tipo == float:
                return float(entrada)
            elif tipo == int:
                return int(entrada)
            else:
                return entrada.strip()
        except ValueError:
            print(f"Entrada inválida. Por favor, insira um valor do tipo '{tipo.__name__}'.")

def cadastrar_freelancer(repo: FreelancerRepo):
    """Função para lidar com a opção de cadastrar um novo freelancer."""
    print("\n--- Cadastro de Novo Freelancer ---")
    try:
        nome = obter_entrada_usuario("Nome: ")
        cpf = obter_entrada_usuario("CPF (11 dígitos): ")
        idade = obter_entrada_usuario("Idade: ", int)
        novo_freelancer = Freelancer(nome=nome, cpf=cpf, idade=idade)
        freelancer_id = repo.adicionar(novo_freelancer)
        if freelancer_id:
            print(f"Freelancer '{novo_freelancer.nome}' cadastrado com sucesso! ID: {freelancer_id}")
        else:
            print("Falha ao cadastrar o freelancer.")
    except ValidationError as e:
        print("\nErro de validação ao cadastrar freelancer:")
        for error in e.errors():
            print(f"- Campo '{error['loc'][0]}': {error['msg']}")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado ao cadastrar: {e}")

def listar_freelancers(repo: FreelancerRepo):
    """Função para lidar com a opção de listar todos os freelancers."""
    print("\n--- Lista de Freelancers Cadastrados ---")
    freelancers = repo.obter_todos()
    if freelancers:
        tabela = [[f.id, f.nome, f.cpf, f.idade] for f in freelancers]
        cabecalhos = ["ID", "Nome", "CPF", "Idade"]
        print(tabulate(tabela, headers=cabecalhos, tablefmt="grid", numalign="right", stralign="left"))
    else:
        print("Nenhum freelancer cadastrado.")

def alterar_freelancer(repo: FreelancerRepo):
    """Função para lidar com a opção de alterar um freelancer existente."""
    print("\n--- Alteração de Freelancer ---")
    try:
        freelancer_id = obter_entrada_usuario("ID do freelancer a ser alterado: ", int)
        freelancer_existente = repo.obter(freelancer_id)
        if freelancer_existente:
            print("\nDados atuais do freelancer:")
            print(f"  Nome: {freelancer_existente.nome}")
            print(f"  CPF: {freelancer_existente.cpf}")
            print(f"  Idade: {freelancer_existente.idade}")
            print("\nDigite os novos dados (deixe em branco para manter o valor atual):")
            nome = obter_entrada_usuario(f"Novo Nome ({freelancer_existente.nome}): ") or freelancer_existente.nome
            cpf = obter_entrada_usuario(f"Novo CPF ({freelancer_existente.cpf}): ") or freelancer_existente.cpf
            idade_str = obter_entrada_usuario(f"Nova Idade ({freelancer_existente.idade}): ")
            idade = int(idade_str) if idade_str else freelancer_existente.idade
            freelancer_atualizado = Freelancer(id=freelancer_existente.id, nome=nome, cpf=cpf, idade=idade)
            if repo.atualizar(freelancer_atualizado):
                print(f"Freelancer ID {freelancer_id} atualizado com sucesso!")
            else:
                print(f"Falha ao atualizar o freelancer ID {freelancer_id}.")
        else:
            print(f"Freelancer com ID {freelancer_id} não encontrado.")
    except ValidationError as e:
        print("\nErro de validação ao alterar freelancer:")
        for error in e.errors():
            print(f"- Campo '{error['loc'][0]}': {error['msg']}")
    except ValueError:
        print("Entrada inválida para ID. A alteração foi cancelada.")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado ao alterar: {e}")

def excluir_freelancer(repo: FreelancerRepo):
    """Função para lidar com a opção de excluir um freelancer."""
    print("\n--- Exclusão de Freelancer ---")
    try:
        freelancer_id = obter_entrada_usuario("ID do freelancer a ser excluído: ", int)
        freelancer = repo.obter(freelancer_id)
        if not freelancer:
            print(f"Freelancer com ID {freelancer_id} não encontrado.")
            return
        confirmacao = input(f"Tem certeza que deseja excluir o freelancer '{freelancer.nome}' (CPF: {freelancer.cpf})? (s/N): ").lower()
        if confirmacao == 's':
            if repo.excluir(freelancer_id):
                print(f"Freelancer ID {freelancer_id} excluído com sucesso.")
            else:
                print(f"Falha ao excluir o freelancer ID {freelancer_id}.")
        else:
            print("Exclusão cancelada.")
    except ValueError:
        print("ID inválido. A exclusão foi cancelada.")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado ao excluir: {e}")

def main():
    """Função principal que executa o loop do menu interativo."""
    repo = FreelancerRepo()
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").lower().strip()
        if opcao == 'a':
            cadastrar_freelancer(repo)
        elif opcao == 'b':
            listar_freelancers(repo)
        elif opcao == 'c':
            alterar_freelancer(repo)
        elif opcao == 'd':
            excluir_freelancer(repo)
        elif opcao == 'e':
            print("Saindo do programa. Até logo!")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()
